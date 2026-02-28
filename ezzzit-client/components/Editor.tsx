"use client";

import { useState } from "react";
import Editor from "@monaco-editor/react";
import { Play, Mic, Sparkles, Terminal } from "lucide-react";
import { motion } from "framer-motion";

export default function EditorUI() {
  const [language, setLanguage] = useState("javascript");
  const [code, setCode] = useState(`// Watch your code come to life ✨

def bubble_sort(arr):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
`);

  const languages = ["python", "javascript", "java"];

  return (
    <div className="relative w-full min-h-[calc(100vh-80px)] bg-[#030712] pt-16 pb-6 overflow-hidden">
      {/* Background Glows (Same as Hero) */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px]" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px]" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-indigo-400 text-xs font-semibold mb-6">
          <Sparkles size={14} />
          <span>AI Code Workspace</span>
        </div>

        {/* Main Editor Card (Glassmorphism like Hero terminal) */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="relative bg-[#0B0F1A]/80 border border-white/10 rounded-2xl shadow-2xl shadow-indigo-500/10 backdrop-blur-xl overflow-hidden"
        >
          {/* Top Bar (Mac style + controls) */}
          <div className="flex items-center justify-between px-5 py-3 border-b border-white/10 bg-white/[0.02]">
            <div className="flex items-center gap-4">
              {/* Window Dots */}
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/50" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                <div className="w-3 h-3 rounded-full bg-green-500/50" />
              </div>

              {/* File Name */}
              <span className="text-xs text-gray-400 font-mono">
                main.
                {language === "python"
                  ? "py"
                  : language === "cpp"
                    ? "cpp"
                    : "js"}
              </span>
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
          </div>

          {/* Editor + Output Layout (NOT full screen) */}
          <div className="grid lg:grid-cols-2">
            {/* Monaco Editor */}
            <div className="h-[420px] border-r border-white/10">
              <Editor
                height="100%"
                theme="vs-dark"
                language={language === "cpp" ? "cpp" : language}
                value={code}
                onChange={(value) => setCode(value || "")}
                options={{
                  fontSize: 14,
                  minimap: { enabled: false },
                  smoothScrolling: true,
                  padding: { top: 16 },
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                }}
              />
            </div>

            {/* Output Panel (Hero Terminal Style) */}
            <div className="h-[420px] flex flex-col bg-black/20">
              {/* Output Header */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-white/10 bg-white/[0.02]">
                <div className="flex items-center gap-2 text-indigo-400 text-sm font-semibold">
                  <Terminal size={16} />
                  Execution Output
                </div>
                <span className="text-[10px] uppercase tracking-widest text-white/50 font-bold">
                  TRACE + AI READY
                </span>
              </div>

              {/* Output Content */}
              <div className="flex-1 p-4 font-mono text-sm text-indigo-300 overflow-auto">
                <p className="text-gray-500">Run your code to see:</p>
                <ul className="mt-3 space-y-2 text-gray-400 text-xs">
                  <li>• Program output</li>
                  <li>• Step-by-step execution trace</li>
                  <li>• AI voice explanation (ElevenLabs)</li>
                </ul>
              </div>

              {/* Action Bar */}
              <div className="flex items-center justify-between px-4 py-3 border-t border-white/10 bg-white/[0.02]">
                <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 text-white text-sm rounded-xl border border-white/10 transition">
                  <Mic size={16} />
                  Voice Explain
                </button>

                <button className="flex items-center gap-2 px-6 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(79,70,229,0.4)]">
                  <Play size={16} />
                  Run Code
                </button>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Subtle Glow Ring (matches hero aesthetic) */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[110%] h-[110%] border border-white/5 rounded-full rotate-12 pointer-events-none" />
      </div>
    </div>
  );
}
