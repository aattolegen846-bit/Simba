'use client';

import { useEffect, useState, useCallback, useMemo } from 'react';
import { useRouter, useParams } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { X, CheckCircle, ArrowRight, Trophy, BookOpen, Brain, Sparkles, Zap, ShieldCheck, Heart, Info, Loader2, MessageCircle } from 'lucide-react';
import Link from 'next/link';

// --- THEORY COMPONENT ---
function TheoryCard({ theory, onStart }: { theory: any, onStart: () => void }) {
  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col items-center justify-center p-6">
      <div className="max-w-2xl w-full bg-white rounded-[32px] shadow-2xl border-2 border-gray-100 overflow-hidden animate-in zoom-in duration-500">
        <div className="bg-indigo-600 p-8 text-white">
          <div className="flex items-center space-x-3 mb-4">
            <Info className="w-6 h-6" />
            <span className="text-sm font-black uppercase tracking-widest opacity-80">Grammar Focus</span>
          </div>
          <h1 className="text-3xl font-black">{theory.title}</h1>
        </div>
        
        <div className="p-8 space-y-8">
          <div className="space-y-4">
            <p className="text-xl text-gray-700 leading-relaxed font-medium">
              {theory.explanation}
            </p>
          </div>

          {theory.examples && (
            <div className="space-y-4">
              <h3 className="text-sm font-black text-gray-400 uppercase tracking-widest">EXAMPLES</h3>
              <div className="grid gap-4">
                {theory.examples.map((ex: any, i: number) => (
                  <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl border border-gray-100">
                    <span className="text-xl font-bold text-gray-900">{ex.kaz}</span>
                    <ArrowRight className="w-5 h-5 text-gray-300" />
                    <span className="text-lg font-medium text-indigo-600">{ex.eng}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={onStart}
            className="w-full py-5 bg-[#58CC02] text-white rounded-2xl text-xl font-black shadow-[0_6px_0_#46A302] hover:bg-[#46A302] transition-all transform active:translate-y-1 mt-8"
          >
            I UNDERSTAND
          </button>
        </div>
      </div>
    </div>
  );
}

interface Task {
  id: number;
  type: 'matching' | 'gaps' | 'ordering';
  skill: string;
  content: any;
}

interface LessonData {
  lesson_id: string;
  title: string;
  tasks: Task[];
}

interface TaskResult {
  skill: string;
  is_correct: boolean;
  user_answer: string;
  expected_answer: string;
}

// --- TASK COMPONENTS ---

function OrderingTask({ sentence, onStatusChange, isChecked, isCorrect }: { 
  sentence: any, 
  onStatusChange: (answer: string, correct: boolean) => void,
  isChecked: boolean,
  isCorrect: boolean
}) {
  const [selectedWords, setSelectedWords] = useState<string[]>([]);
  const [availableWords, setAvailableWords] = useState<string[]>(sentence.words);

  const handleWordClick = (word: string, widx: number) => {
    if (isChecked) return;
    const newSelected = [...selectedWords, word];
    setSelectedWords(newSelected);
    const newAvailable = [...availableWords];
    newAvailable.splice(widx, 1);
    setAvailableWords(newAvailable);
    
    const currentAnswer = newSelected.join(' ');
    onStatusChange(currentAnswer, currentAnswer === sentence.correct);
  };

  const handleReset = () => {
    if (isChecked) return;
    setSelectedWords([]);
    setAvailableWords(sentence.words);
    onStatusChange('', false);
  };

  return (
    <div className="space-y-8 py-4 animate-in zoom-in duration-300">
      {sentence.prompt && (
        <div className="bg-white border-2 border-gray-100 p-8 rounded-3xl shadow-sm mb-8">
          <p className="text-sm font-black text-indigo-600 uppercase tracking-widest mb-2">PROMPT</p>
          <p className="text-3xl font-bold text-gray-900 text-center">{sentence.prompt}</p>
        </div>
      )}
      <div className="space-y-8 text-center">
      <div className={`min-h-[120px] p-6 rounded-3xl border-3 transition-all duration-500 flex flex-wrap justify-center items-center gap-3 ${isChecked ? (isCorrect ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200') : 'bg-white border-gray-200 border-b-6 shadow-inner'}`}>
        {selectedWords.length === 0 && !isChecked && (
          <span className="text-gray-400 font-medium italic">Tap words below to build the sentence...</span>
        )}
        {selectedWords.map((word, idx) => (
          <div key={idx} className={`px-6 py-3 border-b-4 text-xl font-bold rounded-2xl shadow-sm transition-all ${isChecked ? (isCorrect ? 'bg-green-500 border-green-700 text-white' : 'bg-red-500 border-red-700 text-white') : 'bg-white border-indigo-100 text-indigo-700'}`}>
            {word}
          </div>
        ))}
      </div>

      <div className="flex flex-wrap justify-center gap-3">
        {availableWords.map((word, idx) => (
          <button key={idx} onClick={() => handleWordClick(word, idx)} disabled={isChecked} className="px-6 py-3 bg-white border-b-4 border-gray-200 text-xl font-bold text-gray-700 rounded-2xl shadow-sm hover:bg-gray-50 active:translate-y-1 transition-all disabled:opacity-50">
            {word}
          </button>
        ))}
      </div>
      
      {!isChecked && selectedWords.length > 0 && (
        <button onClick={handleReset} className="text-sm font-black text-gray-400 hover:text-indigo-600 transition-colors uppercase tracking-widest">
          Reset Order
        </button>
      )}
      </div>
    </div>
  );
}

function GapsTask({ sentence, onStatusChange, isChecked, isCorrect }: {
  sentence: any,
  onStatusChange: (answer: string, correct: boolean) => void,
  isChecked: boolean,
  isCorrect: boolean
}) {
  const [inputValue, setInputValue] = useState('');

  const handleChange = (val: string) => {
    setInputValue(val);
    onStatusChange(val, val.toLowerCase().trim() === sentence.answer.toLowerCase().trim());
  };

  const parts = sentence.text.replace(/\[.*?\]/g, '___').split('___');

  return (
    <div className="space-y-8 py-4">
      {sentence.prompt && (
        <div className="bg-white border-2 border-gray-100 p-8 rounded-3xl shadow-sm">
          <p className="text-sm font-black text-indigo-600 uppercase tracking-widest mb-2">PROMPT</p>
          <p className="text-3xl font-bold text-gray-900">{sentence.prompt}</p>
        </div>
      )}
      <div className="text-center space-y-6">
        <p className="text-3xl font-bold text-gray-900 leading-relaxed">
          {parts.map((part: string, i: number) => (
            <span key={i}>
              {part}
              {i < parts.length - 1 && (
                <span className="inline-block w-32 border-b-4 border-gray-200 mx-2 -mb-1"></span>
              )}
            </span>
          ))}
        </p>
        <input
          type="text"
          placeholder="Type the missing word..."
          disabled={isChecked}
          value={inputValue}
          onChange={(e) => handleChange(e.target.value)}
          className={`w-full px-8 py-6 text-2xl font-bold text-center border-b-8 rounded-3xl transition-all ${isChecked ? (isCorrect ? 'bg-green-50 border-green-200 text-green-700' : 'bg-red-50 border-red-200 text-red-700') : 'bg-white border-gray-100 focus:border-indigo-400 focus:bg-indigo-50 outline-none shadow-xl'}`}
        />
      </div>
    </div>
  );
}

function MatchingTask({ pairs, isChecked, onStatusChange }: { pairs: any[], isChecked: boolean, onStatusChange: (val: string, correct: boolean) => void }) {
  const [leftWords, setLeftWords] = useState<{id: number, text: string}[]>([]);
  const [rightWords, setRightWords] = useState<{id: number, text: string}[]>([]);
  const [selectedLeft, setSelectedLeft] = useState<number | null>(null);
  const [selectedRight, setSelectedRight] = useState<number | null>(null);
  const [matchedIds, setMatchedIds] = useState<number[]>([]);
  const [wrongMatch, setWrongMatch] = useState<{left: number, right: number} | null>(null);

  useEffect(() => {
    const left = pairs.map((p, i) => ({ id: i, text: p.left })).sort(() => Math.random() - 0.5);
    const right = pairs.map((p, i) => ({ id: i, text: p.right })).sort(() => Math.random() - 0.5);
    setLeftWords(left);
    setRightWords(right);
  }, [pairs]);

  useEffect(() => {
    if (selectedLeft !== null && selectedRight !== null) {
      if (selectedLeft === selectedRight) {
        setMatchedIds(prev => [...prev, selectedLeft]);
        setSelectedLeft(null);
        setSelectedRight(null);
        if (matchedIds.length + 1 === pairs.length) {
          onStatusChange('completed', true);
        }
      } else {
        setWrongMatch({ left: selectedLeft, right: selectedRight });
        setTimeout(() => {
          setWrongMatch(null);
          setSelectedLeft(null);
          setSelectedRight(null);
        }, 500);
      }
    }
  }, [selectedLeft, selectedRight, matchedIds, pairs.length, onStatusChange]);

  return (
    <div className="space-y-8 py-4">
      <div className="grid grid-cols-2 gap-8">
        {/* Left Column */}
        <div className="space-y-4">
          {leftWords.map((word) => (
            <button
              key={`left-${word.id}`}
              disabled={matchedIds.includes(word.id) || isChecked}
              onClick={() => setSelectedLeft(word.id)}
              className={`w-full p-6 text-lg font-bold rounded-2xl border-2 transition-all transform active:scale-95
                ${matchedIds.includes(word.id) ? 'bg-gray-50 border-gray-100 text-gray-300 opacity-50' : 
                  selectedLeft === word.id ? 'bg-indigo-50 border-indigo-400 text-indigo-600 shadow-inner' : 
                  wrongMatch?.left === word.id ? 'bg-red-50 border-red-400 text-red-600 animate-shake' :
                  'bg-white border-gray-100 hover:border-gray-200 shadow-sm'}`}
            >
              {word.text}
            </button>
          ))}
        </div>

        {/* Right Column */}
        <div className="space-y-4">
          {rightWords.map((word) => (
            <button
              key={`right-${word.id}`}
              disabled={matchedIds.includes(word.id) || isChecked}
              onClick={() => setSelectedRight(word.id)}
              className={`w-full p-6 text-lg font-bold rounded-2xl border-2 transition-all transform active:scale-95
                ${matchedIds.includes(word.id) ? 'bg-gray-50 border-gray-100 text-gray-300 opacity-50' : 
                  selectedRight === word.id ? 'bg-indigo-50 border-indigo-400 text-indigo-600 shadow-inner' : 
                  wrongMatch?.right === word.id ? 'bg-red-50 border-red-400 text-red-600 animate-shake' :
                  'bg-white border-gray-100 hover:border-gray-200 shadow-sm'}`}
            >
              {word.text}
            </button>
          ))}
        </div>
      </div>

      {matchedIds.length === pairs.length && (
        <div className="p-6 bg-green-50 rounded-3xl border-b-4 border-green-200 flex items-start space-x-4 animate-in slide-in-from-bottom duration-300">
          <ShieldCheck className="w-6 h-6 text-green-600 mt-1" />
          <div>
            <p className="text-sm font-black text-green-900 uppercase tracking-widest mb-1">Excellent!</p>
            <p className="text-sm text-green-700 font-medium">You've matched all pairs correctly. Click continue to proceed.</p>
          </div>
        </div>
      )}
    </div>
  );
}

// --- MAIN COMPONENT ---

export default function LessonPage() {
  const router = useRouter();
  const params = useParams();
  const { user } = useAuthStore();
  
  const [lesson, setLesson] = useState<LessonData | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [currentTaskIdx, setCurrentTaskIdx] = useState(0);
  const [results, setResults] = useState<TaskResult[]>([]);
  const [isCompleted, setIsCompleted] = useState(false);
  const [summaryData, setSummaryData] = useState<any>(null);

  // Per-task state managed in Parent
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [isCorrect, setIsCorrect] = useState(false);
  const [isChecked, setIsChecked] = useState(false);
  const [showTheory, setShowTheory] = useState(true);

  // AI Chat states
  const [showAiChat, setShowAiChat] = useState(false);
  const [aiMessage, setAiMessage] = useState('');

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchLesson = async () => {
      try {
        const response = await api.get(`/lessons/${params.id}/tasks`);
        setLesson(response.data);
      } catch (error) {
        toast.error('Failed to load lesson tasks');
      } finally {
        setLoading(false);
      }
    };

    fetchLesson();
  }, [user, router, params.id]);

  const handleStatusChange = (answer: string, correct: boolean) => {
    setCurrentAnswer(answer);
    setIsCorrect(correct);
  };

  const handleCheck = () => {
    if (isChecked) {
      handleNext();
      return;
    }
    
    setIsChecked(true);
    const task = lesson!.tasks[currentTaskIdx];
    
    // Auto-correct for matching tasks as they are for learning
    const finalCorrect = task.type === 'matching' ? true : isCorrect;
    if (task.type === 'matching') setIsCorrect(true);
    
    setResults(prev => [...prev, {
      skill: task.skill || 'general',
      is_correct: finalCorrect,
      user_answer: currentAnswer || 'viewed',
      expected_answer: task.type === 'matching' ? 'viewed' : (task.content.sentences?.[0]?.answer || task.content.sentences?.[0]?.correct)
    }]);
  };

  const handleNext = async () => {
    if (!lesson) return;

    if (currentTaskIdx < lesson.tasks.length - 1) {
      setCurrentTaskIdx(currentTaskIdx + 1);
      setIsChecked(false);
      setCurrentAnswer('');
      setIsCorrect(false);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      await finishLesson();
    }
  };

  const finishLesson = async () => {
    setSubmitting(true);
    try {
      const response = await api.post('/quiz/submit', {
        lesson_id: lesson!.lesson_id,
        results: results,
        current_level: user?.level || 'a1',
        available_minutes: 30
      });
      setSummaryData(response.data);

      // Award XP for completing the lesson
      const correctCount = results.filter(r => r.is_correct).length;
      const xpToAward = correctCount * 10; // 10 XP per correct answer

      try {
        await api.post('/progress/award-xp', {
          xp_delta: xpToAward
        });
        toast.success(`+${xpToAward} XP earned!`);
      } catch (xpError) {
        console.error('Failed to award XP:', xpError);
      }

      setIsCompleted(true);
    } catch (error: any) {
      toast.error('Failed to save progress');
      setIsCompleted(true);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-white"><Loader2 className="w-12 h-12 animate-spin text-indigo-600" /></div>;
  if (!lesson || isCompleted) return <CompletionScreen lesson={lesson} summaryData={summaryData} />;

  if (showTheory && lesson.theory && currentTaskIdx === 0) {
    return <TheoryCard theory={lesson.theory} onStart={() => setShowTheory(false)} />;
  }

  const task = lesson.tasks[currentTaskIdx];
  const progress = ((currentTaskIdx + 1) / lesson.tasks.length) * 100;

  return (
    <div className="min-h-screen bg-white pb-32">
      {/* Header */}
      <nav className="max-w-5xl mx-auto px-6 py-8">
        <div className="flex items-center space-x-6">
          <button onClick={() => router.push('/dashboard')} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <X className="w-7 h-7 text-gray-400" />
          </button>
          <div className="flex-1 relative h-4 bg-gray-100 rounded-full overflow-hidden">
            <div 
              className="absolute top-0 left-0 h-full bg-gradient-to-r from-[#58CC02] to-[#46A302] transition-all duration-700 ease-out"
              style={{ width: `${progress}%` }}
            >
              <div className="w-full h-full progress-bar-shine opacity-30"></div>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Heart className="w-7 h-7 text-[#FF4B4B] fill-[#FF4B4B]" />
            <span className="text-xl font-black text-[#FF4B4B]">5</span>
          </div>
        </div>
      </nav>

      <main className="max-w-3xl mx-auto px-6 py-12">
        <div className="mb-12">
          <div className="flex items-center space-x-4 mb-4">
            <div className="w-16 h-16 bg-white border-2 border-gray-100 rounded-3xl shadow-sm flex items-center justify-center">
              <img src="/logo.png" alt="Simba" className="w-12 h-12 object-contain" />
            </div>
            <div className="relative bg-white border-2 border-gray-100 p-4 rounded-2xl rounded-tl-none shadow-sm">
              <p className="text-xl font-bold text-gray-800 leading-tight">
                {task.content?.instruction || "Salem! Follow the task instructions."}
              </p>
              <div className="absolute top-0 -left-2 w-0 h-0 border-t-[8px] border-t-transparent border-r-[12px] border-r-white border-b-[8px] border-b-transparent"></div>
            </div>
          </div>
        </div>

        {/* Task Area */}
        <div className="min-h-[300px]">
          {task.type === 'matching' && <MatchingTask pairs={task.content.pairs} isChecked={isChecked} onStatusChange={handleStatusChange} />}
          {task.type === 'gaps' && (
            <GapsTask 
              sentence={task.content.sentences[0]} 
              onStatusChange={handleStatusChange} 
              isChecked={isChecked} 
              isCorrect={isCorrect} 
            />
          )}
          {task.type === 'ordering' && (
            <OrderingTask 
              sentence={task.content.sentences[0]} 
              onStatusChange={handleStatusChange} 
              isChecked={isChecked} 
              isCorrect={isCorrect} 
            />
          )}
        </div>
      </main>

      {/* Duolingo Style Bottom Bar */}
      <div className={`fixed bottom-0 left-0 right-0 py-10 transition-all duration-300 border-t-2 ${isChecked ? (isCorrect ? 'bg-[#D7FFB8] border-[#A8E08B]' : 'bg-[#FFDFE0] border-[#F2B0B0]') : 'bg-white border-gray-100'}`}>
        <div className="max-w-4xl mx-auto px-6 flex items-center justify-between">
          <div className="flex-1">
            {isChecked && (
              <div className="flex items-center space-x-4 animate-in slide-in-from-bottom-4">
                <div className={`w-14 h-14 rounded-full flex items-center justify-center ${isCorrect ? 'bg-white text-[#58CC02]' : 'bg-white text-[#EA2B2B]'}`}>
                  {isCorrect ? <CheckCircle className="w-8 h-8" /> : <X className="w-8 h-8" />}
                </div>
                <div>
                  <p className={`text-2xl font-black ${isCorrect ? 'text-[#58CC02]' : 'text-[#EA2B2B]'}`}>
                    {isCorrect ? 'Excellent work!' : 'Not quite right'}
                  </p>
                  {!isCorrect && (
                    <p className="text-[#EA2B2B] font-bold text-sm">
                      Correct answer: <span className="underline">{task.content.sentences?.[0]?.answer || task.content.sentences?.[0]?.correct}</span>
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>
          <button 
            onClick={handleCheck}
            disabled={!currentAnswer && !isChecked && task.type !== 'matching'}
            className={`px-12 py-4 rounded-2xl text-xl font-black transition-all transform active:scale-95 ${isChecked ? (isCorrect ? 'bg-[#58CC02] hover:bg-[#46A302] text-white shadow-[0_4px_0_#46A302]' : 'bg-[#FF4B4B] hover:bg-[#EA2B2B] text-white shadow-[0_4px_0_#EA2B2B]') : (currentAnswer || task.type === 'matching' ? 'bg-[#58CC02] text-white shadow-[0_4px_0_#46A302]' : 'bg-[#E5E5E5] text-[#AFAFAF] cursor-not-allowed')}`}
          >
            {isChecked ? 'CONTINUE' : 'CHECK'}
          </button>
        </div>
      </div>

      {/* AI Assistant Button (Floating) */}
      <button 
        onClick={() => setShowAiChat(!showAiChat)}
        className="fixed bottom-36 right-8 w-14 h-14 bg-white border-2 border-gray-100 rounded-2xl shadow-lg flex items-center justify-center hover:bg-gray-50 transition-all z-40"
      >
        <MessageCircle className="w-7 h-7 text-indigo-600" />
      </button>

      {showAiChat && (
        <div className="fixed bottom-36 right-24 w-80 bg-white border-2 border-gray-100 rounded-3xl shadow-2xl p-6 z-50 animate-in fade-in slide-in-from-right-4">
          <p className="text-sm font-bold text-gray-900 mb-4">Simba Assistant 🦁</p>
          <div className="bg-indigo-50 p-4 rounded-2xl mb-4 text-sm text-indigo-700 leading-relaxed">
            "Ask me to explain any word or rule in this task!"
          </div>
          <div className="flex space-x-2">
            <input 
              type="text" 
              placeholder="Ask anything..." 
              className="flex-1 bg-gray-50 border-none rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-indigo-500"
              value={aiMessage}
              onChange={(e) => setAiMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAiAsk()}
            />
            <button onClick={handleAiAsk} className="p-2 bg-indigo-600 text-white rounded-xl"><Send className="w-4 h-4" /></button>
          </div>
        </div>
      )}
    </div>
  );

  async function handleAiAsk() {
    if (!aiMessage.trim()) return;
    const loadingToast = toast.loading('Consulting Simba...');
    try {
      const response = await api.post('/ai/explain', {
        sentence: aiMessage,
        target_language: 'Kazakh',
        native_language: 'English'
      });
      toast.dismiss(loadingToast);
      setAiMessage('');
      toast.success(response.data.explanation, { duration: 8000, icon: '🦁' });
    } catch (e) {
      toast.dismiss(loadingToast);
      toast.error('Simba is taking a nap.');
    }
  }
}

function CompletionScreen({ lesson, summaryData }: { lesson: LessonData | null, summaryData: any }) {
  const router = useRouter();
  const xp = summaryData?.progress?.xp_earned || 150;
  const accuracy = summaryData?.score ? Math.round((summaryData.score / summaryData.total_questions) * 100) : 100;

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-6">
      <div className="max-w-md w-full text-center space-y-8 animate-in zoom-in duration-500">
        <Trophy className="w-32 h-32 text-[#FFD700] mx-auto animate-bounce" />
        <h1 className="text-4xl font-black text-[#58CC02] tracking-tight">LESSON COMPLETE!</h1>
        <p className="text-xl text-gray-500 font-bold">You've mastered <span className="text-gray-900">{lesson?.title}</span></p>
        
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-[#58CC02]/10 p-6 rounded-3xl border-b-4 border-[#58CC02]/20">
            <p className="text-xs font-black text-[#58CC02] uppercase tracking-widest mb-1">TOTAL XP</p>
            <p className="text-4xl font-black text-[#58CC02]">+{xp}</p>
          </div>
          <div className="bg-[#1CB0F6]/10 p-6 rounded-3xl border-b-4 border-[#1CB0F6]/20">
            <p className="text-xs font-black text-[#1CB0F6] uppercase tracking-widest mb-1">ACCURACY</p>
            <p className="text-4xl font-black text-[#1CB0F6]">{accuracy}%</p>
          </div>
        </div>

        <button 
          onClick={() => router.push('/dashboard')}
          className="w-full py-5 bg-[#1CB0F6] text-white rounded-2xl text-xl font-black shadow-[0_6px_0_#1899D6] hover:bg-[#1899D6] transition-all transform active:translate-y-1"
        >
          CONTINUE
        </button>
      </div>
    </div>
  );
}
