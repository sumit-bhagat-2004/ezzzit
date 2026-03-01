"use client";

import { useEffect, useRef } from "react";
import Editor from "@monaco-editor/react";
import type * as monacoEditor from "monaco-editor";

interface ExecutionViewProps {
  code: string;
  language: string;
  currentLine: number | null;
}

export default function ExecutionView({
  code,
  language,
  currentLine,
}: ExecutionViewProps) {
  const editorRef = useRef<monacoEditor.editor.IStandaloneCodeEditor | null>(
    null,
  );
  const decorationsRef = useRef<string[]>([]);

  useEffect(() => {
    if (!editorRef.current || currentLine === null) return;

    const editor = editorRef.current;

    // Clear previous decorations
    decorationsRef.current = editor.deltaDecorations(
      decorationsRef.current,
      [],
    );

    // Add new decoration for current line
    decorationsRef.current = editor.deltaDecorations(
      [],
      [
        {
          range: {
            startLineNumber: currentLine,
            startColumn: 1,
            endLineNumber: currentLine,
            endColumn: 1,
          },
          options: {
            isWholeLine: true,
            className: "executionLineHighlight",
            glyphMarginClassName: "executionLineGlyph",
          },
        },
      ],
    );

    // Scroll to current line
    editor.revealLineInCenter(currentLine);
  }, [currentLine]);

  const handleEditorDidMount = (
    editor: monacoEditor.editor.IStandaloneCodeEditor,
  ) => {
    editorRef.current = editor;

    // Add custom CSS for line highlighting
    const style = document.createElement("style");
    style.innerHTML = `
      .executionLineHighlight {
        background: rgba(255, 200, 0, 0.25) !important;
        border-left: 3px solid rgba(255, 200, 0, 0.8) !important;
      }
      .executionLineGlyph {
        background: rgba(255, 200, 0, 0.8) !important;
        width: 5px !important;
        margin-left: 3px;
      }
    `;
    document.head.appendChild(style);
  };

  return (
    <div className="h-full flex flex-col">
      <div className="px-3 py-2 bg-black/30 border-b border-white/10">
        <div className="flex items-center gap-2 text-xs">
          <div className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse" />
          <span className="text-indigo-400 font-semibold">Execution View</span>
          {currentLine !== null && (
            <span className="ml-auto text-gray-500 font-mono">
              Line {currentLine}
            </span>
          )}
        </div>
      </div>
      <div className="flex-1">
        <Editor
          height="100%"
          theme="vs-dark"
          language={language === "cpp" ? "cpp" : language}
          value={code}
          onMount={handleEditorDidMount}
          options={{
            fontSize: 13,
            readOnly: true,
            minimap: { enabled: false },
            smoothScrolling: true,
            padding: { top: 8 },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            lineNumbers: "on",
            glyphMargin: true,
            folding: false,
            scrollbar: {
              vertical: "visible",
              horizontal: "visible",
            },
          }}
        />
      </div>
    </div>
  );
}
