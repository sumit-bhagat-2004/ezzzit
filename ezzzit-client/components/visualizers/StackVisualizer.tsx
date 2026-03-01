"use client";
import { motion, AnimatePresence } from "framer-motion";

export default function StackVisualizer({ data }: { data: any[] }) {
  // Python lists: append() adds to end. So index (length-1) is TOP.
  // We reverse the array for display so the "Top" is visually up.
  const reversedData = [...data].reverse();

  return (
    <div className="flex flex-col items-center h-full">
      <div className="text-xs text-gray-500 mb-2 font-mono uppercase tracking-widest">Top</div>
      
      {/* The Stack Container */}
      <div className="flex flex-col w-24 border-b-4 border-l-4 border-r-4 border-gray-600 rounded-b-xl p-2 bg-gray-900/50 gap-2 min-h-[150px]">
        <AnimatePresence>
          {reversedData.map((val, idx) => (
            <motion.div
              key={`${val}-${idx}`}
              initial={{ y: -50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ scale: 0, opacity: 0 }}
              className="w-full h-10 bg-indigo-600 rounded flex items-center justify-center text-white font-bold shadow-md border border-indigo-400"
            >
              {JSON.stringify(val)}
            </motion.div>
          ))}
        </AnimatePresence>
        
        {data.length === 0 && (
          <div className="text-gray-600 text-xs text-center py-4">Empty Stack</div>
        )}
      </div>
    </div>
  );
}
