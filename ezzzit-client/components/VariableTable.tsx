"use client";

interface VariableTableProps {
  variables: Record<string, unknown>;
  changedKeys: string[];
}

export default function VariableTable({ variables, changedKeys }: VariableTableProps) {
  const entries = Object.entries(variables);

  if (entries.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500 text-sm">
        No variables yet
      </div>
    );
  }

  return (
    <div className="h-full overflow-auto">
      <table className="w-full text-sm">
        <thead className="sticky top-0 bg-[#0B0F1A] border-b border-white/10">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-semibold text-indigo-400 uppercase tracking-wider">
              Variable
            </th>
            <th className="px-4 py-2 text-left text-xs font-semibold text-indigo-400 uppercase tracking-wider">
              Value
            </th>
          </tr>
        </thead>
        <tbody>
          {entries.map(([key, value]) => {
            const isChanged = changedKeys.includes(key);
            return (
              <tr
                key={key}
                className={`border-b border-white/5 transition-colors ${
                  isChanged
                    ? "bg-yellow-500/10 animate-pulse"
                    : "hover:bg-white/5"
                }`}
              >
                <td className="px-4 py-2 font-mono text-gray-300">
                  {key}
                </td>
                <td className={`px-4 py-2 font-mono ${
                  isChanged ? "text-yellow-400 font-bold" : "text-gray-400"
                }`}>
                  {JSON.stringify(value)}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
