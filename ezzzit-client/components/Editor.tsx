"use client";

import { useState } from "react";
import Editor from "@monaco-editor/react";
import { Play, Sparkles, Terminal } from "lucide-react";
import { motion } from "framer-motion";
import VoiceExplainControls from "./VoiceExplainControls";

type TraceStep = {
  step: number;
  line: number;
  function: string;
  event: string;
  call_stack_depth: number;
  variables: Record<string, any>;
};

type ExecutionResponse = {
  output: string;
  trace: TraceStep[];
  steps: number;
  exception: string | null;
  error: string | null;
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

  const languages = ["python", "javascript", "java"];

  const handleRun = async () => {
    try {
      setLoading(true);

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_CODE_EXECUTION_API_URL}/execute`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code, language, stdin }),
        },
      );

      const data: ExecutionResponse = await res.json();
      setExecution(data);
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
    <div className="relative w-full min-h-[calc(100vh-80px)] bg-[#030712] pt-16 pb-6 overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px]" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px]" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-indigo-400 text-xs font-semibold mb-6">
          <Sparkles size={14} />
          <span>AI Code Workspace</span>
        </div>

        {/* Main Card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative bg-[#0B0F1A]/80 border border-white/10 rounded-2xl shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden"
        >
          {/* Top Bar */}
          <div className="flex items-center justify-between px-5 py-3 border-b border-white/10 bg-white/[0.02]">
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

          <div className="grid lg:grid-cols-2">
            {/* Editor */}
            <div className="flex flex-col border-r border-white/10">
              <div className="h-[360px]">
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
            <div className="h-[460px] flex flex-col bg-black/20">
              <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
                <div className="flex items-center gap-2 text-indigo-400 text-sm font-semibold">
                  <Terminal size={16} />
                  Execution Output
                </div>
                <span className="text-[10px] text-white/50 font-bold">
                  {execution ? `${execution.steps} STEPS` : "TRACE + AI READY"}
                </span>
              </div>

              <div className="flex-1 p-4 font-mono text-sm overflow-auto">
                {!execution && (
                  <p className="text-gray-500">
                    Run your code to see output, trace and voice explanation.
                  </p>
                )}
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
              </div>

              {/* Action Bar */}
              <div className="flex items-center justify-between px-4 py-3 border-t border-white/10 bg-white/[0.02]">
                <VoiceExplainControls
                  execution={execution}
                  code={code}
                  stdin={stdin}
                />

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
          </div>
        </motion.div>
      </div>
    </div>
  );
}
