'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import { Flame, Zap, LogOut, Mic, MicOff, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/theme-toggle';
import { useTheme } from 'next-themes';

interface Stats {
  xp: number;
  streak: number;
  level: string;
}

export default function VoiceModePage() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const { resolvedTheme } = useTheme();
  const [stats, setStats] = useState<Stats | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchStats = async () => {
      try {
        const statsRes = await api.get('/user/stats');
        setStats(statsRes.data);
      } catch (error) {
        console.error('Failed to load stats', error);
      }
    };

    fetchStats();
  }, [user, router]);

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const toggleRecording = useCallback(() => {
    setIsRecording(prev => {
      if (!prev) {
        setTranscript('Listening...');
        setTimeout(() => {
          setTranscript('I heard you. How can I help you practice your English today?');
          setIsRecording(false);
        }, 3000);
        return true;
      } else {
        setTranscript('');
        return false;
      }
    });
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' && !e.repeat) {
        e.preventDefault();
        toggleRecording();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [toggleRecording]);

  const isDark = mounted ? resolvedTheme === 'dark' : true;

  /* Adaptive colors based on theme */
  const ringColor = isDark ? 'rgba(255,255,255,' : 'rgba(99,102,241,';
  const textPrimary = isDark ? '#FFFFFF' : '#0F172A';
  const textSecondary = isDark ? 'rgba(255,255,255,0.5)' : 'rgba(15,23,42,0.4)';
  const textHint = isDark ? 'rgba(255,255,255,0.4)' : 'rgba(15,23,42,0.35)';
  const bgMain = isDark ? '#000000' : '#F8FAFC';
  const navBg = isDark ? 'rgba(0,0,0,0.5)' : 'rgba(255,255,255,0.8)';
  const navBorder = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)';
  const chipBg = isDark ? 'rgba(255,255,255,0.05)' : 'var(--indigo-tint)';
  const chipBorder = isDark ? 'rgba(255,255,255,0.1)' : 'var(--indigo-border)';
  const chipText = isDark ? '#FFFFFF' : '#4F46E5';
  const cursorColor = isDark ? '#FFFFFF' : '#4F46E5';
  const innerRingBg = isDark ? 'rgba(0,0,0,0.5)' : 'rgba(255,255,255,0.8)';

  return (
    <div className="min-h-screen flex flex-col font-sans transition-colors duration-300" style={{ background: bgMain, color: textPrimary }}>
      {/* Navbar */}
      <nav className="backdrop-blur-md sticky top-0 z-50" style={{ background: navBg, borderBottom: `1px solid ${navBorder}` }}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <Link href="/dashboard" className="p-2 rounded-full transition-colors" style={{ color: textPrimary }}>
              <ArrowLeft className="w-6 h-6" />
            </Link>
            <div className="w-10 h-10 bg-[#FFD700] rounded-xl flex items-center justify-center shadow-md border border-[#E6C200] p-1">
              <img src="/logo.png" alt="Simba" className="w-full h-full object-contain" />
            </div>
            <span className="text-2xl font-black tracking-tight uppercase hidden sm:block" style={{ color: textPrimary }}>VOICE</span>
          </div>
          
          <div className="flex items-center space-x-4 md:space-x-6">
            <div className="hidden md:flex items-center space-x-4">
              <div className="flex items-center space-x-1 px-3 py-1 rounded-full" style={{ background: chipBg, border: `1px solid ${chipBorder}`, color: chipText }}>
                <Flame className="w-4 h-4" />
                <span className="text-sm font-bold">{stats?.streak || 0}</span>
              </div>
              <div className="flex items-center space-x-1 px-3 py-1 rounded-full" style={{ background: chipBg, border: `1px solid ${chipBorder}`, color: chipText }}>
                <Zap className="w-4 h-4" />
                <span className="text-sm font-bold">{stats?.xp || 0}</span>
              </div>
            </div>
            
            <div className="h-8 w-[1px] hidden md:block" style={{ background: navBorder }}></div>

            <div className="flex items-center space-x-2 md:space-x-4">
              <ThemeToggle />
              <div className="text-right hidden sm:block">
                <p className="text-sm font-bold leading-none" style={{ color: textPrimary }}>{user?.username}</p>
                <p className="text-[10px] font-black uppercase tracking-widest" style={{ color: 'var(--muted)' }}>{stats?.level || 'A1'} LEARNER</p>
              </div>
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

      {/* Futuristic Voice Interface */}
      <main className="flex-1 flex flex-col items-center justify-center relative overflow-hidden px-6">

        {/* Central Circular Interface */}
        <div className="relative flex items-center justify-center w-full max-w-sm aspect-square mx-auto cursor-pointer group" onClick={toggleRecording}>
          
          {/* Outer wave ring 1 */}
          <div
            className={`absolute inset-0 rounded-full transition-all duration-1000 ease-in-out ${isRecording ? 'scale-110 opacity-50 animate-pulse' : 'scale-100 opacity-20'}`}
            style={{ border: `1px solid ${ringColor}0.15)` }}
          />
          {/* Outer wave ring 2 */}
          <div
            className={`absolute inset-4 rounded-full transition-all duration-700 ease-in-out ${isRecording ? 'scale-105 opacity-60' : 'scale-100 opacity-30'}`}
            style={{ border: `1px solid ${ringColor}0.25)` }}
          />
          {/* Outer wave ring 3 */}
          <div
            className={`absolute inset-8 rounded-full transition-all duration-500 ease-in-out ${isRecording ? 'scale-110 opacity-80' : 'scale-100 opacity-40'}`}
            style={{ border: `1px solid ${ringColor}0.35)` }}
          />

          {/* Particle dotted ring */}
          <div
            className={`absolute inset-12 rounded-full border-[3px] border-dotted transition-all duration-500 ease-in-out flex items-center justify-center ${isRecording ? 'scale-105 animate-slow-spin' : 'scale-100 group-hover:scale-105'}`}
            style={{
              borderColor: `${ringColor}0.8)`,
              boxShadow: isRecording
                ? `0 0 80px ${ringColor}0.5), 0 0 30px ${ringColor}0.2)`
                : `0 0 40px ${ringColor}0.2)`,
            }}
          >
            {/* Inner solid ring */}
            <div className="absolute inset-2 rounded-full backdrop-blur-sm" style={{ border: `1px solid ${ringColor}0.4)`, background: innerRingBg }} />
          </div>

          {/* Center Text & Icon */}
          <div className="relative z-10 flex flex-col items-center">
            {isRecording ? (
              <Mic className="w-10 h-10 mb-4 animate-pulse" style={{ color: textPrimary }} />
            ) : (
              <MicOff className="w-8 h-8 mb-4 transition-all group-hover:opacity-100" style={{ color: textSecondary }} />
            )}
            <div className="font-mono text-sm tracking-[0.2em] font-bold uppercase flex items-center" style={{ color: textPrimary, opacity: 0.9 }}>
              {isRecording ? 'LISTENING' : 'SPEAK TO BEGIN'}
              <span className="ml-1 w-2 h-4 animate-[pulse_1s_step-end_infinite]" style={{ background: cursorColor }} />
            </div>
          </div>
        </div>

        {/* Transcript/Response Area */}
        <div className="mt-16 max-w-xl mx-auto text-center h-24">
          <p className="text-xl font-medium leading-relaxed font-sans transition-all duration-500" style={{ color: textPrimary, opacity: transcript ? 0.8 : 1 }}>
            {transcript || (
              <span style={{ color: textHint }}>Tap the circle or press Spacebar to activate Simba Voice.</span>
            )}
          </p>
        </div>

      </main>
    </div>
  );
}
