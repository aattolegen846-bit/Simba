'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { Brain, Trophy, Flame, Target, TrendingUp, LogOut, Sparkles, Zap, ArrowRight, BookOpen, Layout, Users } from 'lucide-react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/theme-toggle';

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
        setLeaderboard(Array.isArray(leaderboardRes.data) ? leaderboardRes.data : (leaderboardRes.data.leaderboard || []));
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
      <div className="min-h-screen flex flex-col items-center justify-center" style={{ background: 'var(--background)' }}>
        <div className="w-16 h-16 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-4"></div>
        <p className="font-medium animate-pulse" style={{ color: 'var(--muted)' }}>Synchronizing your progress...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--background)' }}>
      {/* Premium Navbar */}
      <nav className="backdrop-blur-md sticky top-0 z-50" style={{ background: 'var(--nav-bg)', borderBottom: '1px solid var(--card-border)' }}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-[#FFD700] rounded-xl flex items-center justify-center shadow-md border border-[#E6C200] p-1 animate-float">
              <img src="/logo.png" alt="Simba" className="w-full h-full object-contain" />
            </div>
            <span className="text-2xl font-black tracking-tight uppercase" style={{ color: 'var(--foreground)' }}>SIMBA</span>
          </div>
          
          <div className="flex items-center space-x-4 md:space-x-6">
            <div className="hidden md:flex items-center space-x-4">
              <div className="flex items-center space-x-1 px-3 py-1 rounded-full text-orange-600" style={{ background: 'var(--orange-tint)', border: '1px solid var(--orange-border)' }}>
                <Flame className="w-4 h-4 fill-orange-500" />
                <span className="text-sm font-bold">{stats?.streak || 0}</span>
              </div>
              <div className="flex items-center space-x-1 px-3 py-1 rounded-full text-indigo-600" style={{ background: 'var(--indigo-tint)', border: '1px solid var(--indigo-border)' }}>
                <Zap className="w-4 h-4 fill-indigo-500" />
                <span className="text-sm font-bold">{stats?.xp || 0}</span>
              </div>
            </div>
            
            <div className="h-8 w-[1px] hidden md:block" style={{ background: 'var(--card-border)' }}></div>

            <div className="flex items-center space-x-2 md:space-x-4">
              <ThemeToggle />
              <Link href="/profile" className="text-right hidden sm:block hover:opacity-80 transition-opacity">
                <p className="text-sm font-bold leading-none" style={{ color: 'var(--foreground)' }}>{user?.username}</p>
                <p className="text-[10px] font-black text-indigo-600 uppercase tracking-widest">{stats?.level || 'A1'} LEARNER</p>
              </Link>
              <button
                onClick={handleLogout}
                className="p-2 rounded-xl transition-all"
                style={{ color: 'var(--muted)' }}
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
            <h1 className="text-4xl font-black mb-2" style={{ color: 'var(--foreground)' }}>Salem, {user?.username}! 👋</h1>
            <p className="font-medium text-lg" style={{ color: 'var(--muted)' }}>You're doing great! Keep the momentum going.</p>
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
            { label: 'Total XP', value: stats?.xp || 0, icon: Trophy, color: 'text-yellow-500', tint: 'var(--yellow-tint)' },
            { label: 'Day Streak', value: stats?.streak || 0, icon: Flame, color: 'text-orange-500', tint: 'var(--orange-tint)' },
            { label: 'CEFR Level', value: stats?.level || 'A1', icon: Target, color: 'text-blue-500', tint: 'var(--blue-tint)' },
            { label: 'Pro Points', value: stats?.points || 0, icon: TrendingUp, color: 'text-green-500', tint: 'var(--green-tint)' },
          ].map((item, idx) => (
            <div key={idx} className="p-6 rounded-3xl shadow-sm hover:shadow-md transition-shadow" style={{ background: 'var(--card)', border: '1px solid var(--card-border)' }}>
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center" style={{ background: item.tint }}>
                  <item.icon className={`w-6 h-6 ${item.color}`} />
                </div>
                <span className="text-3xl font-black" style={{ color: 'var(--foreground)' }}>{item.value}</span>
              </div>
              <p className="text-sm font-black uppercase tracking-widest" style={{ color: 'var(--muted)' }}>{item.label}</p>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Actions */}
          <div className="lg:col-span-2 space-y-8">
            <div className="grid sm:grid-cols-2 gap-6">
              <Link href="/courses" className="premium-card group !p-8">
                <div className="w-14 h-14 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform" style={{ background: 'var(--indigo-tint)' }}>
                  <BookOpen className="w-7 h-7 text-indigo-600" />
                </div>
                <h3 className="text-xl font-bold mb-2" style={{ color: 'var(--foreground)' }}>Curriculum</h3>
                <p className="text-sm mb-6 leading-relaxed" style={{ color: 'var(--muted)' }}>
                  Browse through 100+ lessons from A1 to C1 levels.
                </p>
                <span className="text-indigo-600 font-bold flex items-center text-sm">
                  Explore Courses <ArrowRight className="w-4 h-4 ml-2" />
                </span>
              </Link>

              <Link href="/lessons/fix_mistakes" className="premium-card group !p-8 block">
                <div className="w-14 h-14 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform" style={{ background: 'var(--purple-tint)' }}>
                  <Layout className="w-7 h-7 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold mb-2" style={{ color: 'var(--foreground)' }}>Weak Skills</h3>
                <p className="text-sm mb-6 leading-relaxed" style={{ color: 'var(--muted)' }}>
                  You have <span className="font-bold text-purple-600">{stats?.weak_skills_count || 0} topics</span> to review today.
                </p>
                <span className="text-purple-600 font-bold flex items-center text-sm">
                  Fix Mistakes <ArrowRight className="w-4 h-4 ml-2" />
                </span>
              </Link>

              <Link href="/grammar-checker" className="premium-card group !p-8" style={{ background: 'var(--orange-tint)', borderColor: 'var(--orange-border)' }}>
                <div className="w-14 h-14 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform" style={{ background: 'var(--orange-border)' }}>
                  <Sparkles className="w-7 h-7 text-orange-600" />
                </div>
                <h3 className="text-xl font-bold mb-2" style={{ color: 'var(--foreground)' }}>Grammar Checker</h3>
                <p className="text-sm mb-6 leading-relaxed" style={{ color: 'var(--muted)' }}>
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
                <Link href="/voice" className="inline-block bg-white text-indigo-600 px-6 py-3 rounded-xl font-bold hover:bg-indigo-50 transition-colors">
                  Try Voice Mode
                </Link>
              </div>
              <Brain className="absolute -right-8 -bottom-8 w-48 h-48 text-indigo-500/30" />
            </div>
          </div>

          {/* Leaderboard Sidebar */}
          <div className="lg:col-span-1">
            <div className="rounded-3xl shadow-sm p-8" style={{ background: 'var(--card)', border: '1px solid var(--card-border)' }}>
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-xl font-bold flex items-center" style={{ color: 'var(--foreground)' }}>
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
                        <span className={`text-sm font-black w-6 ${idx < 3 ? 'text-indigo-600' : ''}`} style={idx >= 3 ? { color: 'var(--muted)' } : {}}>
                          0{idx + 1}
                        </span>
                        <div className="w-10 h-10 rounded-xl flex items-center justify-center font-bold transition-colors" style={{ background: 'var(--avatar-bg)', color: 'var(--avatar-text)' }}>
                          {entry.username[0].toUpperCase()}
                        </div>
                        <span className="font-bold" style={{ color: 'var(--entry-text)' }}>{entry.username}</span>
                      </div>
                      <span className="text-sm font-black" style={{ color: 'var(--xp-text)' }}>{entry.xp} <span className="text-[10px]" style={{ color: 'var(--muted)' }}>XP</span></span>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-12">
                    <Trophy className="w-12 h-12 mx-auto mb-4" style={{ color: 'var(--card-border)' }} />
                    <p className="text-sm font-medium" style={{ color: 'var(--muted)' }}>No activity yet in your league.</p>
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
