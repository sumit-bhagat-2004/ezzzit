"use client";

import { useState } from "react";
import { useConversation } from "@elevenlabs/react";
import { Mic, MicOff, Loader2 } from "lucide-react";

type TraceStep = {
  step: number;
  line: number;
  function: string;
  event: string;
  call_stack_depth: number;
  variables: Record<string, any>;
};

type ExecutionResponse = {
  output: string;
  trace: TraceStep[];
  steps: number;
  exception: string | null;
  error: string | null;
};

type VoiceExplainControlsProps = {
  execution: ExecutionResponse | null;
  code: string;
  stdin: string;
  level: string;
};

export default function VoiceExplainControls({
  execution,
  code,
  stdin,
  level,
}: VoiceExplainControlsProps) {
  const [voiceLoading, setVoiceLoading] = useState(false);

  const conversation = useConversation({
    onConnect: () => {
      console.log("Voice agent connected");
      setVoiceLoading(false);
    },
    onDisconnect: () => {
      console.log("Voice agent disconnected");
    },
    onError: (err) => {
      console.error("Voice agent error:", err);
      setVoiceLoading(false);
    },
  });

  const handleVoiceExplain = async () => {
    if (!execution) {
      alert("Run the code first!");
      return;
    }

    try {
      setVoiceLoading(true);

      // Request microphone permission
      await navigator.mediaDevices.getUserMedia({ audio: true });

      // Start session
      await conversation.startSession({
        agentId: process.env.NEXT_PUBLIC_ELEVENLABS_AGENT_ID!,
        connectionType: "webrtc",
        userId: "editor-user",
      });

      // Send structured context
      await conversation.sendContextualUpdate(`
You are inside a code execution visualizer IDE.

Here is the program context:

EXPLANATION LEVEL: ${level}
(beginner = simple terms, medium = standard explanation, interview_ready = advanced concepts)

CODE:
${code}

STDIN:
${stdin || "None"}

OUTPUT:
${execution.output}

TOTAL STEPS:
${execution.steps}

EXECUTION TRACE (JSON):
${JSON.stringify(execution.trace, null, 2)}

ERROR:
${execution.error ?? "None"}

EXCEPTION:
${execution.exception ?? "None"}
`);

      // Trigger the agent with a prompt
      await conversation.sendUserMessage(
        `Explain this program's behavior step by step using the execution trace at ${level} level. Do not explain syntax.`,
      );
    } catch (err) {
      console.error("Voice session failed:", err);
      setVoiceLoading(false);
    }
  };

  const handleReExplain = async () => {
    if (!execution) return;
    await conversation.endSession();
    // Small delay to let the session close cleanly
    await new Promise((r) => setTimeout(r, 300));
    await handleVoiceExplain();
  };

  const stopVoice = async () => {
    await conversation.endSession();
  };

  const isVoiceActive = conversation.status === "connected";

  return (
    <div className="flex items-center gap-2">
      {!isVoiceActive ? (
        <button
          onClick={handleVoiceExplain}
          disabled={voiceLoading || !execution}
          className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 disabled:opacity-40 text-white text-sm rounded-xl border border-white/10 transition"
        >
          {voiceLoading ? (
            <Loader2 size={16} className="animate-spin" />
          ) : (
            <Mic size={16} />
          )}
          {voiceLoading ? "Connecting..." : "Voice Explain"}
        </button>
      ) : (
        <>
          <button
            onClick={stopVoice}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-500 text-white text-sm rounded-xl transition"
          >
            <MicOff size={16} />
            End Voice
          </button>
          <button
            onClick={handleReExplain}
            disabled={!execution}
            className="flex items-center gap-2 px-3 py-2 bg-white/5 hover:bg-white/10 text-white text-sm rounded-xl border border-white/10 transition"
            title="Re-launch with latest execution data"
          >
            <Mic size={14} />
            Re-explain
          </button>
        </>
      )}

      {isVoiceActive && (
        <span className="text-green-400 text-xs font-medium">
          🎙 Listening...
        </span>
      )}
    </div>
  );
}
