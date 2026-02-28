"use client";
import { detectType } from "@/lib/dataTypeDetector";
import ArrayVisualizer from "./visualizers/ArrayVisualizer";
import MatrixVisualizer from "./visualizers/MatrixVisualizer";
import GraphVisualizer from "./visualizers/GraphVisualizer";
import StackVisualizer from "./visualizers/StackVisualizer";
import QueueVisualizer from "./visualizers/QueueVisualizer";
import SetVisualizer from "./visualizers/SetVisualizer";
import MapVisualizer from "./visualizers/MapVisualizer";

interface Props {
  variables: Record<string, unknown>;
}

export default function VisualizerDispatcher({ variables }: Props) {
  // 1. Identify "Pointer" variables (integers usually named i, j, k, low, high)
  const pointers: Record<string, number> = {};
  Object.entries(variables).forEach(([k, v]) => {
    if (typeof v === 'number' && ['i', 'j', 'k', 'low', 'high', 'mid', 'top', 'rear', 'front'].includes(k.toLowerCase())) {
      pointers[k] = v;
    }
  });

  return (
    <div className="flex flex-col gap-8 p-4 h-full overflow-y-auto">
      {Object.entries(variables).map(([name, value]) => {
        // Pass the variable name to detectType for heuristics
        const type = detectType(value, name);
        
        // Skip primitives in the "Big View" (keep them in a small sidebar table if you want)
        if (type === 'VALUE') return null; 

        return (
          <div key={name} className="flex flex-col gap-2 animate-in fade-in duration-300">
             <div className="flex justify-between items-center text-xs uppercase text-gray-400 font-bold tracking-wider">
               <span>{name}</span>
               <span className="bg-gray-800 px-2 py-0.5 rounded text-indigo-400 text-[10px]">{type}</span>
             </div>
             
             <div className="bg-[#0f111a] rounded-xl p-4 border border-white/5 shadow-inner">
                {type === 'STACK' && <StackVisualizer data={value as unknown[]} />}
                {type === 'QUEUE' && <QueueVisualizer data={value as unknown[] | { items?: unknown[] }} />}
                {type === 'SET' && <SetVisualizer data={value} />}
                {type === 'MAP' && <MapVisualizer data={value as Record<string, unknown>} />}
                {type === 'ARRAY' && <ArrayVisualizer data={value as unknown[]} pointers={pointers} />}
                {type === 'MATRIX' && <MatrixVisualizer data={value as unknown[][]} />}
                {(type === 'TREE' || type === 'LINKED_LIST') && <GraphVisualizer data={value} />}
                {type === 'OBJECT' && <pre className="text-xs text-gray-400">{JSON.stringify(value, null, 2)}</pre>}
             </div>
          </div>
        );
      })}
      
      {/* Fallback Table for Primitives */}
      <div className="mt-4">
        <h3 className="text-xs uppercase text-gray-500 font-semibold mb-2">Primitive Scope</h3>
        <table className="w-full text-sm text-left text-gray-400">
            <tbody>
            {Object.entries(variables).map(([k, v]) => 
                detectType(v, k) === 'VALUE' ? (
                <tr key={k} className="border-b border-white/5">
                    <td className="py-1 font-mono text-indigo-300">{k}</td>
                    <td className="py-1 font-mono">{String(v)}</td>
                </tr>
                ) : null
            )}
            </tbody>
        </table>
      </div>
    </div>
  );
}
