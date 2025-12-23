import { motion } from "motion/react";

export function WhatIsSection() {
  return (
    <section className="relative py-32 px-6 bg-black overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0">
        <img 
          src="https://images.unsplash.com/photo-1652212976547-16d7e2841b8c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxhYnN0cmFjdCUyMHRlY2hub2xvZ3klMjBibHVlfGVufDF8fHx8MTc2NjQ3MzUyOHww&ixlib=rb-4.1.0&q=80&w=1080"
          alt=""
          className="w-full h-full object-cover opacity-10"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black via-transparent to-black" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <h2 className="text-5xl md:text-6xl mb-6 text-white">
            What is AI Auto Interviewer?
          </h2>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto">
            A revolutionary interview preparation system that combines artificial intelligence, 
            voice interaction, and realistic avatar technology to simulate authentic interview experiences.
          </p>
        </motion.div>

        {/* Feature Grid - Redesigned with unique layouts */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1 - Personalized AI */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 hover:border-zinc-700 transition-colors"
          >
            <div className="w-12 h-12 bg-zinc-800 rounded-xl flex items-center justify-center mb-6">
              <svg className="w-6 h-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-2xl mb-3 text-white">Personalized AI</h3>
            <p className="text-zinc-400 leading-relaxed">Dynamic question generation based on your responses and interview type</p>
          </motion.div>

          {/* Card 2 - Voice-First Interface */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 hover:border-zinc-700 transition-colors"
          >
            <div className="w-12 h-12 bg-zinc-800 rounded-xl flex items-center justify-center mb-6">
              <svg className="w-6 h-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
            <h3 className="text-2xl mb-3 text-white">Voice-First Interface</h3>
            <p className="text-zinc-400 leading-relaxed">Natural conversation flow with speech recognition and text-to-speech</p>
          </motion.div>

          {/* Card 3 - Powered by GPT-4 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 hover:border-zinc-700 transition-colors"
          >
            <div className="w-12 h-12 bg-zinc-800 rounded-xl flex items-center justify-center mb-6">
              <svg className="w-6 h-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-2xl mb-3 text-white">Powered by GPT-4 AI</h3>
            <p className="text-zinc-400 leading-relaxed">Advanced language model ensures intelligent follow-ups and evaluation</p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}