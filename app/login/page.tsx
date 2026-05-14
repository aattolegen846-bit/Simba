'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { Brain, Sparkles, ShieldCheck, Zap } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await api.post('/auth/login', {
        identifier: formData.username,
        password: formData.password
      });
      const { user, token, refresh_token } = response.data;
      setAuth(user, token, refresh_token);
      toast.success('Salem! Welcome back to Simba.', { icon: '👋' });
      router.push('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center mb-10">
          <div className="w-20 h-20 bg-indigo-600 rounded-3xl flex items-center justify-center shadow-2xl shadow-indigo-200 mb-6 animate-float">
            <Brain className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-4xl font-black tracking-tight text-gray-900">SIMBA</h1>
          <p className="text-gray-500 font-medium mt-2">The most advanced AI Kazakh Tutor</p>
        </div>

        <div className="premium-card relative overflow-hidden">
          <div className="relative z-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-8">Welcome Back</h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-black text-gray-400 uppercase tracking-widest">
                  Username or Email
                </label>
                <input
                  type="text"
                  required
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-100 rounded-2xl focus:border-indigo-500 focus:bg-white transition-all outline-none font-medium"
                  placeholder="name@example.com"
                />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <label className="text-xs font-black text-gray-400 uppercase tracking-widest">
                    Password
                  </label>
                  <Link href="/forgot-password" className="text-xs font-bold text-indigo-600 hover:underline">
                    Forgot password?
                  </Link>
                </div>
                <input
                  type="password"
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-100 rounded-2xl focus:border-indigo-500 focus:bg-white transition-all outline-none font-medium"
                  placeholder="••••••••"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="premium-button w-full flex items-center justify-center space-x-3 text-lg mt-8"
              >
                {loading ? (
                  <div className="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin"></div>
                ) : (
                  <>
                    <span>Enter Pro Experience</span>
                    <Sparkles className="w-5 h-5" />
                  </>
                )}
              </button>
            </form>
          </div>
          
          <Sparkles className="absolute -right-4 -top-4 w-24 h-24 text-indigo-50" />
        </div>

        <p className="text-center mt-8 text-gray-500 font-medium">
          New to the community?{' '}
          <Link href="/register" className="text-indigo-600 font-black hover:underline">
            Create an Account
          </Link>
        </p>

        <div className="mt-12 grid grid-cols-3 gap-4 opacity-50 grayscale hover:grayscale-0 transition-all duration-700">
          <div className="flex flex-col items-center space-y-2">
            <ShieldCheck className="w-5 h-5 text-gray-400" />
            <span className="text-[10px] font-black uppercase tracking-widest">Secure</span>
          </div>
          <div className="flex flex-col items-center space-y-2">
            <Zap className="w-5 h-5 text-gray-400" />
            <span className="text-[10px] font-black uppercase tracking-widest">Fast</span>
          </div>
          <div className="flex flex-col items-center space-y-2">
            <Sparkles className="w-5 h-5 text-gray-400" />
            <span className="text-[10px] font-black uppercase tracking-widest">AI-Driven</span>
          </div>
        </div>
      </div>
    </div>
  );
}
