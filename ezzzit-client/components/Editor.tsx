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
  const [execution, setExecution] = useState<ExecutionResponse | null>(null);
  const [currentLine, setCurrentLine] = useState<number | null>(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
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

  const handlePlay = () => {
    if (!tracePlayerRef.current) return;
    setIsPlaying(true);
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
    }, 600);
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

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/execute`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code, language, stdin }),
        },
      );

      const data: ExecutionResponse = await res.json();
      setExecution(data);
      // Reset current line when new execution starts
      if (data.trace && data.trace.length > 0) {
        tracePlayerRef.current = new TracePlayer(data.trace);
        setCurrentLine(data.trace[0].line);
        setCurrentStepIndex(0);
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
            <span className="text-xs text-gray-400 font-mono">
              main.{language === "python" ? "py" : "js"}
            </span>

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
          </div>

          <AnimatePresence mode="wait">
            {!execution ? (
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
                      Ready to Execute
                    </div>
                  </div>

                  <div className="flex-1 p-4 font-mono text-sm overflow-auto">
                    <p className="text-gray-500">
                      Click Run Code to execute and see the trace visualization.
                    </p>
                  </div>

                  {/* Action Bar */}
                  <div className="flex items-center justify-between px-3 py-2 border-t border-white/10 bg-white/2">
                    <div />
                    <button
                      onClick={handleRun}
                      disabled={loading}
                      className="flex items-center gap-2 px-6 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-semibold rounded-xl transition"
                    >
                      <Play size={16} />
                      {loading ? "Running..." : "Run Code"}
                    </button>
                  </div>
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
              {/* Top Left: Original Editor */}
              <div className="border-r border-b border-white/10 overflow-hidden">
                <div className="h-full">
                  <Editor
                    height="100%"
                    theme="vs-dark"
                    language={language}
                    value={code}
                    onChange={(value) => setCode(value || "")}
                    options={{
                      fontSize: 13,
                      minimap: { enabled: false },
                      automaticLayout: true,
                      scrollBeyondLastLine: false,
                    }}
                  />
                </div>
              </div>

              {/* Top Right: Execution View */}
              <div className="border-b border-white/10 overflow-hidden">
                <ExecutionView
                  code={code}
                  language={language}
                  currentLine={currentLine}
                />
              </div>

              {/* Bottom Left: Variables & Timeline */}
              <div className="border-r border-white/10 flex flex-col overflow-hidden">
                <div className="flex-1 overflow-auto">
                  <VisualizerDispatcher
                    variables={tracePlayerRef.current?.current()?.variables || {}}
                  />
                </div>
                <TimelineControls
                  currentStep={currentStepIndex}
                  totalSteps={tracePlayerRef.current?.total() || 0}
                  isPlaying={isPlaying}
                  onPlay={handlePlay}
                  onPause={handlePause}
                  onNext={handleNext}
                  onPrev={handlePrev}
                  onReset={handleReset}
                  onSliderChange={handleSliderChange}
                />
              </div>

              {/* Bottom Right: AI Analysis */}
              <div className="overflow-auto">
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
              <div className="flex-1 flex flex-col border-b border-white/10">
                <div className="flex items-center gap-2 px-3 py-2 border-b border-white/10 text-indigo-400 text-sm font-semibold">
                  <Terminal size={16} />
                  Output
                </div>
                <div className="flex-1 p-3 font-mono text-xs overflow-auto">
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

              {/* Action Bar */}
              <div className="flex flex-col gap-2 p-3 bg-white/2">
                <VoiceExplainControls
                  execution={execution}
                  code={code}
                  stdin={stdin}
                />
                <button
                  onClick={handleRun}
                  disabled={loading}
                  className="flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-semibold rounded-lg transition"
                >
                  <Play size={16} />
                  {loading ? "Running..." : "Run Code"}
                </button>
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
