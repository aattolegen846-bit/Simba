'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { Brain, Clock, ArrowLeft, Sparkles, Zap, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

export default function LessonsPage() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [duration, setDuration] = useState(30);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user) {
      router.push('/login');
    }
  }, [user, router]);

  const handleStartLesson = async () => {
    setLoading(true);
    const loadingToast = toast.loading('Initializing your personalized lesson...');
    try {
      const response = await api.post('/lessons/start', { 
        available_minutes: duration,
        current_level: user?.level || 'a1'
      });
      toast.dismiss(loadingToast);
      toast.success('Lesson ready! Let\'s go.');
      
      // Navigate to the lesson interface using the returned lesson_id
      if (response.data.lesson_id) {
        router.push(`/lessons/${response.data.lesson_id}`);
      } else {
        toast.error('Failed to retrieve lesson ID');
      }
    } catch (error: any) {
      toast.dismiss(loadingToast);
      toast.error(error.response?.data?.error || 'Failed to start lesson');
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      {/* Premium Header */}
      <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <Link href="/dashboard" className="p-2 hover:bg-gray-100 rounded-xl transition-all active:scale-90">
              <ArrowLeft className="w-6 h-6 text-gray-600" />
            </Link>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-black tracking-tight text-gray-900">SIMBA</span>
            </div>
          </div>
          <div className="flex items-center space-x-2 bg-indigo-50 px-4 py-2 rounded-full border border-indigo-100">
            <Zap className="w-4 h-4 text-indigo-600 fill-indigo-600" />
            <span className="text-sm font-bold text-indigo-700">{user.xp || 0} XP</span>
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-12 items-center">
          <div className="lg:col-span-3 space-y-8">
            <div className="space-y-4">
              <h1 className="text-5xl font-black text-gray-900 leading-tight">
                Ready to level up your <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">Kazakh?</span>
              </h1>
              <p className="text-xl text-gray-600 font-medium">
                Our AI Tutor will craft a unique lesson based on your weak points and current progress.
              </p>
            </div>

            <div className="premium-card !p-8 space-y-8">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-black text-gray-400 uppercase tracking-widest flex items-center">
                    <Clock className="w-4 h-4 mr-2" />
                    Lesson Duration
                  </label>
                  <span className="text-indigo-600 font-bold">{duration} Minutes</span>
                </div>
                <div className="grid grid-cols-3 gap-4">
                  {[10, 20, 30, 45, 60, 90].map((mins) => (
                    <button
                      key={mins}
                      onClick={() => setDuration(mins)}
                      className={`py-4 rounded-2xl font-bold transition-all duration-300 border-2 ${
                        duration === mins
                          ? 'bg-indigo-600 border-indigo-600 text-white shadow-xl shadow-indigo-100 scale-105'
                          : 'bg-white border-gray-100 text-gray-600 hover:border-indigo-200 hover:bg-indigo-50'
                      }`}
                    >
                      {mins}m
                    </button>
                  ))}
                </div>
              </div>

              <button
                onClick={handleStartLesson}
                disabled={loading}
                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-5 rounded-2xl text-xl font-black shadow-2xl shadow-indigo-200 hover:shadow-indigo-300 hover:-translate-y-1 active:translate-y-0 active:scale-[0.98] transition-all disabled:opacity-50 flex items-center justify-center space-x-3"
              >
                {loading ? (
                  <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin"></div>
                ) : (
                  <>
                    <span>Begin Pro Session</span>
                    <Sparkles className="w-6 h-6" />
                  </>
                )}
              </button>
            </div>
          </div>

          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm space-y-4">
              <div className="w-12 h-12 bg-green-50 rounded-2xl flex items-center justify-center">
                <ShieldCheck className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="font-bold text-gray-900">Personalized for {user.level?.toUpperCase() || 'A1'}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">
                We've analyzed your last 5 quizzes. Today we'll focus on <span className="font-bold text-gray-900 italic">"Case endings"</span> and <span className="font-bold text-gray-900 italic">"Daily Vocabulary"</span>.
              </p>
            </div>

            <div className="bg-indigo-600 p-6 rounded-3xl text-white shadow-xl shadow-indigo-100 relative overflow-hidden group">
              <div className="relative z-10 space-y-2">
                <p className="text-xs font-black uppercase tracking-widest text-indigo-200">Daily Tip</p>
                <p className="text-sm font-medium leading-relaxed">
                  "Consistent 15-minute daily practice is 3x more effective than one long session per week."
                </p>
              </div>
              <Sparkles className="absolute -right-4 -bottom-4 w-24 h-24 text-white/10 group-hover:scale-125 transition-transform duration-700" />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
