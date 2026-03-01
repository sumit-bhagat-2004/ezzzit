"use client";
import { useEffect, useRef } from "react";
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
  changedVariables?: string[];
  showOnlyVisualizers?: boolean;
}

export default function VisualizerDispatcher({ variables, changedVariables, showOnlyVisualizers = false }: Props) {
  const variableRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const containerRef = useRef<HTMLDivElement | null>(null);
  const previousVariablesRef = useRef<Record<string, unknown>>({});
  
  // Convert array to Set for efficient lookups
  const changedSet = changedVariables ? new Set(changedVariables) : new Set<string>();

  // Auto-scroll to changed variables
  useEffect(() => {
    if (!changedVariables || changedVariables.length === 0) return;

    // Find the last changed variable that has a visualizer (scroll to bottom-most change)
    const changedVisualizerVars = changedVariables.filter(
      varName => detectType(variables[varName], varName) !== 'VALUE'
    );

    if (changedVisualizerVars.length > 0) {
      // Get the last changed variable to scroll down
      const targetVar = changedVisualizerVars[changedVisualizerVars.length - 1];
      
      // Use setTimeout to ensure DOM is fully updated
      setTimeout(() => {
        const element = variableRefs.current[targetVar];
        
        if (element) {
          element.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'nearest'
          });
        }
      }, 100);
    }

    previousVariablesRef.current = { ...variables };
  }, [changedVariables, variables]);

  // 1. Identify "Pointer" variables (integers usually named i, j, k, low, high)
  const pointers: Record<string, number> = {};
  Object.entries(variables).forEach(([k, v]) => {
    if (typeof v === 'number' && ['i', 'j', 'k', 'low', 'high', 'mid', 'top', 'rear', 'front'].includes(k.toLowerCase())) {
      pointers[k] = v;
    }
  });

  return (
    <div ref={containerRef} className="flex flex-col gap-8 p-4 h-full overflow-y-auto">
      {Object.entries(variables).map(([name, value]) => {
        // Pass the variable name to detectType for heuristics
        const type = detectType(value, name);
        
        // Skip primitives in the "Big View" (keep them in a small sidebar table if you want)
        if (type === 'VALUE') return null; 

        const isChanged = changedSet.has(name);

        return (
          <div 
            key={name} 
            ref={(el) => { variableRefs.current[name] = el; }}
            className={`flex flex-col gap-2 animate-in fade-in duration-300 ${
              isChanged ? 'ring-2 ring-indigo-500/50 rounded-xl' : ''
            }`}
          >
             <div className="flex justify-between items-center text-xs uppercase text-gray-400 font-bold tracking-wider">
               <span className={isChanged ? 'text-indigo-400' : ''}>{name}</span>
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
      
      {/* Fallback Table for Primitives - only show if not in visualizer-only mode */}
      {!showOnlyVisualizers && (
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
      )}
    </div>
  );
}
