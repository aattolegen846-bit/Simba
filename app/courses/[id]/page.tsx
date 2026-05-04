'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/lib/store';
import toast from 'react-hot-toast';
import { Brain, BookOpen, ArrowLeft, Play } from 'lucide-react';
import Link from 'next/link';

interface Module {
  id: number;
  title: string;
  lessons: Lesson[];
}

interface Lesson {
  id: number;
  title: string;
}

interface CourseDetails {
  id: number;
  title: string;
  modules: Module[];
}

export default function CoursePage() {
  const router = useRouter();
  const params = useParams();
  const { user } = useAuthStore();
  const [course, setCourse] = useState<CourseDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }

    const fetchCourse = async () => {
      try {
        const response = await api.get(`/courses/${params.id}`);
        setCourse(response.data);
      } catch (error) {
        toast.error('Failed to load course');
      } finally {
        setLoading(false);
      }
    };

    fetchCourse();
  }, [user, router, params.id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading course...</div>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-xl text-gray-600">Course not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center space-x-4">
          <Link href="/courses" className="text-gray-600 hover:text-indigo-600">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div className="flex items-center space-x-2">
            <Brain className="w-8 h-8 text-indigo-600" />
            <span className="text-2xl font-bold text-gray-900">Simba</span>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">{course.title}</h1>

        {course.modules.length === 0 ? (
          <div className="bg-white p-8 rounded-xl shadow-md text-center">
            <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No modules available yet.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {course.modules.map((module) => (
              <div key={module.id} className="bg-white p-6 rounded-xl shadow-md">
                <h2 className="text-2xl font-semibold text-gray-900 mb-4">{module.title}</h2>

                {module.lessons.length === 0 ? (
                  <p className="text-gray-500">No lessons in this module yet.</p>
                ) : (
                  <div className="space-y-3">
                    {module.lessons.map((lesson) => (
                      <Link
                        key={lesson.id}
                        href={`/lessons/${lesson.id}`}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-indigo-50 transition-colors group"
                      >
                        <div className="flex items-center space-x-3">
                          <BookOpen className="w-5 h-5 text-indigo-600" />
                          <span className="font-medium text-gray-900">{lesson.title}</span>
                        </div>
                        <Play className="w-5 h-5 text-gray-400 group-hover:text-indigo-600" />
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
