from app.main import create_app
from app.database import db
from app.models.db_models import Course, Module, Lesson, Task

app = create_app()

with app.app_context():
    # 1. English for IT Course
    it_english = Course.query.filter_by(title="English for IT Professionals").first()
    if it_english:
        mod1 = Module.query.filter_by(course_id=it_english.id, title="The Agile Workflow").first()
        if mod1:
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
            
            for i, (title, tasks) in enumerate(lessons_it):
                les = Lesson(module_id=mod1.id, title=title, order=i+2) # order starts from 2
                db.session.add(les)
                db.session.flush()
                for t in tasks:
                    t.lesson_id = les.id
                    db.session.add(t)

    # 2. Everyday Kazakh Course
    kazakh_daily = Course.query.filter_by(title="Күнделікті Қазақ тілі").first()
    if kazakh_daily:
        mod_k = Module.query.filter_by(course_id=kazakh_daily.id, title="Танысу").first()
        if mod_k:
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
            
            for i, (title, tasks) in enumerate(lessons_k):
                les = Lesson(module_id=mod_k.id, title=title, order=i+2)
                db.session.add(les)
                db.session.flush()
                for t in tasks:
                    t.lesson_id = les.id
                    db.session.add(t)

    db.session.commit()
    print("Added additional lessons successfully.")
