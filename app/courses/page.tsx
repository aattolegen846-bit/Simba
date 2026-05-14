'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import {
  Flame, Zap, LogOut, BookOpen, Lock, CheckCircle, ChevronDown,
  ArrowRight, Sparkles, Target, MessageSquare, Users, Coffee, Moon
} from 'lucide-react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/theme-toggle';

/* ─── Types ─── */
interface Course { id: number; title: string; description: string; language: string; level: string; }
interface Lesson { id: number; title: string; is_locked?: boolean; is_completed?: boolean; }
interface Module { id: number; title: string; lessons: Lesson[]; }
interface CourseDetails { id: number; title: string; modules: Module[]; }
interface Stats { xp: number; streak: number; level: string; points: number; }

const moduleIcons = [BookOpen, MessageSquare, Target, Users, Coffee, Sparkles];
const moduleDescs = [
  'Learn essential words and simple phrases to get started.',
  'Practice greeting people and introducing yourself.',
  'Talk about your day and common activities.',
  'Learn vocabulary about people and relationships.',
  'Words and phrases for everyday food situations.',
  'Expand your vocabulary with new topics.',
];

// Snake path offset pattern
const pathOffsets = [80, -80, 40, -40, 80, -80, 40, -40];

export default function CoursesPage() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [courses, setCourses] = useState<Course[]>([]);
  const [courseDetails, setCourseDetails] = useState<CourseDetails | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState<number | null>(null);
  const [levelDropdown, setLevelDropdown] = useState(false);

  useEffect(() => {
    if (!user) { router.push('/login'); return; }
    const fetchData = async () => {
      try {
        const [coursesRes, statsRes] = await Promise.all([api.get('/courses'), api.get('/user/stats')]);
        const courseList: Course[] = coursesRes.data;
        setCourses(courseList);
        setStats(statsRes.data);
        if (courseList.length > 0) {
          const firstId = courseList[0].id;
          setSelectedCourse(firstId);
          const detailsRes = await api.get(`/courses/${firstId}`);
          setCourseDetails(detailsRes.data);
        }
      } catch { toast.error('Failed to load courses'); }
      finally { setLoading(false); }
    };
    fetchData();
  }, [user, router]);

  const handleCourseChange = async (courseId: number) => {
    setSelectedCourse(courseId); setLevelDropdown(false);
    try { const res = await api.get(`/courses/${courseId}`); setCourseDetails(res.data); }
    catch { toast.error('Failed to load course'); }
  };

  const handleLogout = () => { logout(); router.push('/'); };

  const modules = courseDetails?.modules || [];
  const totalLessons = modules.reduce((a, m) => a + m.lessons.length, 0);
  const completedLessons = modules.reduce((a, m) => a + m.lessons.filter(l => l.is_completed).length, 0);
  const progressPct = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;
  const currentCourse = courses.find(c => c.id === selectedCourse);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#F7F8FC] dark:bg-[#0B0F19]">
        <div className="w-16 h-16 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-4" />
        <p className="font-medium animate-pulse text-slate-400">Loading roadmap...</p>
      </div>
    );
  }

  /* ── Helper: get module state ── */
  const getModuleState = (mod: Module) => {
    const done = mod.lessons.filter(l => l.is_completed).length;
    const total = mod.lessons.length;
    if (done === total && total > 0) return 'completed';
    if (mod.lessons.every(l => l.is_locked)) return 'locked';
    return 'active';
  };

  /* ── Helper: first active lesson id ── */
  const getFirstActiveLessonId = (mod: Module) => {
    const lesson = mod.lessons.find(l => !l.is_completed && !l.is_locked);
    return lesson?.id;
  };

  return (
    <div className="min-h-screen bg-[#F7F8FC] dark:bg-[#0B0F19] text-slate-900 dark:text-slate-100 font-sans selection:bg-indigo-500/30">
      {/* ─── NAVBAR ─── */}
      <nav className="sticky top-0 z-50 bg-white/70 dark:bg-[#111827]/70 backdrop-blur-xl border-b border-slate-200 dark:border-white/10 transition-colors">
        <div className="max-w-[1280px] mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/dashboard" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 bg-[#FFD700] rounded-[10px] flex items-center justify-center shadow-sm border border-[#E6C200] p-1.5 transition-transform group-hover:scale-105">
              <img src="/logo.png" alt="Simba" className="w-full h-full object-contain" />
            </div>
            <span className="text-xl font-black tracking-tight text-slate-900 dark:text-white uppercase">SIMBA</span>
          </Link>
          <div className="flex items-center space-x-3 sm:space-x-5">
            <div className="hidden sm:flex items-center space-x-3">
              <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-orange-50 dark:bg-orange-500/10 border border-orange-100 dark:border-orange-500/20 text-orange-600 dark:text-orange-400">
                <Flame className="w-4 h-4 fill-current" /><span className="text-sm font-bold">{stats?.streak || 0}</span>
              </div>
              <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-indigo-50 dark:bg-indigo-500/10 border border-indigo-100 dark:border-indigo-500/20 text-indigo-600 dark:text-indigo-400">
                <Zap className="w-4 h-4 fill-current" /><span className="text-sm font-bold">{stats?.xp || 0}</span>
              </div>
            </div>
            <div className="h-6 w-[1px] hidden sm:block bg-slate-200 dark:bg-white/10" />
            <div className="flex items-center space-x-3">
              <div className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors cursor-pointer p-2 rounded-full hover:bg-slate-100 dark:hover:bg-white/5">
                <ThemeToggle />
              </div>
              <Link href="/profile" className="text-right hidden sm:block hover:opacity-80 transition-opacity">
                <p className="text-sm font-bold leading-none text-slate-900 dark:text-white">{user?.username}</p>
                <p className="text-[10px] font-black text-indigo-600 dark:text-indigo-400 uppercase tracking-widest mt-1">{stats?.level || 'A1'} LEARNER</p>
              </Link>
              <button onClick={handleLogout} className="p-2 rounded-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-white/5 transition-all">
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-[1280px] mx-auto px-6 py-12">
        {/* ─── HEADER ─── */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
          <div>
            <h1 className="text-[40px] font-black mb-3 tracking-tight text-slate-900 dark:text-white leading-none">Courses Roadmap</h1>
            <p className="text-slate-500 dark:text-slate-400 text-lg">Follow your AI-powered learning journey.</p>
          </div>
          <div className="relative">
            <button onClick={() => setLevelDropdown(!levelDropdown)} className="flex items-center space-x-2 px-6 py-3 rounded-full text-sm font-bold transition-all bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-500/10 dark:hover:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400">
              <span>{currentCourse?.level || 'A1'} Level</span><ChevronDown className="w-4 h-4" />
            </button>
            {levelDropdown && (
              <div className="absolute right-0 mt-3 w-56 rounded-[20px] shadow-xl z-30 py-2 bg-white dark:bg-[#1E293B] border border-slate-100 dark:border-white/10 overflow-hidden">
                {courses.map(c => (
                  <button key={c.id} onClick={() => handleCourseChange(c.id)} className={`w-full text-left px-5 py-3 text-sm font-bold transition-colors flex items-center justify-between ${c.id === selectedCourse ? 'bg-indigo-50 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/5'}`}>
                    <span>{c.title}</span><span className="text-[10px] uppercase font-black px-2.5 py-1 rounded-full bg-slate-100 dark:bg-white/5 text-slate-500 dark:text-slate-400">{c.level}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_340px] gap-16">
          {/* ═══ LEFT: SNAKE ROADMAP ═══ */}
          <div className="relative flex flex-col items-center w-full pb-32 pt-4">
            {modules.map((mod, idx) => {
              const state = getModuleState(mod);
              const Icon = moduleIcons[idx % moduleIcons.length];
              const desc = moduleDescs[idx % moduleDescs.length];
              const done = mod.lessons.filter(l => l.is_completed).length;
              const activeLessonId = getFirstActiveLessonId(mod);
              
              const offset = pathOffsets[idx % pathOffsets.length];
              const prevOffset = idx > 0 ? pathOffsets[(idx - 1) % pathOffsets.length] : 0;
              const cardSide = idx % 2 === 0 ? 'left' : 'right';

              return (
                <div key={mod.id} className="relative flex flex-col items-center w-full max-w-2xl">
                  
                  {/* Connector Line */}
                  {idx > 0 && (
                    <svg width="300" height="90" viewBox="-150 0 300 90" className="overflow-visible -my-2 z-0 opacity-50 dark:opacity-30">
                      <path 
                        d={`M ${prevOffset} 0 C ${prevOffset} 45, ${offset} 45, ${offset} 90`}
                        stroke="currentColor" 
                        className="text-slate-300 dark:text-slate-700"
                        strokeWidth="4" 
                        fill="none" 
                      />
                    </svg>
                  )}

                  {/* Node Row */}
                  <div 
                    className="relative flex justify-center items-center z-10"
                    style={{
                      transform: `translateX(${offset}px)`,
                      width: state === 'active' ? 100 : 80,
                      height: state === 'active' ? 100 : 80,
                    }}
                  >
                    {/* The Node itself */}
                    <div className="relative flex items-center justify-center w-full h-full">
                      {/* Active Node Effects */}
                      {state === 'active' && (
                        <>
                          <div className="absolute inset-0 rounded-full animate-ping opacity-20 bg-indigo-500" />
                          <div className="absolute -inset-4 rounded-full bg-indigo-500/10 dark:bg-indigo-500/20 blur-xl" />
                          <div className="absolute -inset-1 rounded-full border border-indigo-500/30" />
                        </>
                      )}

                      {/* Completed Badge */}
                      {state === 'completed' && (
                        <div className="absolute -top-1 -right-1 w-8 h-8 rounded-full bg-[#22C55E] flex items-center justify-center shadow-md z-20 border-[3px] border-white dark:border-[#0B0F19]">
                          <CheckCircle className="w-4 h-4 text-white" strokeWidth={3} />
                        </div>
                      )}

                      {/* Node Circle */}
                      <div 
                        className={`w-full h-full rounded-full flex items-center justify-center transition-transform duration-300 relative z-10 ${state === 'active' ? 'scale-105' : 'hover:scale-105'}`}
                        style={{
                          background: state === 'completed'
                            ? 'white'
                            : state === 'active'
                              ? 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)'
                              : 'white',
                          boxShadow: state === 'active'
                            ? '0 20px 40px -10px rgba(99,102,241,0.5), inset 0 2px 4px rgba(255,255,255,0.3)'
                            : state === 'completed'
                              ? '0 0 0 8px rgba(34,197,94,0.1), 0 10px 20px -5px rgba(0,0,0,0.05)'
                              : '0 0 0 4px rgba(226,232,240,0.5), 0 10px 20px -5px rgba(0,0,0,0.05)',
                          border: state === 'completed' ? '2px solid #22C55E' : state === 'locked' ? '2px solid #E2E8F0' : 'none',
                        }}
                      >
                        {/* Inner icon */}
                        {state === 'locked' ? (
                          <Lock className="w-8 h-8 text-slate-300 dark:text-slate-600" />
                        ) : state === 'completed' ? (
                          <Icon className="w-8 h-8 text-[#22C55E]" />
                        ) : (
                          <Icon className="w-10 h-10 text-white drop-shadow-md" />
                        )}
                      </div>
                      
                      {/* Active Start Lesson Button */}
                      {state === 'active' && activeLessonId && (
                        <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 translate-y-full z-30">
                          <Link
                            href={`/lessons/${activeLessonId}`}
                            className="flex items-center gap-2 px-6 py-3 rounded-full text-white text-sm font-bold shadow-xl transition-all hover:-translate-y-1 hover:shadow-2xl whitespace-nowrap"
                            style={{ 
                              background: 'linear-gradient(135deg, #4F46E5, #6366F1)',
                              boxShadow: '0 10px 25px -5px rgba(79,70,229,0.4), inset 0 1px 1px rgba(255,255,255,0.2)'
                            }}
                          >
                            Start Lesson <ArrowRight className="w-4 h-4" />
                          </Link>
                        </div>
                      )}
                    </div>

                    {/* Content Card Positioned Next to Node */}
                    <div 
                      className="absolute top-1/2 -translate-y-1/2 w-[280px] hidden sm:block"
                      style={{
                        [cardSide === 'left' ? 'right' : 'left']: '100%',
                        [cardSide === 'left' ? 'marginRight' : 'marginLeft']: state === 'active' ? '32px' : '24px',
                      }}
                    >
                      <div 
                        className="rounded-[24px] p-5 transition-all bg-white dark:bg-[#1E293B]"
                        style={{
                          opacity: state === 'locked' ? 0.6 : 1,
                          boxShadow: state === 'active' 
                            ? '0 20px 40px -10px rgba(0,0,0,0.05), 0 0 0 1px rgba(99,102,241,0.1)' 
                            : '0 10px 30px -10px rgba(0,0,0,0.03), 0 0 0 1px rgba(0,0,0,0.02)',
                          transform: state === 'active' ? 'scale(1.02)' : 'none',
                        }}
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <div className="w-1.5 h-5 rounded-full" style={{ background: state === 'completed' ? '#22C55E' : state === 'active' ? '#6366F1' : '#CBD5E1' }} />
                          <h3 className="text-[15px] font-bold text-slate-900 dark:text-white leading-tight">{idx + 1}. {mod.title}</h3>
                        </div>
                        <p className="text-[13px] mb-3 ml-3.5 text-slate-500 dark:text-slate-400 leading-relaxed">{desc}</p>
                        
                        {state === 'locked' ? (
                          <p className="text-[11px] font-black ml-3.5 text-slate-400 dark:text-slate-500 uppercase tracking-wider">Locked</p>
                        ) : (
                          <p className="text-[12px] font-bold ml-3.5" style={{ color: state === 'completed' ? '#22C55E' : '#6366F1' }}>
                            {done} / {mod.lessons.length} Lessons {state === 'completed' && 'Completed'}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  {/* Space for the active button */}
                  {state === 'active' && <div className="h-16 w-full" />}
                </div>
              );
            })}

            {/* Bottom dot trail */}
            <div className="flex flex-col items-center justify-center mt-12 gap-3 opacity-30">
              {[1, 2, 3].map(i => (
                <div key={i} className="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600" />
              ))}
            </div>
          </div>

          {/* ═══ RIGHT SIDEBAR ═══ */}
          <div className="space-y-6 shrink-0 relative z-20">
            {/* Course Progress */}
            <div className="rounded-[32px] p-8 bg-white dark:bg-[#1E293B] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 dark:border-white/5">
              <h3 className="text-lg font-black mb-8 text-slate-900 dark:text-white">Course Progress</h3>
              <div className="flex justify-center mb-8 relative">
                <div className="relative w-36 h-36">
                  <svg className="w-full h-full -rotate-90 drop-shadow-sm" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="42" fill="none" strokeWidth="10" className="stroke-slate-100 dark:stroke-slate-800" />
                    <circle 
                      cx="50" 
                      cy="50" 
                      r="42" 
                      fill="none" 
                      strokeWidth="10" 
                      stroke="#4F46E5" 
                      strokeLinecap="round" 
                      strokeDasharray={`${progressPct * 2.64} 264`} 
                      className="transition-all duration-1000 ease-out" 
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">{progressPct}%</span>
                    <span className="text-[11px] font-bold text-slate-400 mt-1 uppercase tracking-wider">Completed</span>
                  </div>
                </div>
              </div>
              <p className="text-[13px] font-medium text-slate-500 dark:text-slate-400 mb-1">Overall Progress</p>
              <p className="text-[15px] font-bold text-slate-900 dark:text-white mb-4">{completedLessons} / {totalLessons} Lessons</p>
              <div className="w-full h-2.5 rounded-full overflow-hidden bg-slate-100 dark:bg-slate-800">
                <div className="h-full rounded-full transition-all duration-1000 ease-out bg-[#4F46E5]" style={{ width: `${progressPct}%` }} />
              </div>
            </div>

            {/* Current Level */}
            <div className="rounded-[32px] p-8 bg-white dark:bg-[#1E293B] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 dark:border-white/5">
              <h3 className="text-lg font-black mb-6 text-slate-900 dark:text-white">Current Level</h3>
              <div className="flex items-center gap-5 mb-6">
                <div className="w-14 h-14 rounded-2xl flex items-center justify-center bg-blue-50 dark:bg-blue-500/10 border border-blue-100 dark:border-blue-500/20">
                  <Target className="w-7 h-7 text-blue-500" />
                </div>
                <div>
                  <p className="text-xl font-black text-slate-900 dark:text-white leading-tight">{stats?.level || 'A1'} Beginner</p>
                  <p className="text-[13px] font-medium text-slate-500 dark:text-slate-400 mt-1">CEFR Level</p>
                </div>
              </div>
              <p className="text-[13px] font-medium text-slate-500 dark:text-slate-400 mb-3">{completedLessons} / {totalLessons} Lessons Completed</p>
              <div className="w-full h-2.5 rounded-full overflow-hidden bg-slate-100 dark:bg-slate-800">
                <div className="h-full rounded-full transition-all duration-1000 ease-out bg-blue-500" style={{ width: `${progressPct}%` }} />
              </div>
            </div>

            {/* Daily Streak */}
            <div className="rounded-[32px] p-8 bg-white dark:bg-[#1E293B] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 dark:border-white/5">
              <h3 className="text-lg font-black mb-6 text-slate-900 dark:text-white">Daily Streak</h3>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center bg-orange-50 dark:bg-orange-500/10 border border-orange-100 dark:border-orange-500/20">
                  <Flame className="w-6 h-6 text-orange-500 fill-orange-500" />
                </div>
                <div>
                  <p className="text-2xl font-black text-slate-900 dark:text-white leading-tight">{stats?.streak || 0} Day</p>
                  <p className="text-[13px] font-medium text-slate-500 dark:text-slate-400 mt-0.5">Keep it up!</p>
                </div>
              </div>
              <div className="flex items-center gap-2 justify-between">
                {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((d, i) => {
                  const isActive = i === 0; // Mock logic, ideally based on real data
                  return (
                    <div key={i} className="flex flex-col items-center gap-2">
                      <div 
                        className={`w-9 h-9 rounded-full flex items-center justify-center text-[13px] font-bold transition-all
                          ${isActive 
                            ? 'bg-[#22C55E] text-white shadow-[0_4px_10px_rgba(34,197,94,0.3)]' 
                            : 'bg-slate-100 dark:bg-slate-800 text-slate-400'}`}
                      >
                        {isActive ? <CheckCircle className="w-4 h-4" strokeWidth={3} /> : d}
                      </div>
                      {!isActive && <span className="text-[10px] font-black text-slate-300 dark:text-slate-600 uppercase">{d}</span>}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* CTA */}
            <div 
              className="rounded-[32px] p-8 relative overflow-hidden group hover:-translate-y-1 transition-transform duration-300" 
              style={{ 
                background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
                boxShadow: '0 20px 40px -10px rgba(99,102,241,0.4), inset 0 1px 1px rgba(255,255,255,0.2)'
              }}
            >
              <div className="absolute top-0 right-0 p-6 opacity-20 transform translate-x-4 -translate-y-4 group-hover:scale-110 transition-transform duration-500">
                <Sparkles className="w-24 h-24 text-white" />
              </div>
              <div className="relative z-10">
                <div className="flex items-start gap-4 mb-6">
                  <div className="w-12 h-12 rounded-2xl bg-white/20 flex items-center justify-center shrink-0 backdrop-blur-sm border border-white/20">
                    <Sparkles className="w-6 h-6 text-white" />
                  </div>
                  <div className="pt-1">
                    <p className="text-white font-black text-lg leading-tight mb-1">Stay consistent!</p>
                    <p className="text-[13px] text-indigo-100 font-medium leading-relaxed">Practice every day to reach your goals faster.</p>
                  </div>
                </div>
                <Link href="/lessons" className="w-full flex items-center justify-center gap-2 bg-white text-[#4F46E5] px-6 py-4 rounded-2xl font-black text-[15px] hover:shadow-lg transition-all hover:bg-slate-50 group/btn">
                  Start Daily Session <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" strokeWidth={3} />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
