'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import {
  Trophy, Flame, Target, TrendingUp, LogOut, Zap, ArrowRight,
  User, BookOpen, Award, Calendar, Mic, Settings, Camera,
  MapPin, Clock, Bell, Sun, ChevronRight, BarChart3, Shield
} from 'lucide-react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/theme-toggle';
import { useTheme } from 'next-themes';

interface Stats {
  xp: number;
  streak: number;
  level: string;
  points: number;
  lessons_completed: number;
  weak_skills_count: number;
}

interface Activity {
  icon: typeof BookOpen;
  title: string;
  subtitle: string;
  time: string;
  color: string;
  tintVar: string;
}

const sidebarItems = [
  { icon: User, label: 'Profile Overview', active: true },
  { icon: BarChart3, label: 'Learning Progress', active: false },
  { icon: Award, label: 'Achievements', active: false },
  { icon: Calendar, label: 'Study Plan', active: false },
  { icon: Mic, label: 'Voice Settings', active: false },
  { icon: Settings, label: 'Account Settings', active: false },
];

const achievements = [
  {
    icon: Flame,
    label: 'First Flame',
    desc: 'Achieved 1 day streak',
    gradient: 'linear-gradient(135deg, #FEF3C7, #FDE68A)',
    iconColor: '#F59E0B',
  },
  {
    icon: BookOpen,
    label: 'First Lesson',
    desc: 'Completed your first lesson',
    gradient: 'linear-gradient(135deg, #E0E7FF, #C7D2FE)',
    iconColor: '#6366F1',
  },
  {
    icon: Shield,
    label: 'Getting Started',
    desc: 'Joined Simba',
    gradient: 'linear-gradient(135deg, #D1FAE5, #A7F3D0)',
    iconColor: '#10B981',
  },
];

const recentActivities: Activity[] = [
  { icon: BookOpen, title: 'Completed Lesson', subtitle: 'Basic Introductions', time: '2h ago', color: '#6366F1', tintVar: 'var(--indigo-tint)' },
  { icon: Award, title: 'Practice Session', subtitle: 'Grammar Checker', time: '1d ago', color: '#F59E0B', tintVar: 'var(--orange-tint)' },
  { icon: Mic, title: 'Voice Practice', subtitle: 'Speaking Exercise', time: '2d ago', color: '#8B5CF6', tintVar: 'var(--purple-tint)' },
];

const quickSettings = [
  { icon: Clock, label: 'Daily Goal', value: '15 minutes', tintVar: 'var(--indigo-tint)', color: '#6366F1' },
  { icon: Bell, label: 'Notifications', value: 'On', tintVar: 'var(--orange-tint)', color: '#F59E0B' },
  { icon: Mic, label: 'Voice Assistant', value: 'Female Voice', tintVar: 'var(--purple-tint)', color: '#8B5CF6' },
  { icon: Sun, label: 'Theme', value: 'Auto', tintVar: 'var(--green-tint)', color: '#10B981' },
];

export default function ProfilePage() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const { resolvedTheme } = useTheme();
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [mounted, setMounted] = useState(false);
  const [activeTab, setActiveTab] = useState('Profile Overview');

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchData = async () => {
      try {
        const statsRes = await api.get('/user/stats');
        setStats(statsRes.data);
      } catch (error) {
        toast.error('Failed to load profile data');
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

  const progressPercent = 45;

  if (loading || !mounted) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center" style={{ background: 'var(--background)' }}>
        <div className="w-16 h-16 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-4" />
        <p className="font-medium animate-pulse" style={{ color: 'var(--muted)' }}>Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--background)' }}>
      {/* ─── NAVBAR ─── */}
      <nav className="backdrop-blur-md sticky top-0 z-50" style={{ background: 'var(--nav-bg)', borderBottom: '1px solid var(--card-border)' }}>
        <div className="max-w-[1400px] mx-auto px-8 py-4 flex justify-between items-center">
          <Link href="/dashboard" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-[#FFD700] rounded-xl flex items-center justify-center shadow-md border border-[#E6C200] p-1">
              <img src="/logo.png" alt="Simba" className="w-full h-full object-contain" />
            </div>
            <span className="text-2xl font-black tracking-tight uppercase" style={{ color: 'var(--foreground)' }}>SIMBA</span>
          </Link>

          <div className="flex items-center space-x-4 md:space-x-6">
            <div className="hidden md:flex items-center space-x-4">
              <div className="flex items-center space-x-1 px-3 py-1.5 rounded-full text-orange-600" style={{ background: 'var(--orange-tint)', border: '1px solid var(--orange-border)' }}>
                <Flame className="w-4 h-4 fill-orange-500" />
                <span className="text-sm font-bold">{stats?.streak || 0}</span>
              </div>
              <div className="flex items-center space-x-1 px-3 py-1.5 rounded-full text-indigo-600" style={{ background: 'var(--indigo-tint)', border: '1px solid var(--indigo-border)' }}>
                <Zap className="w-4 h-4 fill-indigo-500" />
                <span className="text-sm font-bold">{stats?.xp || 0}</span>
              </div>
            </div>

            <div className="h-8 w-[1px] hidden md:block" style={{ background: 'var(--card-border)' }} />

            <div className="flex items-center space-x-3">
              <ThemeToggle />
              <div className="text-right hidden sm:block">
                <p className="text-sm font-bold leading-none" style={{ color: 'var(--foreground)' }}>{user?.username}</p>
                <p className="text-[10px] font-black text-indigo-600 uppercase tracking-widest">{stats?.level || 'A1'} LEARNER</p>
              </div>
              <button onClick={handleLogout} className="p-2 rounded-xl transition-all" style={{ color: 'var(--muted)' }} title="Logout">
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-[1400px] mx-auto px-8 py-10">
        {/* ─── HERO PROFILE CARD ─── */}
        <div className="rounded-[28px] p-8 md:p-10 mb-8" style={{ background: 'var(--card)', border: '1px solid var(--card-border)', boxShadow: '0 1px 3px rgba(0,0,0,0.04)' }}>
          <div className="flex flex-col lg:flex-row items-start lg:items-center gap-8">
            {/* Avatar & Info */}
            <div className="flex items-center gap-6 flex-1">
              <div className="relative group">
                <div className="w-28 h-28 rounded-full overflow-hidden border-4 flex items-center justify-center text-4xl font-black" style={{ borderColor: 'var(--card-border)', background: 'var(--indigo-tint)', color: '#6366F1' }}>
                  {user?.username?.[0]?.toUpperCase() || 'U'}
                </div>
                <button className="absolute bottom-0 right-0 w-9 h-9 rounded-full flex items-center justify-center shadow-lg border-2 transition-transform group-hover:scale-110" style={{ background: 'var(--card)', borderColor: 'var(--card-border)' }}>
                  <Camera className="w-4 h-4" style={{ color: 'var(--muted)' }} />
                </button>
              </div>

              <div>
                <h1 className="text-3xl font-black mb-1" style={{ color: 'var(--foreground)' }}>
                  Salem, {user?.username}! 👋
                </h1>
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs font-black uppercase tracking-widest px-3 py-1 rounded-full text-indigo-600" style={{ background: 'var(--indigo-tint)', border: '1px solid var(--indigo-border)' }}>
                    {stats?.level || 'A1'} LEARNER
                  </span>
                </div>
                <p className="text-sm mb-1" style={{ color: 'var(--muted)' }}>
                  <Calendar className="w-3.5 h-3.5 inline mr-1.5 -mt-0.5" />
                  Learning with Simba since Jan 2024
                </p>
                <p className="text-sm" style={{ color: 'var(--muted)' }}>
                  <MapPin className="w-3.5 h-3.5 inline mr-1.5 -mt-0.5" />
                  Kazakhstan
                </p>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full lg:w-auto">
              {[
                { label: 'TOTAL XP', value: stats?.xp || 0, icon: Trophy, color: 'text-yellow-500', tint: 'var(--yellow-tint)' },
                { label: 'DAY STREAK', value: stats?.streak || 0, icon: Flame, color: 'text-orange-500', tint: 'var(--orange-tint)' },
                { label: 'CEFR LEVEL', value: stats?.level || 'A1', icon: Target, color: 'text-blue-500', tint: 'var(--blue-tint)' },
                { label: 'PRO POINTS', value: stats?.points || 0, icon: TrendingUp, color: 'text-green-500', tint: 'var(--green-tint)' },
              ].map((stat, idx) => (
                <div key={idx} className="text-center px-5 py-4 rounded-2xl" style={{ background: 'var(--muted-bg)' }}>
                  <div className="w-10 h-10 rounded-xl mx-auto mb-2 flex items-center justify-center" style={{ background: stat.tint }}>
                    <stat.icon className={`w-5 h-5 ${stat.color}`} />
                  </div>
                  <p className="text-2xl font-black" style={{ color: 'var(--foreground)' }}>{stat.value}</p>
                  <p className="text-[10px] font-black uppercase tracking-widest mt-1" style={{ color: 'var(--muted)' }}>{stat.label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ─── MAIN GRID: Sidebar + Center + Right ─── */}
        <div className="grid grid-cols-1 lg:grid-cols-[220px_1fr_320px] gap-8">
          {/* LEFT SIDEBAR */}
          <div className="rounded-[28px] p-5 self-start" style={{ background: 'var(--card)', border: '1px solid var(--card-border)', boxShadow: '0 1px 3px rgba(0,0,0,0.04)' }}>
            <nav className="space-y-1">
              {sidebarItems.map((item) => (
                <button
                  key={item.label}
                  onClick={() => setActiveTab(item.label)}
                  className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all text-left"
                  style={{
                    background: activeTab === item.label ? 'var(--indigo-tint)' : 'transparent',
                    color: activeTab === item.label ? '#6366F1' : 'var(--foreground)',
                  }}
                >
                  <item.icon className="w-[18px] h-[18px]" />
                  <span>{item.label}</span>
                </button>
              ))}
            </nav>
            <div className="mt-4 pt-4" style={{ borderTop: '1px solid var(--card-border)' }}>
              <button
                onClick={handleLogout}
                className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all text-red-500"
                style={{ background: 'var(--red-hover)' }}
              >
                <LogOut className="w-[18px] h-[18px]" />
                <span>Sign Out</span>
              </button>
            </div>
          </div>

          {/* CENTER CONTENT */}
          <div className="space-y-8">
            {/* Achievements */}
            <div className="rounded-[28px] p-8" style={{ background: 'var(--card)', border: '1px solid var(--card-border)', boxShadow: '0 1px 3px rgba(0,0,0,0.04)' }}>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold" style={{ color: 'var(--foreground)' }}>Achievements</h2>
                <button className="text-xs font-black text-indigo-600 uppercase tracking-widest hover:underline">View All</button>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
                {achievements.map((a, idx) => (
                  <div key={idx} className="text-center group">
                    <div
                      className="w-20 h-20 rounded-2xl mx-auto mb-3 flex items-center justify-center shadow-sm group-hover:scale-105 transition-transform"
                      style={{ background: a.gradient }}
                    >
                      <a.icon className="w-8 h-8" style={{ color: a.iconColor }} />
                    </div>
                    <p className="font-bold text-sm" style={{ color: 'var(--foreground)' }}>{a.label}</p>
                    <p className="text-xs mt-0.5" style={{ color: 'var(--muted)' }}>{a.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Learning Progress */}
            <div className="rounded-[28px] p-8" style={{ background: 'var(--card)', border: '1px solid var(--card-border)', boxShadow: '0 1px 3px rgba(0,0,0,0.04)' }}>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold" style={{ color: 'var(--foreground)' }}>Learning Progress</h2>
                <Link href="/courses" className="text-xs font-black text-indigo-600 uppercase tracking-widest hover:underline">View Progress</Link>
              </div>
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm font-semibold" style={{ color: 'var(--foreground)' }}>CEFR Level Progress</p>
                <span className="text-sm font-black text-indigo-600 px-3 py-1 rounded-full" style={{ background: 'var(--indigo-tint)' }}>{stats?.level || 'A1'}</span>
              </div>
              {/* Progress bar */}
              <div className="w-full h-5 rounded-full overflow-hidden relative" style={{ background: 'var(--muted-bg)' }}>
                <div
                  className="h-full rounded-full relative overflow-hidden transition-all duration-700"
                  style={{
                    width: `${progressPercent}%`,
                    background: 'linear-gradient(90deg, #6366F1, #818CF8)',
                  }}
                >
                  <div className="progress-bar-shine" />
                  <span className="absolute inset-0 flex items-center justify-center text-white text-xs font-bold">{progressPercent}%</span>
                </div>
              </div>
              <p className="text-sm mt-2" style={{ color: 'var(--muted)' }}>{progressPercent}% to next level</p>
            </div>
          </div>

          {/* RIGHT SIDEBAR — Recent Activity */}
          <div className="space-y-8">
            <div className="rounded-[28px] p-7" style={{ background: 'var(--card)', border: '1px solid var(--card-border)', boxShadow: '0 1px 3px rgba(0,0,0,0.04)' }}>
              <h2 className="text-xl font-bold mb-6" style={{ color: 'var(--foreground)' }}>Recent Activity</h2>
              <div className="space-y-5">
                {recentActivities.map((activity, idx) => (
                  <div key={idx} className="flex items-center gap-4">
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0" style={{ background: activity.tintVar }}>
                      <activity.icon className="w-5 h-5" style={{ color: activity.color }} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold truncate" style={{ color: 'var(--foreground)' }}>{activity.title}</p>
                      <p className="text-xs truncate" style={{ color: 'var(--muted)' }}>{activity.subtitle}</p>
                    </div>
                    <span className="text-xs font-medium shrink-0" style={{ color: 'var(--muted)' }}>{activity.time}</span>
                  </div>
                ))}
              </div>
              <button className="w-full mt-6 text-center text-xs font-black text-indigo-600 uppercase tracking-widest hover:underline">
                View All Activity
              </button>
            </div>
          </div>
        </div>

        {/* ─── BOTTOM: QUICK SETTINGS ─── */}
        <div className="mt-8 rounded-[28px] p-8" style={{ background: 'var(--card)', border: '1px solid var(--card-border)', boxShadow: '0 1px 3px rgba(0,0,0,0.04)' }}>
          <h2 className="text-xl font-bold mb-6" style={{ color: 'var(--foreground)' }}>Quick Settings</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickSettings.map((setting, idx) => (
              <button
                key={idx}
                className="flex items-center gap-4 p-4 rounded-2xl transition-all hover:shadow-sm group text-left"
                style={{ background: 'var(--muted-bg)', border: '1px solid var(--card-border)' }}
              >
                <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0" style={{ background: setting.tintVar }}>
                  <setting.icon className="w-5 h-5" style={{ color: setting.color }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold truncate" style={{ color: 'var(--foreground)' }}>{setting.label}</p>
                  <p className="text-xs truncate" style={{ color: 'var(--muted)' }}>{setting.value}</p>
                </div>
                <ChevronRight className="w-4 h-4 shrink-0 group-hover:translate-x-0.5 transition-transform" style={{ color: 'var(--muted)' }} />
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
