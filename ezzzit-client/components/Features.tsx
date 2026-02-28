"use client";

import { motion } from "framer-motion";
import { Code2, Mic2, Activity, Zap, Layers, Cpu } from "lucide-react";

const features = [
  {
    title: "Real-time Code Tracing",
    description:
      "Watch variables change and logic flow as you step through your DSA algorithms line-by-line.",
    icon: <Code2 className="text-indigo-400" size={24} />,
    className: "md:col-span-2",
    gradient: "from-indigo-500/20 to-transparent",
  },
  {
    title: "ElevenLabs AI Voice",
    description:
      "Talk to an AI tutor that explains complex space complexity in real-time.",
    icon: <Mic2 className="text-purple-400" size={24} />,
    className: "md:col-span-1",
    gradient: "from-purple-500/20 to-transparent",
  },
  {
    title: "Visual Data Structures",
    description:
      "Trees, Graphs, and Linked Lists rendered in smooth 3D animations.",
    icon: <Layers className="text-blue-400" size={24} />,
    className: "md:col-span-1",
    gradient: "from-blue-500/20 to-transparent",
  },
  {
    title: "Performance Analytics",
    description:
      "Detailed breakdown of Big O notation and execution time for every run.",
    icon: <Activity className="text-emerald-400" size={24} />,
    className: "md:col-span-2",
    gradient: "from-emerald-500/20 to-transparent",
  },
];

const FeatureCard = ({
  title,
  description,
  icon,
  className,
  gradient,
}: {
  title: string;
  description: string;
  icon: React.ReactNode;
  className?: string;
  gradient: string;
}) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    className={`relative group overflow-hidden rounded-3xl border border-white/5 bg-[#0B0F1A] p-8 hover:border-white/10 transition-all ${className}`}
  >
    {/* Radial Hover Gradient */}
    <div
      className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-500`}
    />

    <div className="relative z-10">
      <div className="mb-4 inline-flex p-3 rounded-xl bg-white/5 border border-white/10 group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-white mb-3 tracking-tight">
        {title}
      </h3>
      <p className="text-gray-400 leading-relaxed text-sm">{description}</p>
    </div>

    {/* Decorative 3D line at bottom */}
    <div className="absolute bottom-0 left-0 h-[2px] w-0 bg-gradient-to-r from-transparent via-indigo-500 to-transparent group-hover:w-full transition-all duration-700" />
  </motion.div>
);

const Features = () => {
  return (
    <section
      id="features"
      className="py-24 bg-[#030712] relative overflow-hidden"
    >
      {/* Background Orbs */}
      <div className="absolute top-1/2 left-0 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-600/5 rounded-full blur-[120px]" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-extrabold text-white mb-4"
          >
            Master DSA with{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
              Superpowers.
            </span>
          </motion.h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Stop memorizing. Start visualizing. ezzzit combines the power of
            visual learning with generative AI to make coding intuitive.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard key={index} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
