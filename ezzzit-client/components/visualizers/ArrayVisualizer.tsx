"use client";
import { motion } from "framer-motion";

export default function ArrayVisualizer({ data, pointers }: { data: any[], pointers: Record<string, number> }) {
  return (
    <div className="flex gap-2 p-4 overflow-x-auto items-end h-24">
      {data.map((val, idx) => (
        <div key={idx} className="flex flex-col items-center gap-1 min-w-[3rem]">
          {/* Pointer Arrows (i, j, etc.) */}
          <div className="h-6 relative w-full flex justify-center">
            {Object.entries(pointers).map(([varName, varVal]) => 
              varVal === idx && (
                <motion.div 
                  layoutId={`pointer-${varName}`}
                  key={varName}
                  className="absolute bottom-0 text-xs font-bold text-yellow-400 flex flex-col items-center"
                >
                  <span>{varName}</span>
                  <span>↓</span>
                </motion.div>
              )
            )}
          </div>

          {/* The Array Box */}
          <motion.div 
            layout
            className="w-12 h-12 flex items-center justify-center bg-gray-800 border-2 border-indigo-500/50 rounded text-white font-mono shadow-lg"
          >
            {JSON.stringify(val)}
          </motion.div>
          
          {/* Index Label */}
          <span className="text-[10px] text-gray-500 font-mono">{idx}</span>
        </div>
      ))}
    </div>
  );
}
