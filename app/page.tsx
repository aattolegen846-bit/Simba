'use client';

import Link from 'next/link';
import { BookOpen, Brain, Trophy, Zap } from 'lucide-react';
import { BookOpen, Trophy, Zap } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-md border border-gray-100 p-1">
              <img src="/logo.png" alt="Simba" className="w-full h-full object-contain" />
            </div>
            <span className="text-2xl font-black tracking-tight text-gray-900 uppercase">SIMBA</span>
          </div>
          <div className="space-x-4">
            <Link href="/login" className="text-gray-700 hover:text-indigo-600 font-medium">
              Login
            </Link>
            <Link href="/register" className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 font-medium">
              Sign Up
            </Link>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Learn Languages with AI
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Personalized lessons, real-time feedback, and gamified learning powered by artificial intelligence
          </p>
          <Link href="/register" className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 inline-block">
            Start Learning Free
          </Link>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mt-20">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <BookOpen className="w-12 h-12 text-indigo-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Personalized Lessons</h3>
            <p className="text-gray-600">AI adapts to your level and learning style</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md">
            <Brain className="w-12 h-12 text-indigo-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Smart Feedback</h3>
            <p className="text-gray-600">Get instant corrections and explanations</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md">
            <Trophy className="w-12 h-12 text-indigo-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Gamification</h3>
            <p className="text-gray-600">Earn XP, maintain streaks, climb leaderboards</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-md">
            <Zap className="w-12 h-12 text-indigo-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Fast Progress</h3>
            <p className="text-gray-600">Track your improvement in real-time</p>
          </div>
        </div>
      </main>
    </div>
  );
}
