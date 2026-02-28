export default function MapVisualizer({ data }: { data: Record<string, unknown> }) {
  return (
    <div className="flex flex-col gap-2 w-full max-w-sm">
      {Object.entries(data).map(([key, val]) => (
        <div key={key} className="flex items-center gap-2 bg-gray-800 p-2 rounded border border-gray-700">
          {/* Key */}
          <div className="bg-yellow-600/20 text-yellow-400 px-2 py-1 rounded text-xs font-mono font-bold min-w-[30px] text-center border border-yellow-600/50">
            {key}
          </div>
          
          {/* Arrow */}
          <div className="text-gray-500">➜</div>
          
          {/* Value */}
          <div className="text-indigo-300 font-mono text-sm truncate">
            {JSON.stringify(val)}
          </div>
        </div>
      ))}
    </div>
  );
}
