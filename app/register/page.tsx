'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { Brain, Sparkles, User, Mail, Lock } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await api.post('/auth/register', formData);
      const { user, token, refresh_token } = response.data;
      setAuth(user, token, refresh_token);
      toast.success('Welcome to Simba! Your journey begins.', { icon: '✨' });
      router.push('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center mb-10">
          <div className="w-20 h-20 bg-indigo-600 rounded-3xl flex items-center justify-center shadow-2xl shadow-indigo-200 mb-6">
            <Brain className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-4xl font-black tracking-tight text-gray-900">JOIN <span className="text-indigo-600">SIMBA</span></h1>
          <p className="text-gray-500 font-medium mt-2 text-center">Start your journey to Kazakh mastery today.</p>
        </div>

        <div className="premium-card relative overflow-hidden">
          <div className="relative z-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">Create Pro Account</h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-black text-gray-400 uppercase tracking-widest flex items-center">
                  <User className="w-3 h-3 mr-2" />
                  Username
                </label>
                <input
                  type="text"
                  required
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-100 rounded-2xl focus:border-indigo-500 focus:bg-white transition-all outline-none font-medium"
                  placeholder="CoolLearner123"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-black text-gray-400 uppercase tracking-widest flex items-center">
                  <Mail className="w-3 h-3 mr-2" />
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-100 rounded-2xl focus:border-indigo-500 focus:bg-white transition-all outline-none font-medium"
                  placeholder="you@example.com"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-black text-gray-400 uppercase tracking-widest flex items-center">
                  <Lock className="w-3 h-3 mr-2" />
                  Password
                </label>
                <input
                  type="password"
                  required
                  minLength={8}
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-5 py-4 bg-gray-50 border-2 border-gray-100 rounded-2xl focus:border-indigo-500 focus:bg-white transition-all outline-none font-medium"
                  placeholder="Min. 8 characters"
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
                    <span>Start Learning Now</span>
                    <Sparkles className="w-5 h-5" />
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        <p className="text-center mt-8 text-gray-500 font-medium">
          Already part of the family?{' '}
          <Link href="/login" className="text-indigo-600 font-black hover:underline">
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
}
