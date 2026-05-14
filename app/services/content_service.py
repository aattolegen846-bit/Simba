from typing import List, Optional

from app.database import db
from app.models.db_models import Course, Lesson, Module, Task


class ContentService:
    @staticmethod
    def get_courses(language: Optional[str] = None) -> List[dict]:
        query = Course.query
        if language:
            query = query.filter_by(language=language)
        courses = query.all()
        return [
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "language": c.language,
                "level": c.level
            }
            for c in courses
        ]

    @staticmethod
    def get_course_details(course_id: int, user_id: int = None) -> dict:
        course = db.session.get(Course, course_id)
        if not course:
            return {}
        
        completed_lesson_ids = set()
        if user_id:
            from app.models.db_models import LessonSession
            completed_sessions = LessonSession.query.filter_by(user_id=user_id, status="completed").all()
            for s in completed_sessions:
                try:
                    completed_lesson_ids.add(int(s.lesson_id))
                except ValueError:
                    pass

        modules = Module.query.filter_by(course_id=course_id).order_by(Module.order).all()
        details = {
            "id": course.id,
            "title": course.title,
            "modules": []
        }
        
        is_previous_completed = True
        for m in modules:
            lessons = Lesson.query.filter_by(module_id=m.id).order_by(Lesson.order).all()
            module_lessons = []
            for l in lessons:
                is_completed = l.id in completed_lesson_ids
                is_locked = not is_previous_completed
                
                module_lessons.append({
                    "id": l.id,
                    "title": l.title,
                    "is_locked": is_locked,
                    "is_completed": is_completed
                })
                
                is_previous_completed = is_completed
                
            details["modules"].append({
                "id": m.id,
                "title": m.title,
                "lessons": module_lessons
            })
        return details

    @staticmethod
    def get_lesson_tasks(lesson_id: str, user_id: int = None) -> dict:
        is_dynamic = False
        try:
            lid = int(lesson_id)
        except ValueError:
            is_dynamic = True
            
        if is_dynamic:
            from sqlalchemy.sql.expression import func
            from app.models.db_models import LessonSession
            
            # Create a session if it doesn't exist (e.g. for fix_mistakes)
            if user_id:
                session = LessonSession.query.filter_by(lesson_id=str(lesson_id), user_id=user_id).first()
                if not session:
                    session = LessonSession(
                        lesson_id=str(lesson_id),
                        user_id=user_id,
                        focus_topic="dynamic_review",
                        current_level="a1",
                        status="started"
                    )
                    db.session.add(session)
                    db.session.commit()
            
            # Fetch random 5 tasks to act as the dynamic drill
            tasks = Task.query.order_by(func.random()).limit(5).all()
            return {
                "lesson_id": str(lesson_id),
                "title": "Smart Review Session",
                "tasks": [
                    {
                        "id": t.id,
                        "type": t.task_type,
                        "content": t.content
                    }
                    for t in tasks
                ]
            }
            
        lesson = db.session.get(Lesson, lid)
        if not lesson:
            return {}
            
        tasks = Task.query.filter_by(lesson_id=lid).order_by(Task.order).all()
        return {
            "lesson_id": lesson.id,
            "title": lesson.title,
            "theory": lesson.theory,
            "tasks": [
                {
                    "id": t.id,
                    "type": t.task_type,
                    "content": t.content
                }
                for t in tasks
            ]
        }

    @staticmethod
    def seed_demo_content():
        """
        Seeds the database with 'Super Pro Demo' content for investors.
        """
        if Course.query.first():
            return  # Already seeded
            
        # Course 1: English for IT
        it_english = Course(
            title="English for IT Professionals",
            description="Master technical communication and interview skills.",
            language="English",
            level="B2"
        )
        db.session.add(it_english)
        db.session.flush()
        
        mod1 = Module(course_id=it_english.id, title="The Agile Workflow", order=1)
        db.session.add(mod1)
        db.session.flush()
        
        les1 = Lesson(module_id=mod1.id, title="Daily Stand-ups", order=1)
        db.session.add(les1)
        db.session.flush()
        
        # Tasks for Lesson 1 (EdVibe style)
        tasks = [
            Task(
                lesson_id=les1.id,
                task_type="matching",
                content={
                    "instruction": "Match the meeting type to its purpose.",
                    "pairs": [
                        {"item": "Daily Stand-up", "match": "Status updates and blockers"},
                        {"item": "Sprint Review", "match": "Demoing the increment"},
                        {"item": "Retrospective", "match": "Process improvement"}
                    ]
                },
                order=1
            ),
            Task(
                lesson_id=les1.id,
                task_type="gaps",
                content={
                    "sentences": [{
                        "prompt": "Complete the developer update.",
                        "text": "Yesterday I [fixed] a bug in the auth module. Today I will [implement] the new API endpoint.",
                        "options": ["fixed", "implement", "deleted", "broken"],
                        "answer": "fixed"
                    }]
                },
                order=2
            )
        ]
        for t in tasks:
            db.session.add(t)
            
        lessons_it = [
            ("Bug Reports", [
                Task(task_type="gaps", content={
                    "sentences": [{
                        "prompt": "Fill in the correct term for describing a bug.",
                        "text": "The application [crashes] when I click the submit button.",
                        "options": ["crashes", "works", "compiles", "builds"],
                        "answer": "crashes"
                    }]
                }, order=1)
            ]),
            ("Code Review", [
                Task(task_type="ordering", content={
                    "sentences": [{
                        "prompt": "Order the sentence for a code review comment.",
                        "text": "Please add unit tests for this function.",
                        "words": ["Please", "add", "unit", "tests", "for", "this", "function."],
                        "correct": "Please add unit tests for this function."
                    }]
                }, order=1)
            ]),
            ("Sprint Planning", [
                Task(task_type="matching", content={
                    "instruction": "Match Agile terms to their definitions.",
                    "pairs": [
                        {"item": "Backlog", "match": "List of all desired work"},
                        {"item": "Sprint", "match": "Time-boxed iteration"},
                        {"item": "Story Point", "match": "Measure of effort"}
                    ]
                }, order=1)
            ]),
            ("Deployment", [
                Task(task_type="gaps", content={
                    "sentences": [{
                        "prompt": "Complete the deployment message.",
                        "text": "The new version has been [deployed] to production.",
                        "options": ["deployed", "deleted", "reverted", "hacked"],
                        "answer": "deployed"
                    }]
                }, order=1)
            ])
        ]
        
        for i, (title, extra_tasks) in enumerate(lessons_it):
            les = Lesson(module_id=mod1.id, title=title, order=i+2)
            db.session.add(les)
            db.session.flush()
            for t in extra_tasks:
                t.lesson_id = les.id
                db.session.add(t)
            
        # Course 2: Everyday Kazakh
        kazakh_daily = Course(
            title="Күнделікті Қазақ тілі",
            description="Базалық сөйлесу дағдылары.",
            language="Kazakh",
            level="A1"
        )
        db.session.add(kazakh_daily)
        db.session.flush()
        
        mod_k = Module(course_id=kazakh_daily.id, title="Танысу", order=1)
        db.session.add(mod_k)
        db.session.flush()
        
        les_k = Lesson(module_id=mod_k.id, title="Сәлемдесу", order=1)
        db.session.add(les_k)
        db.session.flush()
        
        task_k = Task(
            lesson_id=les_k.id,
            task_type="ordering",
            content={
                "sentences": [{
                    "prompt": "Put the greeting in the correct order.",
                    "words": ["Сәлем", "Қалың", "қалай?", "Жақсы,", "рахмет"],
                    "correct": "Сәлем Қалың қалай? Жақсы, рахмет"
                }]
            },
            order=1
        )
        db.session.add(task_k)
        
        lessons_k = [
            ("Отбасы", [
                Task(task_type="matching", content={
                    "instruction": "Match family members.",
                    "pairs": [
                        {"item": "Ана", "match": "Mother"},
                        {"item": "Әке", "match": "Father"},
                        {"item": "Аға", "match": "Older brother"}
                    ]
                }, order=1)
            ]),
            ("Дүкенде", [
                Task(task_type="gaps", content={
                    "sentences": [{
                        "prompt": "Ask for the price.",
                        "text": "Мынау қанша [тұрады]?",
                        "options": ["тұрады", "жасайды", "керек", "береді"],
                        "answer": "тұрады"
                    }]
                }, order=1)
            ]),
            ("Мейрамханада", [
                Task(task_type="ordering", content={
                    "sentences": [{
                        "prompt": "Order the food request.",
                        "words": ["Маған", "су", "әкеліңізші"],
                        "correct": "Маған су әкеліңізші"
                    }]
                }, order=1)
            ]),
            ("Жол сұрау", [
                Task(task_type="gaps", content={
                    "sentences": [{
                        "prompt": "Ask where the station is.",
                        "text": "Вокзал [қайда] орналасқан?",
                        "options": ["қайда", "қашан", "неге", "кім"],
                        "answer": "қайда"
                    }]
                }, order=1)
            ])
        ]
        
        for i, (title, extra_tasks) in enumerate(lessons_k):
            les = Lesson(module_id=mod_k.id, title=title, order=i+2)
            db.session.add(les)
            db.session.flush()
            for t in extra_tasks:
                t.lesson_id = les.id
                db.session.add(t)
        
        db.session.commit()
