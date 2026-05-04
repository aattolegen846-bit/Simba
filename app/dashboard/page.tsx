'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { Brain, Trophy, Flame, Target, TrendingUp, LogOut, Sparkles, Zap, ArrowRight, BookOpen, Layout, Users } from 'lucide-react';
import Link from 'next/link';

interface Stats {
  xp: number;
  streak: number;
  level: string;
  points: number;
  lessons_completed: number;
  weak_skills_count: number;
}

interface LeaderboardEntry {
  username: string;
  xp: number;
  rank: number;
}

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [stats, setStats] = useState<Stats | null>(null);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchData = async () => {
      try {
        const [statsRes, leaderboardRes] = await Promise.all([
          api.get('/user/stats'),
          api.get('/social/leaderboard?limit=10'),
        ]);
        setStats(statsRes.data);
        setLeaderboard(leaderboardRes.data.leaderboard || []);
      } catch (error) {
        toast.error('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, router]);

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] flex flex-col items-center justify-center">
        <div className="w-16 h-16 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-4"></div>
        <p className="text-gray-500 font-medium animate-pulse">Synchronizing your progress...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      {/* Premium Navbar */}
      <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-md border border-gray-100 p-1">
              <img src="/logo.png" alt="Simba" className="w-full h-full object-contain" />
            </div>
            <span className="text-2xl font-black tracking-tight text-gray-900 uppercase">SIMBA</span>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="hidden md:flex items-center space-x-4">
              <div className="flex items-center space-x-1 px-3 py-1 bg-orange-50 text-orange-600 rounded-full border border-orange-100">
                <Flame className="w-4 h-4 fill-orange-500" />
                <span className="text-sm font-bold">{stats?.streak || 0}</span>
              </div>
              <div className="flex items-center space-x-1 px-3 py-1 bg-indigo-50 text-indigo-600 rounded-full border border-indigo-100">
                <Zap className="w-4 h-4 fill-indigo-500" />
                <span className="text-sm font-bold">{stats?.xp || 0}</span>
              </div>
            </div>
            
            <div className="h-8 w-[1px] bg-gray-200 hidden md:block"></div>

            <div className="flex items-center space-x-4">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-bold text-gray-900 leading-none">{user?.username}</p>
                <p className="text-[10px] font-black text-indigo-600 uppercase tracking-widest">{stats?.level || 'A1'} LEARNER</p>
              </div>
              <button
                onClick={handleLogout}
                className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all"
                title="Logout"
              >
                <LogOut className="w-6 h-6" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-4">
          <div>
            <h1 className="text-4xl font-black text-gray-900 mb-2">Salem, {user?.username}! 👋</h1>
            <p className="text-gray-500 font-medium text-lg">You're doing great! Keep the momentum going.</p>
          </div>
          <Link 
            href="/lessons" 
            className="premium-button flex items-center justify-center space-x-3 group"
          >
            <Sparkles className="w-5 h-5" />
            <span>Start Daily Session</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {[
            { label: 'Total XP', value: stats?.xp || 0, icon: Trophy, color: 'text-yellow-500', bg: 'bg-yellow-50' },
            { label: 'Day Streak', value: stats?.streak || 0, icon: Flame, color: 'text-orange-500', bg: 'bg-orange-50' },
            { label: 'CEFR Level', value: stats?.level || 'A1', icon: Target, color: 'text-blue-500', bg: 'bg-blue-50' },
            { label: 'Pro Points', value: stats?.points || 0, icon: TrendingUp, color: 'text-green-500', bg: 'bg-green-50' },
          ].map((item, idx) => (
            <div key={idx} className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 ${item.bg} rounded-2xl flex items-center justify-center`}>
                  <item.icon className={`w-6 h-6 ${item.color}`} />
                </div>
                <span className="text-3xl font-black text-gray-900">{item.value}</span>
              </div>
              <p className="text-sm font-black text-gray-400 uppercase tracking-widest">{item.label}</p>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Actions */}
          <div className="lg:col-span-2 space-y-8">
            <div className="grid sm:grid-cols-2 gap-6">
              <Link href="/courses" className="premium-card group !p-8">
                <div className="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <BookOpen className="w-7 h-7 text-indigo-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Curriculum</h3>
                <p className="text-gray-500 text-sm mb-6 leading-relaxed">
                  Browse through 100+ lessons from A1 to C1 levels.
                </p>
                <span className="text-indigo-600 font-bold flex items-center text-sm">
                  Explore Courses <ArrowRight className="w-4 h-4 ml-2" />
                </span>
              </Link>

              <div className="premium-card group !p-8">
                <div className="w-14 h-14 bg-purple-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <Layout className="w-7 h-7 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Weak Skills</h3>
                <p className="text-gray-500 text-sm mb-6 leading-relaxed">
                  You have <span className="font-bold text-purple-600">{stats?.weak_skills_count || 0} topics</span> to review today.
                </p>
                <span className="text-purple-600 font-bold flex items-center text-sm">
                  Fix Mistakes <ArrowRight className="w-4 h-4 ml-2" />
                </span>
              </div>

              <Link href="/grammar-checker" className="premium-card group !p-8 bg-orange-50/30 border-orange-100">
                <div className="w-14 h-14 bg-orange-100 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <Sparkles className="w-7 h-7 text-orange-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Grammar Checker</h3>
                <p className="text-gray-500 text-sm mb-6 leading-relaxed">
                  Check your sentences for mistakes using our AI.
                </p>
                <span className="text-orange-600 font-bold flex items-center text-sm">
                  Try Now <ArrowRight className="w-4 h-4 ml-2" />
                </span>
              </Link>
            </div>

            <div className="bg-indigo-600 rounded-3xl p-8 text-white relative overflow-hidden">
              <div className="relative z-10">
                <h2 className="text-2xl font-bold mb-4">Simba Feature</h2>
                <p className="text-indigo-100 mb-8 max-w-md">
                  Enable Real-Time Voice Conversations to practice your speaking skills with our advanced AI Tutor.
                </p>
                <button className="bg-white text-indigo-600 px-6 py-3 rounded-xl font-bold hover:bg-indigo-50 transition-colors">
                  Try Voice Mode
                </button>
              </div>
              <Brain className="absolute -right-8 -bottom-8 w-48 h-48 text-indigo-500/30" />
            </div>
          </div>

          {/* Leaderboard Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-3xl border border-gray-100 shadow-sm p-8">
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-xl font-bold text-gray-900 flex items-center">
                  <Users className="w-5 h-5 mr-2 text-indigo-600" />
                  League
                </h3>
                <Link href="/social" className="text-xs font-black text-indigo-600 uppercase tracking-widest hover:underline">
                  View All
                </Link>
              </div>

              <div className="space-y-6">
                {leaderboard.length > 0 ? (
                  leaderboard.map((entry, idx) => (
                    <div key={idx} className="flex items-center justify-between group">
                      <div className="flex items-center space-x-4">
                        <span className={`text-sm font-black w-6 ${idx < 3 ? 'text-indigo-600' : 'text-gray-300'}`}>
                          0{idx + 1}
                        </span>
                        <div className="w-10 h-10 bg-gray-100 rounded-xl flex items-center justify-center font-bold text-gray-600 group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                          {entry.username[0].toUpperCase()}
                        </div>
                        <span className="font-bold text-gray-700">{entry.username}</span>
                      </div>
                      <span className="text-sm font-black text-gray-900">{entry.xp} <span className="text-[10px] text-gray-400">XP</span></span>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-12">
                    <Trophy className="w-12 h-12 text-gray-100 mx-auto mb-4" />
                    <p className="text-gray-400 text-sm font-medium">No activity yet in your league.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
