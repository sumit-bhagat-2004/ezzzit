export default function MatrixVisualizer({ data }: { data: any[][] }) {
  return (
    <div className="flex flex-col gap-1 p-2 overflow-auto">
      {data.map((row, rIdx) => (
        <div key={rIdx} className="flex gap-1">
          {row.map((col, cIdx) => (
            <div 
              key={`${rIdx}-${cIdx}`}
              className="w-10 h-10 flex items-center justify-center bg-gray-900 border border-gray-700 text-sm font-mono text-gray-300"
            >
              {JSON.stringify(col)}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
