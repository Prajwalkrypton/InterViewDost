import { Button } from "./ui/button";
import { motion } from "motion/react";

export function CTASection() {
  return (
    <section className="relative py-32 px-6 bg-zinc-950 overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-b from-zinc-950 via-zinc-950/90 to-zinc-950" />
      </div>

      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-gradient-to-r from-blue-500/10 to-purple-500/10 blur-3xl rounded-full" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-block px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full mb-8">
            <span className="text-blue-400 text-sm">Limited Beta Access Available</span>
          </div>

          <h2 className="text-5xl md:text-6xl mb-6 text-white leading-tight">
            Ready to Transform Your Interview Preparation?
          </h2>
          <p className="text-xl text-zinc-300 mb-12 max-w-2xl mx-auto leading-relaxed">
            Join the future of interview training with AI-powered evaluation, 
            realistic avatars, and personalized feedback.
          </p>

          <div className="flex gap-4 justify-center mb-16">
            <Button size="lg" className="bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-500/20 px-8">
              Get Started Now →
            </Button>
            <Button size="lg" variant="outline" className="border-zinc-700 text-white hover:bg-zinc-900 px-8">
              Schedule Demo
            </Button>
          </div>

          {/* Stats - Redesigned */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20">
            {[
              { value: "10K+", label: "Interviews Conducted", subtext: "across all industries" },
              { value: "95%", label: "Success Rate", subtext: "job placement increase" },
              { value: "50+", label: "Question Types", subtext: "continuously expanding" },
            ].map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="relative group"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 rounded-2xl blur-xl group-hover:blur-2xl transition-all" />
                <div className="relative bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 hover:border-zinc-700 transition-all">
                  <div className="text-5xl mb-2 bg-gradient-to-br from-white via-blue-100 to-purple-200 bg-clip-text text-transparent">
                    {stat.value}
                  </div>
                  <div className="text-base text-white mb-1">{stat.label}</div>
                  <div className="text-xs text-zinc-500">{stat.subtext}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}