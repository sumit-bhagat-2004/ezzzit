"use client";

import { useState, useEffect, useRef } from "react";
import Editor from "@monaco-editor/react";
import { Play, Terminal } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import VoiceExplainControls from "./VoiceExplainControls";
import ExecutionView from "./ExecutionView";
import VisualizerDispatcher from "./VisualizerDispatcher";
import TimelineControls from "./TimelineControls";
import AIAnalysisPanel from "./AIAnalysisPanel";
import { TracePlayer } from "../lib/TracePlayer";

type TraceStep = {
  step: number;
  line: number;
  function: string;
  event: string;
  call_stack_depth: number;
  variables: Record<string, unknown>;
  explanation?: string; // RAG explanation
};

type DataStructure = {
  name: string;
  type: string;
  variables: string[];
  description: string;
};

type AIAnalysis = {
  structures: DataStructure[];
  trace_enrichment: {
    step_index_mapping: Record<string, string>;
  };
  summary: string;
};

type ExecutionResponse = {
  output: string;
  trace: TraceStep[];
  steps: number;
  exception: string | null;
  error: string | null;
  ai_analysis?: AIAnalysis | null;
  rag_explanations?: string[]; // RAG step explanations summary
};

export default function EditorUI() {
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState(`a = 5
b = 3

sum_val = a + b

if sum_val > 5:
    result = sum_val * 2
else:
    result = sum_val - 2

print(result)`);

  const [stdin, setStdin] = useState("");
  const [loading, setLoading] = useState(false);
  const [explanationLevel, setExplanationLevel] = useState("medium");
  const [execution, setExecution] = useState<ExecutionResponse | null>(null);
  const [currentLine, setCurrentLine] = useState<number | null>(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1); // 0.25x, 0.5x, 1x, 1.5x, 2x
  const [editorMode, setEditorMode] = useState<"edit" | "trace">("edit");
  const tracePlayerRef = useRef<TracePlayer | null>(null);
  const playIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const languages = ["python", "javascript", "java"];

  useEffect(() => {
    return () => {
      if (playIntervalRef.current) {
        clearInterval(playIntervalRef.current);
      }
    };
  }, []);

  // Restart playback with new speed when speed changes during play
  useEffect(() => {
    if (isPlaying && playIntervalRef.current) {
      handlePause();
      handlePlay();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playbackSpeed]);

  const handlePlay = () => {
    if (!tracePlayerRef.current) return;
    setIsPlaying(true);
    // Calculate delay based on speed (base delay is 1200ms at 1x speed)
    const delay = 1200 / playbackSpeed;
    playIntervalRef.current = setInterval(() => {
      const player = tracePlayerRef.current;
      if (!player) return;

      const next = player.next();
      if (next) {
        setCurrentLine(next.line);
        setCurrentStepIndex(player.getCurrentIndex());
      }

      if (player.isAtEnd()) {
        setIsPlaying(false);
        if (playIntervalRef.current) {
          clearInterval(playIntervalRef.current);
          playIntervalRef.current = null;
        }
      }
    }, delay);
  };

  const handlePause = () => {
    setIsPlaying(false);
    if (playIntervalRef.current) {
      clearInterval(playIntervalRef.current);
      playIntervalRef.current = null;
    }
  };

  const handleNext = () => {
    if (!tracePlayerRef.current) return;
    const next = tracePlayerRef.current.next();
    if (next) {
      setCurrentLine(next.line);
      setCurrentStepIndex(tracePlayerRef.current.getCurrentIndex());
    }
  };

  const handlePrev = () => {
    if (!tracePlayerRef.current) return;
    const prev = tracePlayerRef.current.prev();
    if (prev) {
      setCurrentLine(prev.line);
      setCurrentStepIndex(tracePlayerRef.current.getCurrentIndex());
    }
  };

  const handleReset = () => {
    if (!tracePlayerRef.current) return;
    handlePause();
    tracePlayerRef.current.reset();
    const first = tracePlayerRef.current.current();
    if (first) {
      setCurrentLine(first.line);
      setCurrentStepIndex(0);
    }
  };

  const handleSliderChange = (step: number) => {
    if (!tracePlayerRef.current) return;
    handlePause();
    const target = tracePlayerRef.current.go(step);
    if (target) {
      setCurrentLine(target.line);
      setCurrentStepIndex(step);
    }
  };

  const handleRun = async () => {
    try {
      setLoading(true);

      // Call both APIs in parallel
      const [executionRes, ragRes] = await Promise.allSettled([
        // Main execution API
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/execute`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code, language, stdin }),
        }),
        // RAG explanation API
        fetch(`${process.env.NEXT_PUBLIC_RAG_API_URL}/rag/explain_trace`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            code,
            language,
            stdin,
            level: explanationLevel,
          }),
        }),
      ]);

      // Process main execution response
      let data: ExecutionResponse = {
        output: "",
        trace: [],
        steps: 0,
        exception: null,
        error: null,
      };

      if (executionRes.status === "fulfilled" && executionRes.value.ok) {
        data = await executionRes.value.json();
      } else {
        data.error = "Failed to connect to execution server";
        data.exception = "Network Error";
      }

      // Process RAG response and merge explanations
      if (ragRes.status === "fulfilled" && ragRes.value.ok) {
        const ragData = await ragRes.value.json();

        // Merge RAG explanations into trace steps
        if (ragData.trace && Array.isArray(ragData.trace)) {
          data.trace = data.trace.map((step, idx) => {
            const ragStep = ragData.trace[idx];
            return {
              ...step,
              explanation: ragStep?.explanation || "",
            };
          });

          // Extract all explanations for summary
          data.rag_explanations = ragData.trace
            .map((s: any) => s.explanation)
            .filter(Boolean);
        }
      }

      setExecution(data);
      // Reset current line when new execution starts
      if (data.trace && data.trace.length > 0) {
        tracePlayerRef.current = new TracePlayer(data.trace);
        setCurrentLine(data.trace[0].line);
        setCurrentStepIndex(0);
        setEditorMode("trace"); // Switch to trace mode after execution
      }
    } catch (err) {
      console.error(err);
      setExecution({
        output: "",
        trace: [],
        steps: 0,
        exception: "Failed to connect to execution server",
        error: "Network Error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative w-full h-screen bg-[#030712] overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px]" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px]" />

      <div className="h-screen flex flex-col p-2 relative z-10">
        {/* Main Card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex-1 flex flex-col relative bg-[#0B0F1A]/80 border border-white/10 rounded-lg shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden"
        >
          {/* Top Bar */}
          <div className="flex items-center justify-between px-3 py-2 border-b border-white/10 bg-white/2">
            <div className="flex items-center gap-3">
              <span className="text-xs text-gray-400 font-mono">
                main.{language === "python" ? "py" : "js"}
              </span>

              {/* Mode Toggle (only show after execution) */}
              {execution && (
                <div className="flex gap-1 bg-black/40 rounded-lg p-1 border border-white/10">
                  <button
                    onClick={() => setEditorMode("edit")}
                    className={`px-3 py-1 text-xs rounded transition ${
                      editorMode === "edit"
                        ? "bg-indigo-600 text-white"
                        : "text-gray-400 hover:text-white"
                    }`}
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => setEditorMode("trace")}
                    className={`px-3 py-1 text-xs rounded transition ${
                      editorMode === "trace"
                        ? "bg-indigo-600 text-white"
                        : "text-gray-400 hover:text-white"
                    }`}
                  >
                    Trace
                  </button>
                </div>
              )}
            </div>

            <div className="flex items-center gap-3">
              {/* Explanation Level Dropdown */}
              <div className="flex items-center gap-2">
                <label className="text-xs text-indigo-400 font-mono font-semibold">
                  Level:
                </label>
                <select
                  value={explanationLevel}
                  onChange={(e) => setExplanationLevel(e.target.value)}
                  className="px-3 py-1.5 text-xs rounded-lg bg-linear-to-br from-indigo-600/20 to-purple-600/20 text-white border border-indigo-500/30 hover:border-indigo-500/50 hover:bg-linear-to-br hover:from-indigo-600/30 hover:to-purple-600/30 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 cursor-pointer font-medium shadow-lg shadow-indigo-500/10"
                  style={{
                    backgroundImage:
                      "linear-gradient(to bottom right, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2))",
                  }}
                >
                  <option value="beginner" className="bg-gray-900 text-white">
                    🌱 Beginner
                  </option>
                  <option value="medium" className="bg-gray-900 text-white">
                    ⚡ Medium
                  </option>
                  <option
                    value="interview_ready"
                    className="bg-gray-900 text-white"
                  >
                    🚀 Advanced
                  </option>
                </select>
              </div>

              {/* Language Selector */}
              <div className="flex items-center gap-2">
                {languages.map((lang) => (
                  <button
                    key={lang}
                    onClick={() => setLanguage(lang)}
                    className={`px-3 py-1 text-xs rounded-lg transition ${
                      language === lang
                        ? "bg-indigo-600 text-white"
                        : "bg-white/5 text-gray-300 hover:bg-white/10"
                    }`}
                  >
                    {lang.toUpperCase()}
                  </button>
                ))}
              </div>

              {/* Voice Explain Button - only show after successful execution */}
              {execution && (
                <VoiceExplainControls
                  execution={execution}
                  code={code}
                  stdin={stdin}
                  level={explanationLevel}
                />
              )}

              {/* Run Code Button */}
              <button
                onClick={handleRun}
                disabled={loading}
                className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold rounded-lg transition"
              >
                <Play size={16} />
                {loading ? "Running..." : "Run Code"}
              </button>
            </div>
          </div>

          <AnimatePresence mode="wait">
            {!execution || editorMode === "edit" ? (
              <motion.div
                key="initial"
                initial={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex-1 grid lg:grid-cols-2"
              >
                {/* Editor */}
                <div className="flex flex-col border-r border-white/10">
                  <div className="flex-1">
                    <Editor
                      height="100%"
                      theme="vs-dark"
                      language={language}
                      value={code}
                      onChange={(value) => setCode(value || "")}
                      options={{
                        fontSize: 14,
                        minimap: { enabled: false },
                        automaticLayout: true,
                      }}
                    />
                  </div>

                  {/* STDIN */}
                  <div className="border-t border-white/10 bg-black/20 p-3">
                    <label className="text-xs text-indigo-400 font-mono mb-2 block">
                      STDIN (Input)
                    </label>
                    <textarea
                      value={stdin}
                      onChange={(e) => setStdin(e.target.value)}
                      className="w-full h-20 resize-none rounded-lg bg-black/40 border border-white/10 p-2 text-sm text-white font-mono"
                    />
                  </div>
                </div>

                {/* Output Panel */}
                <div className="flex flex-col bg-black/20">
                  <div className="flex items-center justify-between px-3 py-2 border-b border-white/10">
                    <div className="flex items-center gap-2 text-indigo-400 text-sm font-semibold">
                      <Terminal size={16} />
                      {execution ? "Output" : "Ready to Execute"}
                    </div>
                  </div>

                  {!execution ? (
                    <div className="flex-1 p-4 font-mono text-sm overflow-auto">
                      <p className="text-gray-500">
                        Click Run Code to execute and see the trace
                        visualization.
                      </p>
                    </div>
                  ) : (
                    <div className="flex-1 flex flex-col overflow-hidden">
                      {/* Output Section */}
                      <div className="border-b border-white/10 p-3">
                        <div className="font-mono text-xs max-h-32 overflow-y-auto custom-scrollbar">
                          {execution.output && (
                            <pre className="text-green-400 whitespace-pre-wrap">
                              {execution.output}
                            </pre>
                          )}
                          {execution.error && (
                            <pre className="text-red-400 whitespace-pre-wrap">
                              {execution.error}
                            </pre>
                          )}
                          {!execution.output && !execution.error && (
                            <p className="text-gray-500">No output</p>
                          )}
                        </div>
                      </div>

                      {/* RAG Explanations */}
                      <div className="flex-1 flex flex-col border-b border-white/10 overflow-hidden">
                        <div className="flex items-center gap-2 px-3 py-2 border-b border-white/10 text-purple-400 text-sm font-semibold">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          >
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                          </svg>
                          Step Explanations
                        </div>
                        <div
                          className="flex-1 p-3 text-xs overflow-y-auto custom-scrollbar"
                          style={{ maxHeight: "400px" }}
                        >
                          {execution.rag_explanations &&
                          execution.rag_explanations.length > 0 ? (
                            <div className="space-y-2">
                              {execution.rag_explanations.map(
                                (explanation, idx) => (
                                  <div
                                    key={idx}
                                    className="p-2 bg-purple-500/10 border border-purple-500/20 rounded text-gray-300"
                                  >
                                    <span className="text-purple-400 font-semibold">
                                      Step {idx + 1}:{" "}
                                    </span>
                                    {explanation}
                                  </div>
                                ),
                              )}
                            </div>
                          ) : (
                            <p className="text-gray-500">
                              No AI explanations available
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="execution"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex-1 flex gap-0 overflow-hidden"
              >
                {/* Left: 4-panel grid */}
                <div className="flex-1 grid grid-cols-2 grid-rows-2 gap-0 h-full">
                  {/* Panel 1 (Top Left): Execution View */}
                  <div className="border-r border-b border-white/10 overflow-hidden flex flex-col">
                    <div className="px-3 py-2 border-b border-white/10 bg-black/20">
                      <h3 className="text-xs font-semibold text-gray-400">
                        Execution Trace
                      </h3>
                    </div>
                    <div className="flex-1 overflow-hidden">
                      <ExecutionView
                        code={code}
                        language={language}
                        currentLine={currentLine}
                      />
                    </div>
                  </div>

                  {/* Panel 2 (Top Right): Data Structure Visualizations */}
                  <div className="border-b border-white/10 flex flex-col overflow-hidden">
                    <div className="px-3 py-2 border-b border-white/10 bg-black/20">
                      <h3 className="text-xs font-semibold text-indigo-400">
                        Data Structures
                      </h3>
                    </div>
                    <div className="flex-1 overflow-auto custom-scrollbar">
                      <VisualizerDispatcher
                        variables={
                          tracePlayerRef.current?.current()?.variables || {}
                        }
                        changedVariables={tracePlayerRef.current?.getChangedVariables()}
                        showOnlyVisualizers={true}
                      />
                    </div>
                  </div>

                  {/* Panel 3 (Bottom Left): Variable Table & Timeline */}
                  <div className="border-r border-white/10 flex flex-col overflow-hidden">
                    <div className="px-3 py-2 border-b border-white/10 bg-black/20">
                      <h3 className="text-xs font-semibold text-gray-400">
                        Variables
                      </h3>
                    </div>
                    <div className="flex-1 overflow-auto custom-scrollbar p-4">
                      <table className="w-full text-sm text-left text-gray-400">
                        <thead>
                          <tr className="border-b border-white/10">
                            <th className="py-2 font-mono text-indigo-300">
                              Name
                            </th>
                            <th className="py-2 font-mono text-indigo-300">
                              Value
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(
                            tracePlayerRef.current?.current()?.variables || {},
                          ).map(([k, v]) => (
                            <tr key={k} className="border-b border-white/5">
                              <td className="py-2 font-mono text-indigo-300">
                                {k}
                              </td>
                              <td className="py-2 font-mono">
                                {typeof v === "object"
                                  ? JSON.stringify(v)
                                  : String(v)}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                    <TimelineControls
                      currentStep={currentStepIndex}
                      totalSteps={tracePlayerRef.current?.total() || 0}
                      isPlaying={isPlaying}
                      playbackSpeed={playbackSpeed}
                      onPlay={handlePlay}
                      onPause={handlePause}
                      onNext={handleNext}
                      onPrev={handlePrev}
                      onReset={handleReset}
                      onSliderChange={handleSliderChange}
                      onSpeedChange={setPlaybackSpeed}
                    />
                  </div>

                  {/* Panel 4 (Bottom Right): AI Analysis */}
                  <div className="overflow-auto custom-scrollbar">
                    <AIAnalysisPanel
                      structures={execution?.ai_analysis?.structures}
                      summary={execution?.ai_analysis?.summary}
                    />
                  </div>
                </div>

                {/* Right: Output and Controls */}
                <div className="w-96 border-l border-white/10 flex flex-col">
                  {/* STDIN */}
                  <div className="border-b border-white/10 bg-black/20 p-3">
                    <label className="text-xs text-indigo-400 font-mono mb-2 block">
                      STDIN (Input)
                    </label>
                    <textarea
                      value={stdin}
                      onChange={(e) => setStdin(e.target.value)}
                      className="w-full h-20 resize-none rounded-lg bg-black/40 border border-white/10 p-2 text-sm text-white font-mono"
                    />
                  </div>

                  {/* Output */}
                  <div className="h-48 flex flex-col border-b border-white/10">
                    <div className="flex items-center gap-2 px-3 py-2 border-b border-white/10 text-indigo-400 text-sm font-semibold">
                      <Terminal size={16} />
                      Output
                    </div>
                    <div className="flex-1 p-3 font-mono text-xs overflow-y-auto custom-scrollbar">
                      {execution?.output && (
                        <pre className="text-green-400 whitespace-pre-wrap">
                          {execution.output}
                        </pre>
                      )}
                      {execution?.error && (
                        <pre className="text-red-400 whitespace-pre-wrap">
                          {execution.error}
                        </pre>
                      )}
                      {!execution?.output && !execution?.error && (
                        <p className="text-gray-500">No output</p>
                      )}
                    </div>
                  </div>

                  {/* RAG Explanations */}
                  <div className="flex-1 flex flex-col border-b border-white/10">
                    <div className="flex items-center gap-2 px-3 py-2 border-b border-white/10 text-purple-400 text-sm font-semibold">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                      </svg>
                      Step Explanations
                    </div>
                    <div
                      className="flex-1 p-3 text-xs overflow-y-auto custom-scrollbar"
                      style={{ maxHeight: "300px" }}
                    >
                      {execution?.rag_explanations &&
                      execution.rag_explanations.length > 0 ? (
                        <div className="space-y-2">
                          {execution.rag_explanations.map(
                            (explanation, idx) => (
                              <div
                                key={idx}
                                className="p-2 bg-purple-500/10 border border-purple-500/20 rounded text-gray-300"
                              >
                                <span className="text-purple-400 font-semibold">
                                  Step {idx + 1}:{" "}
                                </span>
                                {explanation}
                              </div>
                            ),
                          )}
                        </div>
                      ) : (
                        <p className="text-gray-500">
                          Run code to see AI-powered step-by-step explanations
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
}
