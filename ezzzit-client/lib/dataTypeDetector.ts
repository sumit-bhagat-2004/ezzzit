export type VisualizationType = 'MATRIX' | 'ARRAY' | 'TREE' | 'LINKED_LIST' | 'VALUE' | 'OBJECT' | 'STACK' | 'QUEUE' | 'SET' | 'MAP';

export function detectType(value: any, varName: string = ''): VisualizationType {
  const name = varName.toLowerCase();

  // 1. Explicit Type Tags (from Backend)
  if (value && typeof value === 'object') {
    if (value.__type__ === 'set') return 'SET';
    if (value.__type__ === 'deque') return 'QUEUE';
  }

  // 2. Arrays (Heuristics for Stack/Queue vs Matrix)
  if (Array.isArray(value)) {
    // Matrix
    if (value.length > 0 && Array.isArray(value[0])) return 'MATRIX';

    // Heuristics based on variable name
    if (name.includes('stack') || name.includes('stk')) return 'STACK';
    if (name.includes('queue') || name === 'q') return 'QUEUE';
    if (name.includes('heap') || name.includes('pq')) return 'TREE'; // Visualize heaps as trees ideally

    return 'ARRAY';
  }

  // 3. Objects (Maps vs Trees)
  if (typeof value === 'object' && value !== null) {
    const keys = Object.keys(value);
    
    // Recursive Data Structures
    if (keys.includes('val') && (keys.includes('next'))) return 'LINKED_LIST';
    if (keys.includes('val') && (keys.includes('left') || keys.includes('right'))) return 'TREE';
    
    // Python Dictionaries often imply Maps
    if (keys.length > 0 && !keys.includes('__type__')) return 'MAP';
    
    return 'OBJECT';
  }

  return 'VALUE';
}
