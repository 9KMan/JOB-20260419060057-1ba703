import Link from "next/link";
import { Music, Calendar, Users, Sparkles, ArrowRight, CheckCircle } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <header className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Music className="h-8 w-8 text-primary-400" />
            <span className="text-xl font-bold text-white">MusicSync Pro</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-white hover:text-primary-400 transition">
              Sign In
            </Link>
            <Link
              href="/register"
              className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg transition"
            >
              Get Started
            </Link>
          </div>
        </nav>
      </header>

      <main className="container mx-auto px-4 py-20">
        <section className="text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-primary-500/20 text-primary-400 px-4 py-2 rounded-full mb-6">
            <Sparkles className="h-4 w-4" />
            <span className="text-sm font-medium">AI-Powered Booking Platform</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Book Music Events
            <span className="block text-primary-400">Without the Hassle</span>
          </h1>
          <p className="text-xl text-slate-300 mb-10 max-w-2xl mx-auto">
            The all-in-one platform for artists, venues, and event organizers.
            Intelligent scheduling, AI-powered descriptions, and seamless payments.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="bg-primary-500 hover:bg-primary-600 text-white px-8 py-4 rounded-lg font-medium flex items-center justify-center gap-2 transition"
            >
              Start Free Trial <ArrowRight className="h-5 w-5" />
            </Link>
            <Link
              href="/demo"
              className="border border-slate-500 hover:border-slate-400 text-white px-8 py-4 rounded-lg font-medium flex items-center justify-center gap-2 transition"
            >
              Watch Demo
            </Link>
          </div>
        </section>

        <section className="mt-32 grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Calendar className="h-10 w-10" />}
            title="Smart Scheduling"
            description="AI-optimized booking times and conflict detection. Never double-book again."
          />
          <FeatureCard
            icon={<Users className="h-10 w-10" />}
            title="Artist Discovery"
            description="Find the perfect artists for your venue. Filter by genre, availability, and price."
          />
          <FeatureCard
            icon={<Sparkles className="h-10 w-10" />}
            title="AI Assistant"
            description="Generate compelling event descriptions and marketing copy with GPT-4 and Claude."
          />
        </section>

        <section className="mt-32">
          <h2 className="text-3xl font-bold text-white text-center mb-12">
            Trusted by Leading Venues
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 opacity-60">
            <div className="h-12 bg-slate-700 rounded-lg"></div>
            <div className="h-12 bg-slate-700 rounded-lg"></div>
            <div className="h-12 bg-slate-700 rounded-lg"></div>
            <div className="h-12 bg-slate-700 rounded-lg"></div>
          </div>
        </section>

        <section className="mt-32 bg-slate-800/50 rounded-2xl p-8 md:p-12">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-white mb-4">
                Ready to transform your booking process?
              </h2>
              <p className="text-slate-300 mb-6">
                Join hundreds of venues and artists already using MusicSync Pro.
                Start your free trial today.
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-2 text-slate-300">
                  <CheckCircle className="h-5 w-5 text-primary-400" />
                  14-day free trial
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <CheckCircle className="h-5 w-5 text-primary-400" />
                  No credit card required
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <CheckCircle className="h-5 w-5 text-primary-400" />
                  Cancel anytime
                </li>
              </ul>
            </div>
            <div className="bg-slate-700 rounded-xl p-6">
              <h3 className="text-white font-semibold mb-4">Basic Plan</h3>
              <div className="text-4xl font-bold text-white mb-2">$49<span className="text-lg text-slate-400">/month</span></div>
              <p className="text-slate-400 mb-6">Perfect for small venues and independent artists</p>
              <Link
                href="/register"
                className="block w-full bg-primary-500 hover:bg-primary-600 text-white text-center py-3 rounded-lg font-medium transition"
              >
                Start Free Trial
              </Link>
            </div>
          </div>
        </section>
      </main>

      <footer className="container mx-auto px-4 py-12 border-t border-slate-700 mt-32">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Music className="h-6 w-6 text-primary-400" />
            <span className="text-lg font-bold text-white">MusicSync Pro</span>
          </div>
          <p className="text-slate-400 text-sm">
            © 2024 MusicSync Pro. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-slate-800/50 rounded-xl p-6 hover:bg-slate-800 transition">
      <div className="text-primary-400 mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-slate-400">{description}</p>
    </div>
  );
}
