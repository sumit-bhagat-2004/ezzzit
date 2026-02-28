"use client";
import { motion, AnimatePresence } from "framer-motion";

interface DequeData {
  items?: unknown[];
}

export default function QueueVisualizer({ data }: { data: unknown[] | DequeData }) {
  // Handle both raw lists and our custom deque object
  const items = Array.isArray(data) ? data : ((data as DequeData).items || []);

  return (
    <div className="flex flex-col gap-1 w-full overflow-hidden">
      <div className="flex justify-between text-xs text-gray-500 px-2 font-mono">
        <span>FRONT (Out)</span>
        <span>REAR (In)</span>
      </div>

      <div className="flex items-center gap-2 p-3 bg-gray-900/50 border-y-2 border-gray-700 min-h-[80px] overflow-x-auto">
        <AnimatePresence mode="popLayout">
          {items.map((val: unknown, idx: number) => (
            <motion.div
              key={`${idx}-${JSON.stringify(val)}`}
              initial={{ x: 50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -50, opacity: 0 }}
              layout
              className="min-w-[50px] h-[50px] bg-emerald-600 rounded-full flex items-center justify-center text-white font-bold border-2 border-emerald-400 shadow-sm"
            >
              {JSON.stringify(val)}
            </motion.div>
          ))}
        </AnimatePresence>
        
        {items.length === 0 && (
          <div className="text-gray-600 text-xs w-full text-center">Empty Queue</div>
        )}
      </div>
    </div>
  );
}
