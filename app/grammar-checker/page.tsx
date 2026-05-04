'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { Brain, ArrowLeft, Send, CheckCircle2, XCircle, Lightbulb, RefreshCw, Sparkles, Languages } from 'lucide-react';

interface GrammarResult {
  is_correct: boolean;
  explanation: string;
  corrections: string[];
  grammar_rules: string[];
}

export default function GrammarCheckerPage() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GrammarResult | null>(null);

  const checkGrammar = async () => {
    if (!text.trim()) {
      toast.error('Please enter a sentence to check');
      return;
    }

    setLoading(true);
    setResult(null);
    try {
      const response = await api.post('/grammar/check', { 
        sentence: text,
        language: 'kk' 
      });
      setResult(response.data);
    } catch (error) {
      toast.error('Failed to check grammar. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      {/* Header */}
      <nav className="bg-white border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <button 
            onClick={() => router.back()}
            className="p-2 hover:bg-gray-50 rounded-xl transition-colors group"
          >
            <ArrowLeft className="w-6 h-6 text-gray-400 group-hover:text-indigo-600" />
          </button>
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-black text-gray-900">Grammar <span className="text-indigo-600">Checker</span></span>
          </div>
          <div className="w-10" /> {/* Spacer */}
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-black text-gray-900 mb-4">Master Your Grammar</h1>
          <p className="text-gray-500 font-medium text-lg">Type any sentence in Kazakh and our AI will analyze its structure for you.</p>
        </div>

        <div className="space-y-8">
          {/* Input Area */}
          <div className="bg-white rounded-[32px] p-8 shadow-sm border border-gray-100">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Мұнда сөйлемді жазыңыз... (e.g., Мен мектепке барамын)"
              className="w-full min-h-[150px] text-2xl font-bold text-gray-900 placeholder:text-gray-200 focus:outline-none resize-none"
            />
            
            <div className="flex items-center justify-between mt-8 pt-8 border-t border-gray-50">
              <div className="flex items-center space-x-2 text-gray-400">
                <Languages className="w-5 h-5" />
                <span className="text-sm font-bold uppercase tracking-widest">Kazakh (KK)</span>
              </div>
              
              <button
                onClick={checkGrammar}
                disabled={loading || !text.trim()}
                className="premium-button flex items-center space-x-3 !py-4 disabled:opacity-50 disabled:grayscale"
              >
                {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
                <span>{loading ? 'Analyzing...' : 'Check Grammar'}</span>
              </button>
            </div>
          </div>

          {/* Result Area */}
          {result && (
            <div className="space-y-6 animate-in slide-in-from-bottom-8 duration-500">
              <div className={`p-8 rounded-[32px] border-b-8 shadow-xl ${result.is_correct ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                <div className="flex items-center space-x-4 mb-6">
                  {result.is_correct ? (
                    <CheckCircle2 className="w-10 h-10 text-green-500" />
                  ) : (
                    <XCircle className="w-10 h-10 text-red-500" />
                  )}
                  <h2 className={`text-2xl font-black ${result.is_correct ? 'text-green-700' : 'text-red-700'}`}>
                    {result.is_correct ? 'Perfect Sentence!' : 'Needs Improvement'}
                  </h2>
                </div>
                
                <p className={`text-lg font-medium leading-relaxed ${result.is_correct ? 'text-green-800' : 'text-red-800'}`}>
                  {result.explanation}
                </p>
              </div>

              {result.corrections.length > 0 && (
                <div className="bg-white p-8 rounded-[32px] border border-gray-100 shadow-sm">
                  <h3 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-6 flex items-center">
                    <CheckCircle2 className="w-4 h-4 mr-2 text-indigo-500" />
                    Suggested Corrections
                  </h3>
                  <div className="space-y-4">
                    {result.corrections.map((correction, i) => (
                      <div key={i} className="p-4 bg-indigo-50 rounded-2xl text-xl font-bold text-indigo-700 border border-indigo-100">
                        {correction}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {result.grammar_rules.length > 0 && (
                <div className="bg-white p-8 rounded-[32px] border border-gray-100 shadow-sm">
                  <h3 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-6 flex items-center">
                    <Lightbulb className="w-4 h-4 mr-2 text-orange-500" />
                    Key Grammar Rules
                  </h3>
                  <div className="flex flex-wrap gap-3">
                    {result.grammar_rules.map((rule, i) => (
                      <span key={i} className="px-4 py-2 bg-orange-50 text-orange-700 rounded-full text-sm font-bold border border-orange-100">
                        {rule}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
