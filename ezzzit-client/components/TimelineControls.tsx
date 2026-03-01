"use client";

import { Play, Pause, SkipBack, SkipForward, RotateCcw } from "lucide-react";

interface TimelineControlsProps {
  currentStep: number;
  totalSteps: number;
  isPlaying: boolean;
  playbackSpeed: number;
  onPlay: () => void;
  onPause: () => void;
  onNext: () => void;
  onPrev: () => void;
  onReset: () => void;
  onSliderChange: (step: number) => void;
  onSpeedChange: (speed: number) => void;
}

export default function TimelineControls({
  currentStep,
  totalSteps,
  isPlaying,
  playbackSpeed,
  onPlay,
  onPause,
  onNext,
  onPrev,
  onReset,
  onSliderChange,
  onSpeedChange,
}: TimelineControlsProps) {
  const speedOptions = [0.25, 0.5, 1, 1.5, 2];

  return (
    <div className="p-2 space-y-2 bg-black/20 border-t border-white/10">
      {/* Step Info */}
      <div className="flex items-center justify-between text-xs">
        <span className="text-indigo-400 font-semibold">
          Step {currentStep + 1} of {totalSteps}
        </span>
        {/* Speed Control */}
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-[10px]">Speed:</span>
          <select
            value={playbackSpeed}
            onChange={(e) => onSpeedChange(parseFloat(e.target.value))}
            className="px-2 py-0.5 text-[10px] rounded bg-white/5 text-white border border-white/10 hover:bg-white/10 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition cursor-pointer"
          >
            {speedOptions.map((speed) => (
              <option key={speed} value={speed} className="bg-gray-900">
                {speed}x
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Timeline Slider */}
      <div className="relative">
        <input
          type="range"
          min={0}
          max={Math.max(0, totalSteps - 1)}
          value={currentStep}
          onChange={(e) => onSliderChange(parseInt(e.target.value))}
          className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-indigo-600
            [&::-webkit-slider-thumb]:appearance-none
            [&::-webkit-slider-thumb]:w-3
            [&::-webkit-slider-thumb]:h-3
            [&::-webkit-slider-thumb]:rounded-full
            [&::-webkit-slider-thumb]:bg-indigo-600
            [&::-webkit-slider-thumb]:cursor-pointer
            [&::-webkit-slider-thumb]:shadow-[0_0_10px_rgba(79,70,229,0.5)]
            [&::-webkit-slider-thumb]:hover:scale-110
            [&::-webkit-slider-thumb]:transition-transform"
        />
        <div
          className="absolute top-0 left-0 h-1.5 bg-indigo-600/50 rounded-lg pointer-events-none"
          style={{
            width: `${((currentStep + 1) / totalSteps) * 100}%`,
          }}
        />
      </div>

      {/* Control Buttons */}
      <div className="flex items-center justify-center gap-1.5">
        <button
          onClick={onReset}
          className="p-1.5 bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white rounded border border-white/10 transition"
          title="Reset to start"
        >
          <RotateCcw size={14} />
        </button>

        <button
          onClick={onPrev}
          disabled={currentStep === 0}
          className="p-1.5 bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white rounded border border-white/10 transition disabled:opacity-30 disabled:cursor-not-allowed"
          title="Previous step"
        >
          <SkipBack size={14} />
        </button>

        {isPlaying ? (
          <button
            onClick={onPause}
            className="p-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded transition shadow-[0_0_15px_rgba(79,70,229,0.4)]"
            title="Pause"
          >
            <Pause size={16} />
          </button>
        ) : (
          <button
            onClick={onPlay}
            className="p-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded transition shadow-[0_0_15px_rgba(79,70,229,0.4)]"
            title="Play"
          >
            <Play size={16} />
          </button>
        )}

        <button
          onClick={onNext}
          disabled={currentStep === totalSteps - 1}
          className="p-1.5 bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white rounded border border-white/10 transition disabled:opacity-30 disabled:cursor-not-allowed"
          title="Next step"
        >
          <SkipForward size={14} />
        </button>
      </div>
    </div>
  );
}
