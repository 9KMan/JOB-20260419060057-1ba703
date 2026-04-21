"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/lib/store";
import { Calendar, Users, Music, TrendingUp, ArrowRight, Clock } from "lucide-react";

export default function DashboardPage() {
  const { user, token } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!token) {
      router.push("/login");
    }
  }, [token, router]);

  if (!user) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900">
      <header className="bg-slate-800 border-b border-slate-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2">
              <Music className="h-8 w-8 text-primary-400" />
              <span className="text-xl font-bold text-white">MusicSync Pro</span>
            </Link>
            <nav className="flex items-center gap-6">
              <Link href="/dashboard" className="text-white hover:text-primary-400">
                Dashboard
              </Link>
              <Link href="/bookings" className="text-slate-300 hover:text-primary-400">
                Bookings
              </Link>
              <Link href="/events" className="text-slate-300 hover:text-primary-400">
                Events
              </Link>
            </nav>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-white font-medium">{user.full_name}</p>
                <p className="text-slate-400 text-sm capitalize">{user.role}</p>
              </div>
              <button
                onClick={() => useAuthStore.getState().logout()}
                className="text-slate-300 hover:text-white"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">
            Welcome back, {user.full_name}
          </h1>
          <p className="text-slate-400">
            Here&apos;s what&apos;s happening with your bookings today.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={<Calendar className="h-6 w-6" />}
            label="Active Bookings"
            value="12"
            trend="+2 from last month"
          />
          <StatCard
            icon={<Users className="h-6 w-6" />}
            label="Total Artists"
            value="48"
            trend="+5 this week"
          />
          <StatCard
            icon={<Music className="h-6 w-6" />}
            label="Upcoming Events"
            value="8"
            trend="Next in 3 days"
          />
          <StatCard
            icon={<TrendingUp className="h-6 w-6" />}
            label="Revenue"
            value="$4,250"
            trend="+18% from last month"
          />
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          <div className="bg-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-white">Upcoming Bookings</h2>
              <Link href="/bookings" className="text-primary-400 hover:text-primary-300 flex items-center gap-1">
                View all <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
            <div className="space-y-4">
              <BookingItem
                artist="The Midnight Jazz Band"
                venue="Blue Note Lounge"
                date="Apr 24, 2024"
                time="8:00 PM"
                status="Confirmed"
              />
              <BookingItem
                artist="Sarah Chen Quartet"
                venue="Opera House"
                date="Apr 28, 2024"
                time="7:30 PM"
                status="Pending"
              />
              <BookingItem
                artist="Electric Dreams"
                venue="The Warehouse"
                date="May 2, 2024"
                time="9:00 PM"
                status="Confirmed"
              />
            </div>
          </div>

          <div className="bg-slate-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-white">AI Assistant</h2>
              <Link href="/ai" className="text-primary-400 hover:text-primary-300 flex items-center gap-1">
                Open AI <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
            <div className="bg-slate-700 rounded-lg p-4 mb-4">
              <p className="text-slate-300 text-sm">
                Your AI assistant can help you generate event descriptions, suggest
                optimal booking times, and compose professional emails to artists and venues.
              </p>
            </div>
            <div className="space-y-3">
              <AIGenreCard title="Generate Event Description" description="Create compelling copy for your next event" />
              <AIGenreCard title="Suggest Booking Times" description="AI-optimized scheduling recommendations" />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function StatCard({ icon, label, value, trend }: { icon: React.ReactNode; label: string; value: string; trend: string }) {
  return (
    <div className="bg-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="text-primary-400">{icon}</div>
        <span className="text-xs text-green-400 flex items-center gap-1">
          <TrendingUp className="h-3 w-3" /> {trend}
        </span>
      </div>
      <h3 className="text-2xl font-bold text-white mb-1">{value}</h3>
      <p className="text-slate-400 text-sm">{label}</p>
    </div>
  );
}

function BookingItem({ artist, venue, date, time, status }: { artist: string; venue: string; date: string; time: string; status: string }) {
  const statusColors = {
    Confirmed: "bg-green-500/20 text-green-400",
    Pending: "bg-yellow-500/20 text-yellow-400",
    Cancelled: "bg-red-500/20 text-red-400",
  };

  return (
    <div className="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg">
      <div>
        <p className="text-white font-medium">{artist}</p>
        <p className="text-slate-400 text-sm">{venue}</p>
      </div>
      <div className="text-right">
        <div className="flex items-center gap-2 text-slate-300 text-sm">
          <Clock className="h-4 w-4" />
          {date} • {time}
        </div>
        <span className={`inline-block mt-1 px-2 py-0.5 rounded text-xs ${statusColors[status as keyof typeof statusColors]}`}>
          {status}
        </span>
      </div>
    </div>
  );
}

function AIGenreCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-4 bg-slate-700/50 rounded-lg hover:bg-slate-700 transition cursor-pointer">
      <p className="text-white font-medium">{title}</p>
      <p className="text-slate-400 text-sm">{description}</p>
    </div>
  );
}
