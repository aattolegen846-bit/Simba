"""B2 Upper-Intermediate English curriculum for Kazakh speakers. 10 lessons."""
import os
os.environ.setdefault("SECRET_KEY", "dev")
os.environ.setdefault("WEBHOOK_SECRET", "dev")
from app.main import create_app
from app.database import db
from app.models.db_models import Course, Module, Lesson, Task

app = create_app()

def match(i, p):
    return Task(task_type="matching", content={"instruction": i, "pairs": p}, order=0)
def gaps(p, t, o, a):
    return Task(task_type="gaps", content={"sentences": [{"prompt": p, "text": t, "options": o, "answer": a}]}, order=0)
def order(p, w, c):
    return Task(task_type="ordering", content={"sentences": [{"prompt": p, "words": w, "correct": c}]}, order=0)

B2_MODULES = [
  {
    "title": "Advanced Grammar",
    "lessons": [
      {
        "title": "Reported Speech",
        "theory": {
          "title": "Төлеу сөз — Reported Speech",
          "explanation": "Біреудің сөзін жеткізу: He said that... Тура сөзден төлеу сөзге ауысу: 'I am happy' → He said he was happy. Шақ бір қадам артқа жылжиды: am→was, will→would, can→could.",
          "examples": [
            {"kaz": "Ол 'Мен бақыттымын' деді.", "eng": "He said that he was happy."},
            {"kaz": "Ол 'Мен ертең келемін' деді.", "eng": "She said she would come tomorrow."},
            {"kaz": "Олар 'Біз ағылшынша сөйлей аламыз' деді.", "eng": "They said they could speak English."}
          ]
        },
        "tasks": [
          match("Тура сөзден төлеу сөзге ауысуды сәйкестендіріңіз:", [
            {"item": "am / is", "match": "was"},
            {"item": "are", "match": "were"},
            {"item": "will", "match": "would"},
            {"item": "can", "match": "could"},
            {"item": "have", "match": "had"}
          ]),
          gaps("Reported Speech формасын таңдаңыз:", "He said he [was] happy.", ["was", "is", "am", "be"], "was"),
          gaps("Reported Speech формасын таңдаңыз:", "She said she [would] come tomorrow.", ["would", "will", "can", "shall"], "would"),
          gaps("Reported Speech формасын таңдаңыз:", "They said they [could] speak English.", ["could", "can", "will", "are"], "could"),
          order("Сөйлемді құрастырыңыз:", ["said", "He", "that", "he", "was", "tired", "."], "He said that he was tired."),
          order("Сөйлемді құрастырыңыз:", ["said", "She", "she", "would", "help", "me", "."], "She said she would help me.")
        ]
      },
      {
        "title": "Second Conditional",
        "theory": {
          "title": "Екінші шартты сөйлем — Second Conditional",
          "explanation": "'If + Past Simple, would + V1' — нақты емес, қиялдағы жағдай. 'If I had money, I would travel.' — Менде ақша болса, саяхаттар едім. 'If I were you...' — Сенің орнында болсам...",
          "examples": [
            {"kaz": "Менде ақша болса, саяхаттар едім.", "eng": "If I had money, I would travel."},
            {"kaz": "Ол ұшақ болса, ұша алар еді.", "eng": "If he had a plane, he could fly."},
            {"kaz": "Сенің орнында болсам, оқыр едім.", "eng": "If I were you, I would study."}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "If I [had] money, I would travel.", ["had", "have", "has", "having"], "had"),
          gaps("Дұрыс формасын таңдаңыз:", "If she were here, she [would] help us.", ["would", "will", "can", "is"], "would"),
          gaps("Дұрыс формасын таңдаңыз:", "If I [were] you, I would accept.", ["were", "was", "am", "is"], "were"),
          order("Сөйлемді құрастырыңыз:", ["had", "If", "I", "time", ",", "would", "I", "read", "more", "."], "If I had time, I would read more."),
          order("Сөйлемді құрастырыңыз:", ["were", "If", "I", "you", ",", "would", "I", "study", "."], "If I were you, I would study.")
        ]
      }
    ]
  },
  {
    "title": "Professional English",
    "lessons": [
      {
        "title": "Business Communication",
        "theory": {
          "title": "Іскерлік қарым-қатынас",
          "explanation": "Ресми хат: 'Dear Sir/Madam' — Құрметті мырза/ханым. 'I am writing to...' — Мен ... мақсатымен жазып отырмын. 'I look forward to hearing from you.' — Жауабыңызды күтемін. 'Best regards' — Құрметпен.",
          "examples": [
            {"kaz": "Мен жұмысқа өтініш жазып отырмын.", "eng": "I am writing to apply for the position."},
            {"kaz": "Жауабыңызды күтемін.", "eng": "I look forward to hearing from you."},
            {"kaz": "Қосымша ақпарат бере аласыз ба?", "eng": "Could you provide more information?"}
          ]
        },
        "tasks": [
          match("Іскерлік сөздерді аударыңыз:", [
            {"item": "Dear Sir", "match": "Құрметті мырза"},
            {"item": "Best regards", "match": "Құрметпен"},
            {"item": "I am writing to", "match": "Мен жазып отырмын"},
            {"item": "Deadline", "match": "Мерзім"},
            {"item": "Meeting", "match": "Жиналыс"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "I am writing to [apply] for the position.", ["apply", "applying", "applied", "applies"], "apply"),
          gaps("Дұрыс сөзді таңдаңыз:", "I look [forward] to hearing from you.", ["forward", "for", "toward", "forwards"], "forward"),
          gaps("Дұрыс сөзді таңдаңыз:", "[Could] you provide more information?", ["Could", "Can", "Will", "Do"], "Could"),
          order("Сөйлемді құрастырыңыз:", ["writing", "I", "am", "to", "apply", "for", "the", "job", "."], "I am writing to apply for the job."),
          order("Сөйлемді құрастырыңыз:", ["forward", "look", "I", "to", "hearing", "from", "you", "."], "I look forward to hearing from you.")
        ]
      },
      {
        "title": "Idioms & Expressions",
        "theory": {
          "title": "Идиомалар мен тұрақты тіркестер",
          "explanation": "Идиомалар — сөзбе-сөз аударуға болмайтын тіркестер. 'Break the ice' — танысуды бастау. 'Piece of cake' — оңай іс. 'Hit the books' — оқуға кірісу. 'Under the weather' — ауырып қалу.",
          "examples": [
            {"kaz": "Бұл оңай іс. (тура: торт кесігі)", "eng": "It's a piece of cake."},
            {"kaz": "Мен ауырып қалдым. (тура: ауа райы астында)", "eng": "I'm feeling under the weather."},
            {"kaz": "Оқуға кірісу керек. (тура: кітаптарды ұру)", "eng": "I need to hit the books."}
          ]
        },
        "tasks": [
          match("Идиомаларды мағынасымен сәйкестендіріңіз:", [
            {"item": "Piece of cake", "match": "Оңай іс"},
            {"item": "Break the ice", "match": "Танысуды бастау"},
            {"item": "Hit the books", "match": "Оқуға кірісу"},
            {"item": "Under the weather", "match": "Ауырып қалу"},
            {"item": "Cost an arm and a leg", "match": "Өте қымбат"}
          ]),
          gaps("Дұрыс идиоманы таңдаңыз:", "The exam was easy. It was a [piece] of cake.", ["piece", "peace", "part", "plate"], "piece"),
          gaps("Дұрыс идиоманы таңдаңыз:", "I'm feeling [under] the weather today.", ["under", "over", "in", "on"], "under"),
          order("Сөйлемді құрастырыңыз:", ["a", "It's", "piece", "of", "cake", "."], "It's a piece of cake."),
          order("Сөйлемді құрастырыңыз:", ["need", "I", "to", "hit", "the", "books", "."], "I need to hit the books.")
        ]
      }
    ]
  },
  {
    "title": "Debating & Discussing",
    "lessons": [
      {
        "title": "Expressing Arguments",
        "theory": {
          "title": "Дәлелдер келтіру",
          "explanation": "'First of all...' — Біріншіден. 'Furthermore...' — Сонымен қатар. 'However...' — Алайда. 'On the other hand...' — Екінші жағынан. 'In conclusion...' — Қорытындылай келе. Бұл сөздер эссе мен пікірталаста қолданылады.",
          "examples": [
            {"kaz": "Біріншіден, білім маңызды.", "eng": "First of all, education is important."},
            {"kaz": "Алайда, бәрі келіспейді.", "eng": "However, not everyone agrees."},
            {"kaz": "Қорытындылай келе, технология пайдалы.", "eng": "In conclusion, technology is useful."}
          ]
        },
        "tasks": [
          match("Байланыстырғыш сөздерді аударыңыз:", [
            {"item": "First of all", "match": "Біріншіден"},
            {"item": "Furthermore", "match": "Сонымен қатар"},
            {"item": "However", "match": "Алайда"},
            {"item": "On the other hand", "match": "Екінші жағынан"},
            {"item": "In conclusion", "match": "Қорытындылай келе"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "[However], not everyone agrees.", ["However", "Because", "And", "So"], "However"),
          gaps("Дұрыс сөзді таңдаңыз:", "In [conclusion], technology is useful.", ["conclusion", "conclude", "concluding", "concluded"], "conclusion"),
          order("Сөйлемді құрастырыңыз:", ["of", "First", "all", ",", "education", "is", "important", "."], "First of all, education is important."),
          order("Сөйлемді құрастырыңыз:", ["the", "On", "other", "hand", ",", "it", "is", "expensive", "."], "On the other hand, it is expensive.")
        ]
      },
      {
        "title": "Relative Clauses",
        "theory": {
          "title": "Анықтауыш сөйлемдер — Relative Clauses",
          "explanation": "'Who' — адам: 'The man who lives here.' 'Which' — зат: 'The book which I read.' 'That' — екеуінің орнына. 'Where' — орын: 'The city where I was born.' 'Whose' — иелік: 'The girl whose bag is red.'",
          "examples": [
            {"kaz": "Мұнда тұратын адам — менің көршім.", "eng": "The man who lives here is my neighbor."},
            {"kaz": "Мен оқыған кітап қызықты болды.", "eng": "The book which I read was interesting."},
            {"kaz": "Мен туылған қала — Алматы.", "eng": "The city where I was born is Almaty."}
          ]
        },
        "tasks": [
          match("Relative pronoun-дарды қолданылуымен сәйкестендіріңіз:", [
            {"item": "who", "match": "адамдар үшін"},
            {"item": "which", "match": "заттар үшін"},
            {"item": "where", "match": "орын үшін"},
            {"item": "whose", "match": "иелік үшін"},
            {"item": "that", "match": "адам/зат екеуіне де"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "The man [who] lives here is my neighbor.", ["who", "which", "where", "whose"], "who"),
          gaps("Дұрыс сөзді таңдаңыз:", "The book [which] I read was interesting.", ["which", "who", "where", "whose"], "which"),
          gaps("Дұрыс сөзді таңдаңыз:", "The city [where] I was born is Almaty.", ["where", "who", "which", "whose"], "where"),
          order("Сөйлемді құрастырыңыз:", ["who", "The", "girl", "speaks", "English", "is", "my", "friend", "."], "The girl who speaks English is my friend."),
          order("Сөйлемді құрастырыңыз:", ["where", "The", "place", "we", "met", "is", "beautiful", "."], "The place where we met is beautiful.")
        ]
      }
    ]
  },
  {
    "title": "B2 Final Challenge",
    "lessons": [
      {
        "title": "Advanced Tenses",
        "theory": {
          "title": "Past Perfect & Future Perfect",
          "explanation": "Past Perfect 'had + V3' — бір өткен оқиғадан бұрын болған іс: 'I had eaten before he came.' Future Perfect 'will have + V3' — болашақта белгілі уақытқа дейін аяқталатын іс: 'By 2030, I will have graduated.'",
          "examples": [
            {"kaz": "Ол келгенге дейін мен тамақтанып қойдым.", "eng": "I had eaten before he came."},
            {"kaz": "2030 жылға дейін мен бітіріп қоямын.", "eng": "By 2030, I will have graduated."},
            {"kaz": "Олар біз жеткенде кетіп қойған еді.", "eng": "They had left before we arrived."}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "I [had eaten] before he came.", ["had eaten", "ate", "eat", "have eaten"], "had eaten"),
          gaps("Дұрыс формасын таңдаңыз:", "By 2030, I [will have graduated].", ["will have graduated", "graduated", "will graduate", "have graduated"], "will have graduated"),
          gaps("Дұрыс формасын таңдаңыз:", "They [had left] before we arrived.", ["had left", "left", "leave", "have left"], "had left"),
          order("Сөйлемді құрастырыңыз:", ["had", "She", "finished", "before", "I", "arrived", "."], "She had finished before I arrived."),
          order("Сөйлемді құрастырыңыз:", ["will", "By", "next", "year", ",", "I", "have", "learned", "English", "."], "By next year, I will have learned English.")
        ]
      },
      {
        "title": "B2 Boss Battle",
        "theory": {
          "title": "B2 қорытынды тест",
          "explanation": "Барлық B2 тақырыптарын қайталау: Reported Speech, Second Conditional, іскерлік хат, идиомалар, дәлелдер, Relative Clauses, Past/Future Perfect.",
          "examples": [
            {"kaz": "Ол маған 'Мен ертең келемін' деді.", "eng": "He told me he would come the next day."},
            {"kaz": "Менде уақыт болса, кітап оқыр едім.", "eng": "If I had time, I would read a book."}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "He said he [would] come tomorrow.", ["would", "will", "can", "is"], "would"),
          gaps("Дұрыс формасын таңдаңыз:", "If I [had] time, I would travel.", ["had", "have", "has", "having"], "had"),
          gaps("Дұрыс сөзді таңдаңыз:", "The person [who] called you is here.", ["who", "which", "where", "whose"], "who"),
          gaps("Дұрыс формасын таңдаңыз:", "She [had finished] before I arrived.", ["had finished", "finished", "finish", "finishes"], "had finished"),
          order("Сөйлемді құрастырыңыз:", ["said", "She", "that", "she", "was", "busy", "."], "She said that she was busy."),
          order("Сөйлемді құрастырыңыз:", ["had", "If", "I", "money", ",", "would", "I", "buy", "a", "car", "."], "If I had money, I would buy a car.")
        ]
      }
    ]
  }
]

def seed_b2():
    old = Course.query.filter_by(level="B2").all()
    for c in old:
        for m in Module.query.filter_by(course_id=c.id).all():
            for l in Lesson.query.filter_by(module_id=m.id).all():
                Task.query.filter_by(lesson_id=l.id).delete()
            Lesson.query.filter_by(module_id=m.id).delete()
        Module.query.filter_by(course_id=c.id).delete()
    Course.query.filter_by(level="B2").delete()
    db.session.commit()
    course = Course(title="English B2: Upper-Intermediate", description="Reported Speech, Second Conditional, іскерлік ағылшын, идиомалар, Relative Clauses, Past/Future Perfect.", language="English", level="B2")
    db.session.add(course); db.session.flush()
    lo = 0
    for mi, md in enumerate(B2_MODULES):
        mod = Module(course_id=course.id, title=md["title"], order=mi+1)
        db.session.add(mod); db.session.flush()
        for ld in md["lessons"]:
            lo += 1
            les = Lesson(module_id=mod.id, title=ld["title"], theory=ld["theory"], order=lo)
            db.session.add(les); db.session.flush()
            for ti, t in enumerate(ld["tasks"]):
                t.lesson_id = les.id; t.order = ti+1; db.session.add(t)
    db.session.commit()
    print(f"✅ B2 seeded: {lo} lessons")

if __name__ == "__main__":
    with app.app_context(): seed_b2()
