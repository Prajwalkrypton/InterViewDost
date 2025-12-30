import { Button } from "./ui/button";
import { motion } from "motion/react";
import { useNavigate } from "react-router-dom";
import heroVideo from "../../../media/1.mp4";

export function Hero() {
  const navigate = useNavigate();
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0">
        <video
          className="w-full h-full object-cover opacity-60"
          src={heroVideo}
          autoPlay
          muted
          loop
          playsInline
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/20 to-black/40" />

      </div>

      {/* Animated Grid Overlay */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff05_1px,transparent_1px),linear-gradient(to_bottom,#ffffff05_1px,transparent_1px)] bg-[size:64px_64px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,#000_70%,transparent_110%)]" />
      </div>

      {/* Flowing Lines Effect */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute top-1/2 left-0 w-full h-px"
          animate={{
            opacity: [0.2, 0.5, 0.2],
            scaleX: [0.8, 1, 0.8],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        >
          <div className="h-full w-full bg-gradient-to-r from-transparent via-blue-400 to-transparent" />
        </motion.div>
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-block px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full mb-6">
            <span className="text-blue-400 text-sm">Next-Generation Interview Technology</span>
          </div>
          
          <h1 className="text-7xl md:text-8xl mb-6 bg-gradient-to-b from-white via-white to-zinc-500 bg-clip-text text-transparent leading-tight">
            AI-Powered Auto Interviewer
          </h1>
          <p className="text-2xl text-zinc-300 mb-4 max-w-3xl mx-auto">
            Practice with a <span className="text-white">realistic AI avatar</span> that speaks, listens, and evaluates your responses in real-time
          </p>
          <p className="text-base text-zinc-500 mb-12 max-w-2xl mx-auto">
            Voice-driven conversations • Dynamic questioning • Instant feedback • Professional development
          </p>

          <div className="flex gap-4 justify-center mb-20">
            <Button
              size="lg"
              className="bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-500/20"
              onClick={() => navigate("/login")}
            >
              Start Your First Interview
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-zinc-700 text-white hover:bg-zinc-900"
              onClick={() => navigate("/login")}
            >
              Watch Demo
            </Button>
          </div>
        </motion.div>

        {/* Central Avatar Showcase */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.3 }}
          className="relative max-w-5xl mx-auto"
        >
          <div className="relative">
            {/* Glowing Orbs */}
            <div className="absolute -top-20 left-1/4 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl" />
            <div className="absolute -bottom-20 right-1/4 w-64 h-64 bg-purple-500/20 rounded-full blur-3xl" />
            
            {/* Main Avatar Card */}
            <div className="relative bg-gradient-to-br from-zinc-900/80 to-zinc-950/80 backdrop-blur-xl border border-zinc-800 rounded-3xl p-12 shadow-2xl">
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
                  <span className="text-sm text-zinc-400">Live Interview Session</span>
                </div>
                <div className="flex gap-2">
                  <div className="w-16 h-1 bg-zinc-700 rounded-full" />
                  <div className="w-16 h-1 bg-blue-500 rounded-full" />
                  <div className="w-16 h-1 bg-zinc-700 rounded-full" />
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-8 items-center">
                {/* Avatar Visual */}
                <div className="relative">
                  <div className="relative w-64 h-64 mx-auto">
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full blur-2xl opacity-30" />
                    <div className="relative w-full h-full bg-gradient-to-br from-zinc-800 to-zinc-900 rounded-full border-4 border-zinc-700 flex items-center justify-center overflow-hidden">
                      <div className="relative z-10">
                        <svg className="w-24 h-24 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </div>
                      {/* Voice Waves */}
                      <motion.div 
                        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-1"
                        animate={{ opacity: [0.5, 1, 0.5] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                      >
                        {[...Array(5)].map((_, i) => (
                          <motion.div
                            key={i}
                            className="w-1 bg-blue-400 rounded-full"
                            animate={{ height: [12, 24, 12] }}
                            transition={{ 
                              duration: 0.6, 
                              repeat: Infinity,
                              delay: i * 0.1 
                            }}
                          />
                        ))}
                      </motion.div>
                    </div>
                  </div>
                </div>
                
                {/* Interview Info */}
                <div className="text-left space-y-6">
                  <div className="space-y-2">
                    <div className="text-sm text-blue-400">Current Question</div>
                    <div className="text-lg text-white">"Tell me about a challenging project you led and how you handled it."</div>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-zinc-400">Clarity Score</span>
                      <span className="text-sm text-white">8.5/10</span>
                    </div>
                    <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                      <motion.div 
                        className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                        initial={{ width: 0 }}
                        animate={{ width: "85%" }}
                        transition={{ duration: 1.5, delay: 0.5 }}
                      />
                    </div>
                  </div>
                  
                  <div className="flex gap-3 pt-4">
                    <div className="flex-1 bg-zinc-800/50 rounded-xl p-4 text-center">
                      <div className="text-2xl text-white mb-1">12</div>
                      <div className="text-xs text-zinc-500">Questions</div>
                    </div>
                    <div className="flex-1 bg-zinc-800/50 rounded-xl p-4 text-center">
                      <div className="text-2xl text-white mb-1">18m</div>
                      <div className="text-xs text-zinc-500">Duration</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Powered By Section */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.6 }}
          className="mt-20"
        >
          <p className="text-xs text-zinc-600 mb-8 tracking-wider">POWERED BY ADVANCED AI TECHNOLOGY</p>
          <div className="flex items-center justify-center gap-12 flex-wrap opacity-30">
            <span className="text-zinc-500 text-sm">OpenAI GPT-4</span>
            <span className="text-zinc-500 text-sm">Google Cloud TTS</span>
            <span className="text-zinc-500 text-sm">AWS Infrastructure</span>
            <span className="text-zinc-500 text-sm">Azure Cognitive</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}