import { motion } from "motion/react";

export function FeaturesSection() {
  return (
    <section className="relative py-32 px-6 bg-zinc-950 overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0">
        <img 
          src="https://images.unsplash.com/photo-1758518727193-a8da31447858?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBvZmZpY2UlMjBpbnRlcnZpZXd8ZW58MXx8fHwxNzY2NDc0ODI4fDA&ixlib=rb-4.1.0&q=80&w=1080"
          alt=""
          className="w-full h-full object-cover opacity-5"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-zinc-950 via-zinc-950/95 to-zinc-950" />
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
            Key Features
          </h2>
          <p className="text-xl text-zinc-400">
            Everything you need for comprehensive interview preparation
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Card 1 - Realistic Avatar */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 hover:border-zinc-700 transition-colors"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-zinc-800 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg className="w-6 h-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 className="text-2xl text-white">Realistic Avatar</h3>
            </div>
            <p className="text-zinc-400 mb-6 leading-relaxed">
              Experience interviews with a human-like AI avatar featuring synchronized lip movement and natural expressions that adapt to the conversation.
            </p>
            <ul className="space-y-2 text-sm text-zinc-400">
              <li>• Natural facial expressions</li>
              <li>• Lip-sync technology</li>
              <li>• Gesture recognition</li>
            </ul>
          </motion.div>

          {/* Card 2 - Smart Evaluation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 hover:border-zinc-700 transition-colors"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-zinc-800 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg className="w-6 h-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-2xl text-white">Smart Evaluation</h3>
            </div>
            <p className="text-zinc-400 mb-6 leading-relaxed">
              Get instant, detailed feedback on your responses with comprehensive scoring across multiple dimensions including clarity and confidence.
            </p>
            <ul className="space-y-2 text-sm text-zinc-400">
              <li>• Multi-criteria analysis</li>
              <li>• Performance metrics</li>
              <li>• Improvement suggestions</li>
            </ul>
          </motion.div>

          {/* Card 3 - Adaptive Questions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 hover:border-zinc-700 transition-colors"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-zinc-800 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg className="w-6 h-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-2xl text-white">Adaptive Questions</h3>
            </div>
            <p className="text-zinc-400 mb-6 leading-relaxed">
              Questions automatically adjust in difficulty and topic based on your performance and expertise level throughout the interview.
            </p>
            <ul className="space-y-2 text-sm text-zinc-400">
              <li>• Difficulty scaling</li>
              <li>• Contextual follow-ups</li>
              <li>• Intelligent branching</li>
            </ul>
          </motion.div>

          {/* Card 4 - Session Recording */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8 hover:border-zinc-700 transition-colors"
          >
            <div className="flex items-center gap-4 mb-6">
              <div className="w-12 h-12 bg-zinc-800 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg className="w-6 h-6 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-2xl text-white">Session Recording</h3>
            </div>
            <p className="text-zinc-400 mb-6 leading-relaxed">
              Complete interview history stored securely in the cloud for unlimited review and performance tracking over time.
            </p>
            <ul className="space-y-2 text-sm text-zinc-400">
              <li>• Full session playback</li>
              <li>• Progress analytics</li>
              <li>• Transcript export</li>
            </ul>
          </motion.div>
        </div>
      </div>
    </section>
  );
}