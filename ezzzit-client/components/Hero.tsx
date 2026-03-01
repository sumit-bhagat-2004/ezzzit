"use client";

import { useUser } from "@auth0/nextjs-auth0";
import { motion } from "framer-motion";
import { Play, Mic, Sparkles, ChevronRight } from "lucide-react";
import Link from "next/link";

const Hero = () => {
  const { user } = useUser();

  return (
    <div className="relative min-h-[calc(100vh-5rem)] bg-[#030712] flex items-center py-8 sm:py-12 md:py-16 overflow-hidden">
      {/* Background Radial Glows */}
      <div className="absolute top-0 left-1/4 w-64 h-64 sm:w-80 sm:h-80 md:w-96 md:h-96 bg-indigo-600/20 rounded-full blur-[100px] sm:blur-[120px]" />
      <div className="absolute bottom-0 right-1/4 w-64 h-64 sm:w-80 sm:h-80 md:w-96 md:h-96 bg-purple-600/10 rounded-full blur-[100px] sm:blur-[120px]" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 lg:grid-cols-2 gap-8 md:gap-10 lg:gap-12 items-center relative z-10">
        {/* Left Content */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center lg:text-left"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-indigo-400 text-xs font-semibold mb-4 sm:mb-6">
            <Sparkles size={14} />
            <span>AI-Powered DSA Learning</span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-white leading-tight mb-4 sm:mb-6">
            Watch your{" "}
            <span className="text-transparent bg-clip-text bg-linear-to-r from-indigo-400 to-purple-400">
              code come to life.
            </span>
          </h1>

          <p className="text-gray-400 text-base sm:text-lg mb-8 sm:mb-10 max-w-lg mx-auto lg:mx-0 leading-relaxed">
            Paste your algorithms and see them move. Trace logic step-by-step
            and talk to our AI agent powered by ElevenLabs for real-time
            guidance.
          </p>

          <div className="flex flex-col sm:flex-row flex-wrap gap-3 sm:gap-4 justify-center lg:justify-start">
            <button className="flex items-center justify-center gap-2 px-6 sm:px-8 py-3 sm:py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(79,70,229,0.4)]">
              <Link
                href={user ? "/editor" : "/auth/login"}
                className="flex items-center gap-2"
              >
                Start Visualizing
              </Link>
              <ChevronRight size={18} />
            </button>
            <button className="flex items-center justify-center gap-2 px-6 sm:px-8 py-3 sm:py-4 bg-white/5 hover:bg-white/10 text-white font-bold rounded-xl border border-white/10 transition-all">
              <Play size={18} className="fill-current" /> Watch Demo
            </button>
          </div>
        </motion.div>

        {/* Right 3D/Visual Section */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="relative mt-8 lg:mt-0 px-4 sm:px-8 lg:px-0"
        >
          {/* Main "3D" Terminal Card */}
          <div className="relative z-20 bg-[#0B0F1A] border border-white/10 rounded-xl sm:rounded-2xl p-4 sm:p-6 shadow-2xl shadow-indigo-500/10 backdrop-blur-sm transform rotate-2 sm:rotate-3 hover:rotate-0 transition-transform duration-500">
            <div className="flex gap-1.5 mb-3 sm:mb-4">
              <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-500/50" />
              <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-yellow-500/50" />
              <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-green-500/50" />
            </div>
            <pre className="font-mono text-xs sm:text-sm text-indigo-300 overflow-x-auto">
              <code>{`function bubbleSort(arr) {
  for (let i = 0; i < arr.length; i++) {
    // AI: "Notice how the largest
    // element bubbles to the top"
    if (arr[j] > arr[j + 1]) {
       [arr[j], arr[j+1]] = [arr[j+1], arr[j]]
    }
  }
}`}</code>
            </pre>
          </div>

          {/* Floating AI Agent UI */}
          <motion.div
            animate={{ y: [0, -15, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
            className="absolute -top-6 sm:-top-10 right-0 sm:-right-4 z-30 bg-linear-to-br from-indigo-500 to-purple-600 p-3 sm:p-4 rounded-xl sm:rounded-2xl shadow-xl flex items-center gap-2 sm:gap-3 border border-white/20 max-w-50 sm:max-w-none"
          >
            <div className="w-8 h-8 sm:w-10 sm:h-10 bg-black/20 rounded-full flex items-center justify-center animate-pulse shrink-0">
              <Mic size={16} className="sm:w-5 sm:h-5 text-white" />
            </div>
            <div className="min-w-0">
              <p className="text-[9px] sm:text-[10px] uppercase tracking-widest text-white/70 font-bold truncate">
                ElevenLabs AI
              </p>
              <p className="text-xs sm:text-sm text-white font-medium italic truncate">
                "Explaining step 4..."
              </p>
            </div>
          </motion.div>

          {/* Decorative 3D Elements */}
          <div className="absolute -bottom-8 sm:-bottom-12 -left-8 sm:-left-12 w-32 h-32 sm:w-48 sm:h-48 bg-indigo-500/20 rounded-full mix-blend-screen filter blur-2xl sm:blur-3xl opacity-50" />
          <div className="hidden md:block absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] border border-white/5 rounded-full rotate-45 pointer-events-none" />
        </motion.div>
      </div>
    </div>
  );
};

export default Hero;
