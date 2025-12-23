import { motion } from "motion/react";
import howItWorksVideo from "../../../media/2.mp4";

export function HowItWorks() {
  const steps = [
    {
      number: "01",
      title: "Initialize Session",
      description: "Start your interview and meet your AI interviewer avatar",
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
    },
    {
      number: "02",
      title: "Voice Interaction",
      description: "Answer questions naturally using your voice",
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
      ),
    },
    {
      number: "03",
      title: "AI Analysis",
      description: "Real-time evaluation of your responses",
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
    },
    {
      number: "04",
      title: "Get Feedback",
      description: "Receive detailed insights and improvement suggestions",
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
  ];

  return (
    <section className="relative py-32 px-6 bg-black overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0">
        <video
          className="w-full h-full object-cover opacity-60"
          src={howItWorksVideo}
          autoPlay
          muted
          loop
          playsInline
        />
       <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/20 to-black/40" />

      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <h2 className="text-5xl md:text-6xl mb-6 text-white">
            How It Works
          </h2>
          <p className="text-xl text-zinc-400">
            Simple, intuitive process from start to finish
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="relative group"
            >
              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-16 left-full w-full h-px">
                  <div className="h-full w-full bg-gradient-to-r from-zinc-700 via-zinc-700 to-transparent" />
                </div>
              )}

              <div className="relative bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 hover:border-zinc-700 transition-all duration-300 hover:bg-zinc-900/70">
                {/* Icon */}
                <div className="w-12 h-12 bg-blue-500/10 rounded-xl flex items-center justify-center mb-4 text-blue-400 group-hover:bg-blue-500/20 transition-colors">
                  {step.icon}
                </div>
                
                {/* Number */}
                <div className="text-4xl mb-3 bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent">
                  {step.number}
                </div>
                
                <h3 className="text-xl mb-2 text-white">{step.title}</h3>
                <p className="text-sm text-zinc-400 leading-relaxed">{step.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}