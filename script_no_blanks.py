from app.main import create_app
from app.database import db
from app.models.db_models import Course, Module, Lesson, Task
import random
app = create_app()
# Grammar and Vocabulary Data for different levels
GRAMMAR_DATA = {
    "Greetings": {
        "title": "Greetings & Basic Etiquette",
        "explanation": "Ағылшын тілінде амандасу ресми және бейресми болып бөлінеді. 'Hello' кез келген жерде қолданылады, ал 'Hi' достар арасында қолданылады. 'How are you?' сұрағына әдетте 'I am fine' деп жауап береміз.",
        "examples": [
            {"kaz": "Сәлем (ресми)", "eng": "Hello"},
            {"kaz": "Мен жақсымын", "eng": "I am fine"}
        ]
    },
    "Numbers": {
        "title": "Numbers 1-10",
        "explanation": "Сандар - тілдің негізі. Ағылшын тілінде 1-ден 10-ға дейінгі сандарды жаттау өте маңызды. Олар заттардың санын айтқанда қолданылады.",
        "examples": [
            {"kaz": "Бір алма", "eng": "One apple"},
            {"kaz": "Бес кітап", "eng": "Five books"}
        ]
    },
    "Family": {
        "title": "Family & Relationships",
        "explanation": "Отбасы мүшелерін атағанда 'My' (менің) сөзін қолданамыз. Мысалы: 'My mother' - Менің анам.",
        "examples": [
            {"kaz": "Менің әкем", "eng": "My father"},
            {"kaz": "Менің анам", "eng": "My mother"}
        ]
    },
    "Present Simple": {
        "title": "Present Simple (Осы шақ)",
        "explanation": "Present Simple күнделікті қайталанатын әрекеттер үшін қолданылады. Мысалы: 'I study English' (Мен ағылшынша оқимын - әрқашан).",
        "examples": [
            {"kaz": "Мен күнде жұмыс істеймін", "eng": "I work every day"},
            {"kaz": "Ол футбол ойнайды", "eng": "He plays football"}
        ]
    }
}
def generate_task(lesson_id, task_type, topic, level):
    # Mock data generation based on topic
    if task_type == "matching":
        pairs = [
            {"left": f"English {i}", "right": f"Қазақша {i}"} for i in range(1, 4)
        ]
        return Task(
            lesson_id=lesson_id,
            task_type="matching",
            content={"instruction": f"Match the {topic} vocabulary:", "pairs": pairs},
            order=1
        )
    elif task_type == "gaps":
        return Task(
            lesson_id=lesson_id,
            task_type="gaps",
            content={
                "sentences": [{
                    "prompt": f"Apply {topic} rule:",
                    "text": f"I [speak] English well.",
                    "options": ["speak", "speaks", "speaking", "spoken"],
                    "answer": "speak"
                }]
            },
            order=1
        )
    else: # ordering
        return Task(
            lesson_id=lesson_id,
            task_type="ordering",
            content={
                "sentences": [{
                    "prompt": f"Form a sentence about {topic}:",
                    "words": ["I", "love", "learning", "languages"],
                    "correct": "I love learning languages"
                }]
            },
            order=1
        )
def seed_level(course_title, level_code, topics):
    course = Course(
        title=course_title,
        description=f"{level_code} деңгейіндегі ағылшын тілі курсы. 20 грамматикалық тақырып және 60+ тест.",
        language="English",
        level=level_code
    )
    db.session.add(course)
    db.session.flush()
    for m_idx in range(10): # 10 modules
        module = Module(course_id=course.id, title=f"{level_code} Module {m_idx + 1}", order=m_idx + 1)
        db.session.add(module)
        db.session.flush()
        for l_idx in range(6): # 6 lessons per module = 60 lessons total
            topic_name = topics[(m_idx * 6 + l_idx) % len(topics)]
            theory = GRAMMAR_DATA.get(topic_name, {
                "title": f"Grammar: {topic_name}",
                "explanation": f"{topic_name} тақырыбы бойынша ережелер мен қолдану тәсілдері. Бұл жерде осы ереженің қашан және қалай қолданылатыны түсіндіріледі.",
                "examples": [{"kaz": f"Мысал {i}", "eng": f"Example {i}"} for i in range(1, 3)]
            })
            lesson = Lesson(
                module_id=module.id, 
                title=f"{topic_name}", 
                theory=theory,
                order=l_idx + 1
            )
            db.session.add(lesson)
            db.session.flush()
            # Add 3 tasks per lesson (1 matching vocab, 1 gaps grammar, 1 ordering sentence)
            db.session.add(generate_task(lesson.id, "matching", topic_name, level_code))
            db.session.add(generate_task(lesson.id, "gaps", topic_name, level_code))
            db.session.add(generate_task(lesson.id, "ordering", topic_name, level_code))
with app.app_context():
    db.create_all()
    print("Clearing database for clean scale...")
    Task.query.delete()
    Lesson.query.delete()
    Module.query.delete()
    Course.query.delete()
    db.session.commit()
    levels = [
        ("English A1: Beginner", "A1", ["Greetings", "Numbers", "Family", "Colors", "Food", "Animals"]),
        ("English A2: Elementary", "A2", ["Present Simple", "Past Simple", "Future Simple", "Comparatives"]),
        ("English B1: Intermediate", "B1", ["Present Perfect", "Modals", "Conditionals 1", "Passive Voice"]),
        ("English B2: Upper-Intermediate", "B2", ["Past Perfect", "Conditionals 2", "Reported Speech"]),
        ("English C1: Advanced", "C1", ["Cleft Sentences", "Inversion", "Advanced Phrasals"])
    ]
    for title, code, topics in levels:
        print(f"Generating {title}...")
        seed_level(title, code, topics)
    db.session.commit()
    print("Successfully generated A1-C1 curriculum with Grammar Theory!")
