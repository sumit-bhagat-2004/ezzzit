export interface TraceStep {
  step: number;
  line: number;
  function: string;
  event: string;
  call_stack_depth: number;
  variables: Record<string, unknown>;
}

export class TracePlayer {
  private trace: TraceStep[];
  private index: number = 0;

  constructor(trace: TraceStep[]) {
    this.trace = trace;
  }

  current(): TraceStep | null {
    return this.trace[this.index] || null;
  }

  next(): TraceStep | null {
    if (this.index < this.trace.length - 1) {
      this.index++;
    }
    return this.current();
  }

  prev(): TraceStep | null {
    if (this.index > 0) {
      this.index--;
    }
    return this.current();
  }

  go(step: number): TraceStep | null {
    if (step >= 0 && step < this.trace.length) {
      this.index = step;
    }
    return this.current();
  }

  getCurrentIndex(): number {
    return this.index;
  }

  total(): number {
    return this.trace.length;
  }

  reset(): void {
    this.index = 0;
  }

  isAtStart(): boolean {
    return this.index === 0;
  }

  isAtEnd(): boolean {
    return this.index === this.trace.length - 1;
  }

  getChangedVariables(): string[] {
    if (this.index === 0) return Object.keys(this.trace[0].variables);
    
    const prev = this.trace[this.index - 1].variables;
    const curr = this.trace[this.index].variables;
    const changed: string[] = [];

    for (const key in curr) {
      if (!(key in prev) || prev[key] !== curr[key]) {
        changed.push(key);
      }
    }

    return changed;
  }
}
