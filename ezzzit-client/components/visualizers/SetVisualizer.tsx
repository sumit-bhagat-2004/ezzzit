"use client";
import { motion } from "framer-motion";

export default function SetVisualizer({ data }: { data: any }) {
  const items = data.items || []; // Access the 'items' property from our custom Set serialization

  return (
    <div className="p-4 border border-dashed border-gray-600 rounded-xl bg-gray-900/30 flex flex-wrap gap-3 justify-center">
      {items.map((val: any, idx: number) => (
        <motion.div
          key={idx}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="w-12 h-12 rounded-full bg-pink-600 flex items-center justify-center text-white text-sm font-bold shadow-lg border border-pink-400"
        >
          {JSON.stringify(val)}
        </motion.div>
      ))}
      {items.length === 0 && <span className="text-gray-500 italic">Empty Set</span>}
    </div>
  );
}
