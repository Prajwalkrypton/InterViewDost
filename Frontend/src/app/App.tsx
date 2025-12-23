import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { WhatIsSection } from "./components/WhatIsSection";
import { FeaturesSection } from "./components/FeaturesSection";
import { HowItWorks } from "./components/HowItWorks";
import { CTASection } from "./components/CTASection";
import { Footer } from "./components/Footer";

export default function App() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Header />
      <main>
        <Hero />
        <WhatIsSection />
        <FeaturesSection />
        <HowItWorks />
        <CTASection />
      </main>
      <Footer />
    </div>
  );
}
