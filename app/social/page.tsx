'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { ArrowLeft, Users, Swords, Trophy, Search, Loader2 } from 'lucide-react';
import Link from 'next/link';

interface Challenge {
  id: number;
  creator_id: number;
  opponent_id: number;
  creator_xp: number;
  opponent_xp: number;
  goal_xp: number;
  status: string;
}

interface LeaderboardEntry {
  username: string;
  xp: number;
  level: string;
}

export default function SocialPage() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [opponent, setOpponent] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }
    fetchData();
  }, [user]);

  const fetchData = async () => {
    try {
      const [chalRes, leadRes] = await Promise.all([
        api.get('/social/challenges'),
        api.get('/gamification/leaderboard')
      ]);
      setChallenges(chalRes.data);
      // Handle array vs object response for leaderboard
      const leadData = Array.isArray(leadRes.data) ? leadRes.data : leadRes.data.leaderboard || [];
      setLeaderboard(leadData);
    } catch (error) {
      console.error('Error fetching social data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChallenge = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!opponent.trim()) return;
    
    setCreating(true);
    try {
      await api.post('/social/challenge', { opponent_username: opponent, goal_xp: 500 });
      toast.success('Challenge sent!');
      setOpponent('');
      fetchData();
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to send challenge');
    } finally {
      setCreating(false);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-white"><Loader2 className="w-12 h-12 animate-spin text-indigo-600" /></div>;

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      {/* Header */}
      <header className="bg-white border-b border-gray-100 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/dashboard" className="p-2 hover:bg-gray-100 rounded-full transition-colors">
              <ArrowLeft className="w-6 h-6 text-gray-600" />
            </Link>
            <h1 className="text-2xl font-black text-gray-900 tracking-tight">Social & Challenges</h1>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content: Challenges */}
          <div className="lg:col-span-2 space-y-8">
            <div className="bg-white rounded-[32px] p-8 border-2 border-gray-100 shadow-sm">
              <div className="flex items-center space-x-4 mb-8">
                <div className="w-14 h-14 bg-red-50 rounded-2xl flex items-center justify-center">
                  <Swords className="w-7 h-7 text-red-500" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Friend Duels</h2>
                  <p className="text-gray-500 font-medium">Race to 500 XP and prove who is the best!</p>
                </div>
              </div>

              {/* Create Challenge Form */}
              <form onSubmit={handleCreateChallenge} className="flex space-x-4 mb-10 bg-gray-50 p-4 rounded-3xl">
                <div className="flex-1 relative">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Enter friend's username..."
                    value={opponent}
                    onChange={(e) => setOpponent(e.target.value)}
                    className="w-full bg-white border-2 border-gray-200 rounded-2xl pl-12 pr-4 py-4 text-gray-900 focus:border-indigo-500 focus:ring-0 outline-none transition-colors"
                  />
                </div>
                <button 
                  type="submit" 
                  disabled={creating || !opponent.trim()}
                  className="bg-indigo-600 text-white px-8 py-4 rounded-2xl font-bold hover:bg-indigo-700 transition-colors disabled:opacity-50"
                >
                  {creating ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : 'Challenge'}
                </button>
              </form>

              {/* Active Challenges List */}
              <div className="space-y-4">
                <h3 className="text-lg font-bold text-gray-900 mb-4 uppercase tracking-widest text-sm opacity-60">Active Duels</h3>
                {challenges.length === 0 ? (
                  <div className="text-center py-12 bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200">
                    <Swords className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500 font-medium">No active challenges. Start one above!</p>
                  </div>
                ) : (
                  challenges.map((c) => {
                    const isCreator = c.creator_id === user?.id;
                    const myXp = isCreator ? c.creator_xp : c.opponent_xp;
                    const opponentXp = isCreator ? c.opponent_xp : c.creator_xp;
                    const progress = Math.min((myXp / c.goal_xp) * 100, 100);
                    const oppProgress = Math.min((opponentXp / c.goal_xp) * 100, 100);

                    return (
                      <div key={c.id} className="bg-white border-2 border-gray-100 rounded-3xl p-6 relative overflow-hidden">
                        <div className="flex justify-between items-center mb-6">
                          <span className="font-bold text-gray-900">You vs User #{isCreator ? c.opponent_id : c.creator_id}</span>
                          <span className="text-xs font-black bg-indigo-50 text-indigo-600 px-3 py-1 rounded-full uppercase tracking-widest">
                            Goal: {c.goal_xp} XP
                          </span>
                        </div>

                        {/* My Progress */}
                        <div className="mb-4">
                          <div className="flex justify-between text-sm font-bold mb-2">
                            <span className="text-indigo-600">You</span>
                            <span className="text-gray-900">{myXp} XP</span>
                          </div>
                          <div className="h-4 bg-gray-100 rounded-full overflow-hidden">
                            <div className="h-full bg-indigo-500 transition-all duration-1000" style={{ width: `${progress}%` }}></div>
                          </div>
                        </div>

                        {/* Opponent Progress */}
                        <div>
                          <div className="flex justify-between text-sm font-bold mb-2">
                            <span className="text-red-500">Opponent</span>
                            <span className="text-gray-900">{opponentXp} XP</span>
                          </div>
                          <div className="h-4 bg-gray-100 rounded-full overflow-hidden">
                            <div className="h-full bg-red-400 transition-all duration-1000" style={{ width: `${oppProgress}%` }}></div>
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>

          {/* Sidebar: Global Leaderboard */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-[32px] border-2 border-gray-100 shadow-sm p-8 sticky top-24">
              <div className="flex items-center space-x-3 mb-8">
                <Trophy className="w-6 h-6 text-[#FFD700]" />
                <h3 className="text-xl font-bold text-gray-900">Global League</h3>
              </div>

              <div className="space-y-6">
                {leaderboard.length > 0 ? (
                  leaderboard.map((entry, idx) => (
                    <div key={idx} className="flex items-center justify-between group">
                      <div className="flex items-center space-x-4">
                        <span className={`text-sm font-black w-6 ${idx === 0 ? 'text-[#FFD700]' : idx === 1 ? 'text-gray-400' : idx === 2 ? 'text-amber-600' : 'text-gray-300'}`}>
                          {idx + 1}
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
                  <p className="text-gray-500 text-center py-4">No data yet.</p>
                )}
              </div>
            </div>
          </div>

        </div>
      </main>
    </div>
  );
}
