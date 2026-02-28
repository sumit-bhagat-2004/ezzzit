"use client";

interface DataStructure {
  name: string;
  type: string;
  variables: string[];
  description: string;
}

interface AIAnalysisProps {
  structures?: DataStructure[];
  summary?: string;
}

export default function AIAnalysisPanel({ structures, summary }: AIAnalysisProps) {
  if (!structures || !summary) {
    return (
      <div className="h-full flex items-center justify-center bg-black/20 p-4">
        <div className="text-center text-gray-500">
          <p className="text-sm">AI Analysis</p>
          <p className="text-xs mt-2">Run code to see data structures</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-black/20 overflow-hidden">
      {/* Header */}
      <div className="px-3 py-2 border-b border-white/10 bg-white/5">
        <h3 className="text-sm font-semibold text-indigo-400">AI Analysis</h3>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-3 space-y-3">
        {/* Summary */}
        <div className="bg-indigo-600/10 border border-indigo-600/20 rounded-lg p-3">
          <div className="text-xs font-semibold text-indigo-400 mb-1">Algorithm Summary</div>
          <p className="text-xs text-gray-300 leading-relaxed">{summary}</p>
        </div>

        {/* Data Structures */}
        <div>
          <div className="text-xs font-semibold text-gray-400 mb-2">Data Structures</div>
          <div className="space-y-2">
            {structures.map((structure, idx) => (
              <div
                key={idx}
                className="bg-white/5 border border-white/10 rounded-lg p-2 hover:bg-white/10 transition"
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-semibold text-white">{structure.name}</span>
                  <span className="text-[10px] px-1.5 py-0.5 bg-indigo-600/20 text-indigo-400 rounded">
                    {structure.type}
                  </span>
                </div>
                <p className="text-[11px] text-gray-400 mb-1.5">{structure.description}</p>
                <div className="flex flex-wrap gap-1">
                  {structure.variables.map((variable, vIdx) => (
                    <span
                      key={vIdx}
                      className="text-[10px] px-1.5 py-0.5 bg-black/40 text-gray-300 rounded font-mono"
                    >
                      {variable}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
