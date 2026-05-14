"""C1 Advanced English curriculum for Kazakh speakers. 10 lessons."""
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

C1_MODULES = [
  {
    "title": "Nuanced Communication",
    "lessons": [
      {
        "title": "Mixed Conditionals",
        "theory": {
          "title": "Аралас шартты сөйлемдер",
          "explanation": "Mixed Conditionals — өткен шақ пен қазіргі шақты араластырады. 'If I had studied harder, I would be a doctor now.' (Егер жақсы оқығанымда, қазір дәрігер болар едім). Өткен шарт + қазіргі нәтиже немесе қазіргі шарт + өткен нәтиже.",
          "examples": [
            {"kaz": "Егер жақсы оқысам, қазір дәрігер болар едім.", "eng": "If I had studied harder, I would be a doctor now."},
            {"kaz": "Егер ол ағылшынша білсе, ол кеше жұмысқа тұрар еді.", "eng": "If she spoke English, she would have got the job yesterday."},
            {"kaz": "Егер біз ерте шықсақ, қазір сонда болар едік.", "eng": "If we had left earlier, we would be there now."}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "If I [had studied] harder, I would be a doctor now.", ["had studied", "studied", "study", "have studied"], "had studied"),
          gaps("Дұрыс формасын таңдаңыз:", "If she spoke English, she [would have got] the job.", ["would have got", "will get", "would get", "gets"], "would have got"),
          gaps("Дұрыс формасын таңдаңыз:", "If we had left earlier, we [would be] there now.", ["would be", "will be", "are", "were"], "would be"),
          order("Сөйлемді құрастырыңыз:", ["had", "If", "I", "known", ",", "would", "I", "have", "helped", "."], "If I had known, I would have helped."),
          order("Сөйлемді құрастырыңыз:", ["had", "If", "he", "practiced", ",", "would", "he", "be", "fluent", "now", "."], "If he had practiced, he would be fluent now.")
        ]
      },
      {
        "title": "Persuasive Language",
        "theory": {
          "title": "Сендіру тілі",
          "explanation": "Сендіру стратегиялары: 'Don\\'t you think...?' — Сіз ... деп ойламайсыз ба? 'It is widely recognized that...' — Жалпы мойындалған. 'There is no doubt that...' — Күмән жоқ. 'You have to admit that...' — Мойындауыңыз керек.",
          "examples": [
            {"kaz": "Күмән жоқ, білім маңызды.", "eng": "There is no doubt that education is important."},
            {"kaz": "Мойындауыңыз керек, бұл әділетті.", "eng": "You have to admit that this is fair."},
            {"kaz": "Жалпы мойындалған, спорт денсаулыққа пайдалы.", "eng": "It is widely recognized that sports are healthy."}
          ]
        },
        "tasks": [
          match("Сендіру тіркестерін аударыңыз:", [
            {"item": "There is no doubt", "match": "Күмән жоқ"},
            {"item": "It is widely recognized", "match": "Жалпы мойындалған"},
            {"item": "You have to admit", "match": "Мойындауыңыз керек"},
            {"item": "Don't you think", "match": "Ойламайсыз ба"},
            {"item": "It goes without saying", "match": "Айтпаса да түсінікті"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "There is no [doubt] that education matters.", ["doubt", "problem", "way", "idea"], "doubt"),
          gaps("Дұрыс сөзді таңдаңыз:", "It is widely [recognized] that exercise is healthy.", ["recognized", "recognizing", "recognize", "recognizes"], "recognized"),
          order("Сөйлемді құрастырыңыз:", ["is", "There", "no", "doubt", "that", "this", "is", "important", "."], "There is no doubt that this is important."),
          order("Сөйлемді құрастырыңыз:", ["have", "You", "to", "admit", "this", "is", "fair", "."], "You have to admit this is fair.")
        ]
      }
    ]
  },
  {
    "title": "Academic English",
    "lessons": [
      {
        "title": "Academic Writing",
        "theory": {
          "title": "Академиялық жазу",
          "explanation": "Академиялық стиль: бейтарап тон, дәлелді құрылым. 'This essay examines...' — Бұл эссе қарастырады. 'Research suggests that...' — Зерттеулер көрсетеді. 'It can be argued that...' — Дәлелдеуге болады. Эссе құрылымы: Introduction → Body → Conclusion.",
          "examples": [
            {"kaz": "Бұл эссе жаһандануды қарастырады.", "eng": "This essay examines globalization."},
            {"kaz": "Зерттеулер көрсетеді, оқу пайдалы.", "eng": "Research suggests that reading is beneficial."},
            {"kaz": "Қорытындылай келе, екі жағы да бар.", "eng": "In conclusion, there are advantages and disadvantages."}
          ]
        },
        "tasks": [
          match("Академиялық тіркестерді аударыңыз:", [
            {"item": "This essay examines", "match": "Бұл эссе қарастырады"},
            {"item": "Research suggests", "match": "Зерттеулер көрсетеді"},
            {"item": "It can be argued", "match": "Дәлелдеуге болады"},
            {"item": "In conclusion", "match": "Қорытындылай келе"},
            {"item": "On the contrary", "match": "Керісінше"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "Research [suggests] that reading is beneficial.", ["suggests", "suggest", "suggested", "suggesting"], "suggests"),
          gaps("Дұрыс сөзді таңдаңыз:", "This essay [examines] the impact of technology.", ["examines", "examine", "examining", "examined"], "examines"),
          order("Сөйлемді құрастырыңыз:", ["suggests", "Research", "that", "exercise", "improves", "health", "."], "Research suggests that exercise improves health."),
          order("Сөйлемді құрастырыңыз:", ["conclusion", "In", ",", "both", "sides", "have", "valid", "points", "."], "In conclusion, both sides have valid points.")
        ]
      },
      {
        "title": "Abstract Topics",
        "theory": {
          "title": "Абстрактілі тақырыптар",
          "explanation": "Күрделі тақырыптар туралы пікір: 'In terms of...' — ... тұрғысынан. 'With regard to...' — ...қатысты. 'It is essential to consider...' — Ескеру маңызды. 'The underlying issue is...' — Негізгі мәселе...",
          "examples": [
            {"kaz": "Экономика тұрғысынан бұл тиімсіз.", "eng": "In terms of the economy, this is inefficient."},
            {"kaz": "Негізгі мәселе — теңсіздік.", "eng": "The underlying issue is inequality."},
            {"kaz": "Екі жақты да ескеру маңызды.", "eng": "It is essential to consider both sides."}
          ]
        },
        "tasks": [
          match("Академиялық сөздерді аударыңыз:", [
            {"item": "In terms of", "match": "...тұрғысынан"},
            {"item": "With regard to", "match": "...қатысты"},
            {"item": "The underlying issue", "match": "Негізгі мәселе"},
            {"item": "It is essential", "match": "Маңызды"},
            {"item": "Nevertheless", "match": "Соған қарамастан"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "In [terms] of the economy, this is inefficient.", ["terms", "term", "way", "case"], "terms"),
          gaps("Дұрыс сөзді таңдаңыз:", "The [underlying] issue is inequality.", ["underlying", "under", "below", "basic"], "underlying"),
          order("Сөйлемді құрастырыңыз:", ["essential", "It", "is", "to", "consider", "both", "sides", "."], "It is essential to consider both sides."),
          order("Сөйлемді құрастырыңыз:", ["terms", "In", "of", "education", ",", "progress", "has", "been", "made", "."], "In terms of education, progress has been made.")
        ]
      }
    ]
  },
  {
    "title": "Advanced Structures",
    "lessons": [
      {
        "title": "Inversion & Emphasis",
        "theory": {
          "title": "Инверсия мен екпін",
          "explanation": "Инверсия — сөз тәртібін өзгерту, ерекшелеу үшін. 'Not only...but also' — ...ғана емес, сонымен қатар. 'Hardly had I arrived when...' — Мен жеткенімше... 'Never have I seen...' — Мен ешқашан көрген жоқпын... 'Seldom do we...' — Біз сирек...",
          "examples": [
            {"kaz": "Ол ғана емес, сонымен қатар досы да келді.", "eng": "Not only did he come, but also his friend."},
            {"kaz": "Мен мұндай көрген жоқпын.", "eng": "Never have I seen anything like this."},
            {"kaz": "Мен жеткенімше жаңбыр жауды.", "eng": "Hardly had I arrived when it started raining."}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "Not only [did] he come, but also his friend.", ["did", "do", "does", "was"], "did"),
          gaps("Дұрыс формасын таңдаңыз:", "Never [have] I seen anything like this.", ["have", "has", "had", "did"], "have"),
          gaps("Дұрыс формасын таңдаңыз:", "Hardly [had] I arrived when it rained.", ["had", "have", "has", "did"], "had"),
          order("Сөйлемді құрастырыңыз:", ["only", "Not", "did", "she", "win", ",", "but", "also", "broke", "a", "record", "."], "Not only did she win, but also broke a record."),
          order("Сөйлемді құрастырыңыз:", ["have", "Never", "I", "been", "so", "surprised", "."], "Never have I been so surprised.")
        ]
      },
      {
        "title": "Advanced Phrasal Verbs",
        "theory": {
          "title": "Күрделі фразалық етістіктер",
          "explanation": "Phrasal verbs — мағынасы бөлек сөздерден құралады. 'Come up with' — ойлап табу. 'Put up with' — шыдау. 'Look into' — зерттеу. 'Break down' — бұзылу/жылау. 'Get along with' — тіл табысу.",
          "examples": [
            {"kaz": "Ол жақсы идея ойлап тапты.", "eng": "She came up with a great idea."},
            {"kaz": "Мен бұл шуылға шыдай алмаймын.", "eng": "I can't put up with this noise."},
            {"kaz": "Полиция бұл ісді зерттеп жатыр.", "eng": "The police are looking into the case."}
          ]
        },
        "tasks": [
          match("Фразалық етістіктерді мағынасымен сәйкестендіріңіз:", [
            {"item": "come up with", "match": "ойлап табу"},
            {"item": "put up with", "match": "шыдау"},
            {"item": "look into", "match": "зерттеу"},
            {"item": "break down", "match": "бұзылу"},
            {"item": "get along with", "match": "тіл табысу"}
          ]),
          gaps("Дұрыс phrasal verb таңдаңыз:", "She came [up] with a great idea.", ["up", "out", "in", "on"], "up"),
          gaps("Дұрыс phrasal verb таңдаңыз:", "I can't put up [with] this noise.", ["with", "to", "on", "for"], "with"),
          gaps("Дұрыс phrasal verb таңдаңыз:", "We need to look [into] this problem.", ["into", "up", "out", "for"], "into"),
          order("Сөйлемді құрастырыңыз:", ["came", "She", "up", "with", "a", "brilliant", "solution", "."], "She came up with a brilliant solution."),
          order("Сөйлемді құрастырыңыз:", ["along", "I", "get", "well", "with", "my", "colleagues", "."], "I get along well with my colleagues.")
        ]
      }
    ]
  },
  {
    "title": "C1 Final Challenge",
    "lessons": [
      {
        "title": "Cleft Sentences",
        "theory": {
          "title": "Cleft сөйлемдер — Екпінді құрылымдар",
          "explanation": "'It is/was...that/who' — маңызды бөлікті ерекшелеу. 'It was John who broke the window.' — Терезені сындырған — Джон. 'What I need is...' — Маған керегі... 'All I want is...' — Мен тек қана ... қалаймын.",
          "examples": [
            {"kaz": "Терезені сындырған — Джон.", "eng": "It was John who broke the window."},
            {"kaz": "Маған керегі — демалыс.", "eng": "What I need is a vacation."},
            {"kaz": "Мен тек бейбітшілік қалаймын.", "eng": "All I want is peace."}
          ]
        },
        "tasks": [
          gaps("Дұрыс сөзді таңдаңыз:", "It [was] John who broke the window.", ["was", "is", "were", "been"], "was"),
          gaps("Дұрыс сөзді таңдаңыз:", "[What] I need is a vacation.", ["What", "That", "Which", "Who"], "What"),
          gaps("Дұрыс сөзді таңдаңыз:", "[All] I want is peace.", ["All", "Every", "Much", "Many"], "All"),
          order("Сөйлемді құрастырыңыз:", ["was", "It", "she", "who", "solved", "the", "problem", "."], "It was she who solved the problem."),
          order("Сөйлемді құрастырыңыз:", ["I", "What", "need", "is", "more", "time", "."], "What I need is more time.")
        ]
      },
      {
        "title": "C1 Boss Battle",
        "theory": {
          "title": "C1 қорытынды тест",
          "explanation": "Барлық C1 тақырыптарын қайталау: Mixed Conditionals, сендіру тілі, академиялық жазу, абстрактілі тақырыптар, инверсия, phrasal verbs, cleft sentences. Тамаша жұмыс! Сіз C1 деңгейіне жеттіңіз!",
          "examples": [
            {"kaz": "Егер жақсы оқығанымда, қазір дәрігер болар едім.", "eng": "If I had studied harder, I would be a doctor now."},
            {"kaz": "Күмән жоқ, технология өмірімізді өзгертті.", "eng": "There is no doubt that technology has changed our lives."}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "If I [had studied] harder, I would be a doctor.", ["had studied", "studied", "study", "have studied"], "had studied"),
          gaps("Дұрыс формасын таңдаңыз:", "Not only [did] she graduate, but she also got a job.", ["did", "do", "does", "has"], "did"),
          gaps("Дұрыс формасын таңдаңыз:", "She came up [with] an innovative solution.", ["with", "to", "for", "on"], "with"),
          gaps("Дұрыс формасын таңдаңыз:", "It [was] the teacher who inspired me.", ["was", "is", "were", "been"], "was"),
          match("C1 тақырыптарын сәйкестендіріңіз:", [
            {"item": "Mixed Conditional", "match": "Өткен шарт + қазіргі нәтиже"},
            {"item": "Inversion", "match": "Сөз тәртібін ерекшелеу"},
            {"item": "Cleft sentence", "match": "It was...who/that"},
            {"item": "Phrasal verb", "match": "come up with, look into"},
            {"item": "Academic register", "match": "Research suggests that..."}
          ]),
          order("Сөйлемді құрастырыңыз:", ["is", "There", "no", "doubt", "that", "technology", "has", "changed", "our", "lives", "."], "There is no doubt that technology has changed our lives.")
        ]
      }
    ]
  }
]

def seed_c1():
    old = Course.query.filter_by(level="C1").all()
    for c in old:
        for m in Module.query.filter_by(course_id=c.id).all():
            for l in Lesson.query.filter_by(module_id=m.id).all():
                Task.query.filter_by(lesson_id=l.id).delete()
            Lesson.query.filter_by(module_id=m.id).delete()
        Module.query.filter_by(course_id=c.id).delete()
    Course.query.filter_by(level="C1").delete()
    db.session.commit()
    course = Course(title="English C1: Advanced", description="Mixed Conditionals, инверсия, академиялық жазу, phrasal verbs, cleft sentences.", language="English", level="C1")
    db.session.add(course); db.session.flush()
    lo = 0
    for mi, md in enumerate(C1_MODULES):
        mod = Module(course_id=course.id, title=md["title"], order=mi+1)
        db.session.add(mod); db.session.flush()
        for ld in md["lessons"]:
            lo += 1
            les = Lesson(module_id=mod.id, title=ld["title"], theory=ld["theory"], order=lo)
            db.session.add(les); db.session.flush()
            for ti, t in enumerate(ld["tasks"]):
                t.lesson_id = les.id; t.order = ti+1; db.session.add(t)
    db.session.commit()
    print(f"✅ C1 seeded: {lo} lessons")

if __name__ == "__main__":
    with app.app_context(): seed_c1()
