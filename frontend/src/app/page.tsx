import { Navbar } from "@/components/Navbar";
import { PredictionForm } from "@/components/PredictionForm";
import { Dashboard } from "@/components/Dashboard";
import { BackgroundEffects } from "@/components/BackgroundEffects";
import { Hero } from "@/components/Hero";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-background relative overflow-hidden">
      <BackgroundEffects />

      <Navbar />

      <div className="container mx-auto px-4 py-8 md:py-12 z-10">
        <Hero />

        <section id="predict" className="mb-16">
          <PredictionForm />
        </section>

        <section id="features">
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold font-heading">Model Intelligence</h2>
              <p className="text-muted-foreground">Insights derived from Global YouTube Statistics dataset</p>
            </div>
          </div>
          <Dashboard />
        </section>
      </div>
    </main>
  );
}
