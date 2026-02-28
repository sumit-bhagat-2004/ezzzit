import { motion } from "framer-motion";
import { Play, Mic, Sparkles, ChevronRight } from "lucide-react";

const Hero = () => {
  return (
    <div className="relative min-h-screen bg-[#030712] flex items-center pt-20 overflow-hidden">
      {/* Background Radial Glows */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px]" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px]" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid lg:grid-cols-2 gap-12 items-center relative z-10">
        {/* Left Content */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-indigo-400 text-xs font-semibold mb-6">
            <Sparkles size={14} />
            <span>AI-Powered DSA Learning</span>
          </div>

          <h1 className="text-5xl lg:text-7xl font-extrabold text-white leading-tight mb-6">
            Watch your{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
              code come to life.
            </span>
          </h1>

          <p className="text-gray-400 text-lg mb-10 max-w-lg leading-relaxed">
            Paste your algorithms and see them move. Trace logic step-by-step
            and talk to our AI agent powered by ElevenLabs for real-time
            guidance.
          </p>

          <div className="flex flex-wrap gap-4">
            <button className="flex items-center gap-2 px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(79,70,229,0.4)]">
              Start Visualizing <ChevronRight size={18} />
            </button>
            <button className="flex items-center gap-2 px-8 py-4 bg-white/5 hover:bg-white/10 text-white font-bold rounded-xl border border-white/10 transition-all">
              <Play size={18} className="fill-current" /> Watch Demo
            </button>
          </div>
        </motion.div>

        {/* Right 3D/Visual Section */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="relative"
        >
          {/* Main "3D" Terminal Card */}
          <div className="relative z-20 bg-[#0B0F1A] border border-white/10 rounded-2xl p-6 shadow-2xl shadow-indigo-500/10 backdrop-blur-sm transform rotate-3 hover:rotate-0 transition-transform duration-500">
            <div className="flex gap-1.5 mb-4">
              <div className="w-3 h-3 rounded-full bg-red-500/50" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
              <div className="w-3 h-3 rounded-full bg-green-500/50" />
            </div>
            <pre className="font-mono text-sm text-indigo-300">
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
            className="absolute -top-10 -right-4 z-30 bg-gradient-to-br from-indigo-500 to-purple-600 p-4 rounded-2xl shadow-xl flex items-center gap-3 border border-white/20"
          >
            <div className="w-10 h-10 bg-black/20 rounded-full flex items-center justify-center animate-pulse">
              <Mic size={20} className="text-white" />
            </div>
            <div>
              <p className="text-[10px] uppercase tracking-widest text-white/70 font-bold">
                ElevenLabs AI
              </p>
              <p className="text-sm text-white font-medium italic">
                "Explaining step 4..."
              </p>
            </div>
          </motion.div>

          {/* Decorative 3D Elements */}
          <div className="absolute -bottom-12 -left-12 w-48 h-48 bg-indigo-500/20 rounded-full mix-blend-screen filter blur-3xl opacity-50" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] border border-white/5 rounded-full rotate-45 pointer-events-none" />
        </motion.div>
      </div>
    </div>
  );
};

export default Hero;
