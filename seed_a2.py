"""A2 Elementary English curriculum for Kazakh speakers. 10 lessons."""
import os, sys
os.environ.setdefault("SECRET_KEY", "dev")
os.environ.setdefault("WEBHOOK_SECRET", "dev")
from app.main import create_app
from app.database import db
from app.models.db_models import Course, Module, Lesson, Task

app = create_app()

def match(instruction, pairs):
    return Task(task_type="matching", content={"instruction": instruction, "pairs": pairs}, order=0)
def gaps(prompt, text, options, answer):
    return Task(task_type="gaps", content={"sentences": [{"prompt": prompt, "text": text, "options": options, "answer": answer}]}, order=0)
def order(prompt, words, correct):
    return Task(task_type="ordering", content={"sentences": [{"prompt": prompt, "words": words, "correct": correct}]}, order=0)

A2_MODULES = [
  {
    "title": "Past Events",
    "lessons": [
      {
        "title": "Yesterday",
        "theory": {
          "title": "Past Simple — Кеше не болды?",
          "explanation": "Past Simple — өткен шақтағы аяқталған іс-әрекет. Дұрыс етістіктерге -ed жалғанады: work→worked, play→played. Бұрыс етістіктер: go→went, eat→ate, see→saw. Уақыт сөздері: yesterday, last week, ago.",
          "examples": [
            {"kaz": "Мен кеше мектепке бардым.", "eng": "I went to school yesterday."},
            {"kaz": "Ол кеше футбол ойнады.", "eng": "He played football yesterday."},
            {"kaz": "Біз кино көрдік.", "eng": "We watched a movie."}
          ]
        },
        "tasks": [
          match("Етістіктердің Past Simple формасын сәйкестендіріңіз:", [
            {"item": "go", "match": "went"},
            {"item": "eat", "match": "ate"},
            {"item": "see", "match": "saw"},
            {"item": "play", "match": "played"},
            {"item": "have", "match": "had"},
            {"item": "come", "match": "came"}
          ]),
          gaps("Past Simple формасын таңдаңыз:", "I [went] to school yesterday.", ["went", "go", "goes", "going"], "went"),
          gaps("Past Simple формасын таңдаңыз:", "She [played] tennis last week.", ["played", "play", "plays", "playing"], "played"),
          order("Сөйлемді құрастырыңыз:", ["watched", "We", "a", "movie", "yesterday", "."], "We watched a movie yesterday."),
          order("Сөйлемді құрастырыңыз:", ["ate", "I", "breakfast", "morning", "this", "."], "I ate breakfast this morning.")
        ]
      },
      {
        "title": "My Hobbies",
        "theory": {
          "title": "Хобби — like / enjoy + -ing",
          "explanation": "'I like' + -ing — маған ұнайды. 'I enjoy' + -ing — мен ләззат аламын. Хоббилер: reading (оқу), swimming (жүзу), drawing (сурет салу), cooking (тамақ пісіру), playing guitar (гитара ойнау).",
          "examples": [
            {"kaz": "Маған кітап оқу ұнайды.", "eng": "I like reading books."},
            {"kaz": "Ол жүзуден ләззат алады.", "eng": "She enjoys swimming."},
            {"kaz": "Сенің хоббиің не?", "eng": "What is your hobby?"}
          ]
        },
        "tasks": [
          match("Хоббилерді аударыңыз:", [
            {"item": "Reading", "match": "Оқу"},
            {"item": "Swimming", "match": "Жүзу"},
            {"item": "Drawing", "match": "Сурет салу"},
            {"item": "Cooking", "match": "Тамақ пісіру"},
            {"item": "Dancing", "match": "Би билеу"}
          ]),
          gaps("Дұрыс формасын таңдаңыз:", "I like [reading] books.", ["reading", "read", "reads", "to reads"], "reading"),
          gaps("Дұрыс формасын таңдаңыз:", "She enjoys [swimming].", ["swimming", "swim", "swims", "swam"], "swimming"),
          order("Сөйлемді құрастырыңыз:", ["like", "I", "cooking", "."], "I like cooking."),
          order("Сөйлемді құрастырыңыз:", ["is", "What", "your", "hobby", "?"], "What is your hobby?")
        ]
      }
    ]
  },
  {
    "title": "Shopping & Travel",
    "lessons": [
      {
        "title": "At the Shop",
        "theory": {
          "title": "Дүкенде сөйлесу",
          "explanation": "Дүкенде: 'How much is this?' — Мынау қанша тұрады? 'I would like...' — Мен ... алғым келеді. 'Can I pay by card?' — Картамен төлей аламын ба? Бағаны айту: 'It costs five dollars.'",
          "examples": [
            {"kaz": "Мынау қанша тұрады?", "eng": "How much is this?"},
            {"kaz": "Мен сүт алғым келеді.", "eng": "I would like some milk."},
            {"kaz": "Бұл бес доллар тұрады.", "eng": "It costs five dollars."}
          ]
        },
        "tasks": [
          match("Дүкен сөздерін аударыңыз:", [
            {"item": "Price", "match": "Баға"},
            {"item": "Cheap", "match": "Арзан"},
            {"item": "Expensive", "match": "Қымбат"},
            {"item": "Money", "match": "Ақша"},
            {"item": "To buy", "match": "Сатып алу"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "How [much] is this?", ["much", "many", "old", "big"], "much"),
          gaps("Дұрыс сөзді таңдаңыз:", "I would [like] some bread.", ["like", "liked", "liking", "likes"], "like"),
          order("Сөйлемді құрастырыңыз:", ["much", "How", "is", "this", "?"], "How much is this?"),
          order("Сөйлемді құрастырыңыз:", ["like", "would", "I", "some", "tea", "."], "I would like some tea.")
        ]
      },
      {
        "title": "Travel & Transport",
        "theory": {
          "title": "Саяхат пен көлік",
          "explanation": "Көлік түрлері: bus (автобус), train (пойыз), plane (ұшақ), taxi (такси), car (көлік). 'How do I get to...?' — ...ға қалай жетемін? 'Turn left/right' — Солға/оңға бұрылыңыз.",
          "examples": [
            {"kaz": "Вокзалға қалай жетемін?", "eng": "How do I get to the station?"},
            {"kaz": "Солға бұрылыңыз.", "eng": "Turn left."},
            {"kaz": "Мен автобуспен келдім.", "eng": "I came by bus."}
          ]
        },
        "tasks": [
          match("Көлік түрлерін аударыңыз:", [
            {"item": "Bus", "match": "Автобус"},
            {"item": "Train", "match": "Пойыз"},
            {"item": "Plane", "match": "Ұшақ"},
            {"item": "Taxi", "match": "Такси"},
            {"item": "Car", "match": "Көлік"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "Turn [left] at the corner.", ["left", "up", "fast", "old"], "left"),
          gaps("Дұрыс сөзді таңдаңыз:", "I came [by] bus.", ["by", "on", "at", "in"], "by"),
          order("Сөйлемді құрастырыңыз:", ["get", "do", "How", "I", "to", "the", "station", "?"], "How do I get to the station?"),
          order("Сөйлемді құрастырыңыз:", ["left", "Turn", "at", "the", "corner", "."], "Turn left at the corner.")
        ]
      }
    ]
  },
  {
    "title": "Feelings & Future",
    "lessons": [
      {
        "title": "Emotions",
        "theory": {
          "title": "Сезімдер мен көңіл-күй",
          "explanation": "Сезімдер: happy (бақытты), sad (мұңды), angry (ашулы), tired (шаршаған), excited (қуанышты), scared (қорыққан). 'I feel...' — Мен ... сезінемін. 'Are you okay?' — Сен жақсы ма?",
          "examples": [
            {"kaz": "Мен бақыттымын.", "eng": "I am happy."},
            {"kaz": "Ол шаршаған.", "eng": "She is tired."},
            {"kaz": "Неге мұңдысың?", "eng": "Why are you sad?"}
          ]
        },
        "tasks": [
          match("Сезімдерді аударыңыз:", [
            {"item": "Happy", "match": "Бақытты"},
            {"item": "Sad", "match": "Мұңды"},
            {"item": "Angry", "match": "Ашулы"},
            {"item": "Tired", "match": "Шаршаған"},
            {"item": "Scared", "match": "Қорыққан"},
            {"item": "Excited", "match": "Қуанышты"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "I feel [happy] today.", ["happy", "yesterday", "blue", "five"], "happy"),
          gaps("Дұрыс сөзді таңдаңыз:", "She is [tired] after work.", ["tired", "tire", "tiring", "tires"], "tired"),
          order("Сөйлемді құрастырыңыз:", ["are", "Why", "you", "sad", "?"], "Why are you sad?"),
          order("Сөйлемді құрастырыңыз:", ["feel", "I", "happy", "today", "."], "I feel happy today.")
        ]
      },
      {
        "title": "Future Plans",
        "theory": {
          "title": "Болашақ жоспарлар — will / going to",
          "explanation": "'Will' — жылдам шешім немесе болжам: 'I will help you.' 'Going to' — алдын ала жоспарланған іс: 'I am going to visit my grandma.' Уақыт сөздері: tomorrow, next week, next year.",
          "examples": [
            {"kaz": "Мен саған көмектесемін.", "eng": "I will help you."},
            {"kaz": "Ол ертең келетін болады.", "eng": "She is going to come tomorrow."},
            {"kaz": "Біз келесі жылы саяхаттаймыз.", "eng": "We will travel next year."}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "I [will] help you.", ["will", "am", "was", "did"], "will"),
          gaps("Дұрыс формасын таңдаңыз:", "She is [going] to visit her grandma.", ["going", "go", "went", "gone"], "going"),
          gaps("Дұрыс формасын таңдаңыз:", "We will [travel] next year.", ["travel", "traveled", "travels", "traveling"], "travel"),
          order("Сөйлемді құрастырыңыз:", ["will", "I", "help", "you", "."], "I will help you."),
          order("Сөйлемді құрастырыңыз:", ["going", "is", "She", "to", "come", "tomorrow", "."], "She is going to come tomorrow.")
        ]
      }
    ]
  },
  {
    "title": "Comparing & Describing",
    "lessons": [
      {
        "title": "Bigger & Better",
        "theory": {
          "title": "Салыстырмалы шырай — Comparatives",
          "explanation": "Қысқа сын есімдерге -er жалғанады: big→bigger, tall→taller, fast→faster. Ұзын сөздер: more + adjective: more beautiful, more expensive. 'Than' — ...дан/ден: 'He is taller than me.'",
          "examples": [
            {"kaz": "Ол менен биік.", "eng": "He is taller than me."},
            {"kaz": "Бұл кітап қызықтырақ.", "eng": "This book is more interesting."},
            {"kaz": "Жаз қыстан жылы.", "eng": "Summer is warmer than winter."}
          ]
        },
        "tasks": [
          match("Салыстырмалы формаларды сәйкестендіріңіз:", [
            {"item": "big", "match": "bigger"},
            {"item": "tall", "match": "taller"},
            {"item": "fast", "match": "faster"},
            {"item": "good", "match": "better"},
            {"item": "bad", "match": "worse"}
          ]),
          gaps("Дұрыс формасын таңдаңыз:", "He is [taller] than me.", ["taller", "tall", "tallest", "more tall"], "taller"),
          gaps("Дұрыс формасын таңдаңыз:", "This is [more] expensive.", ["more", "most", "much", "many"], "more"),
          order("Сөйлемді құрастырыңыз:", ["is", "Summer", "warmer", "than", "winter", "."], "Summer is warmer than winter."),
          order("Сөйлемді құрастырыңыз:", ["is", "She", "faster", "than", "me", "."], "She is faster than me.")
        ]
      },
      {
        "title": "Health & Body",
        "theory": {
          "title": "Денсаулық — Дәрігерде",
          "explanation": "Дене мүшелері: head (бас), hand (қол), leg (аяқ), stomach (асқазан). Сырқаттану: 'I have a headache' — Басым ауырады. 'I feel sick' — Мен ауырамын. Дәрігерде: 'What is the problem?' — Не болды?",
          "examples": [
            {"kaz": "Басым ауырады.", "eng": "I have a headache."},
            {"kaz": "Мен ауырамын.", "eng": "I feel sick."},
            {"kaz": "Дәрігерге барайын.", "eng": "I should see a doctor."}
          ]
        },
        "tasks": [
          match("Дене мүшелерін аударыңыз:", [
            {"item": "Head", "match": "Бас"},
            {"item": "Hand", "match": "Қол"},
            {"item": "Leg", "match": "Аяқ"},
            {"item": "Eye", "match": "Көз"},
            {"item": "Ear", "match": "Құлақ"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "I have a [headache].", ["headache", "head", "happy", "hand"], "headache"),
          gaps("Дұрыс сөзді таңдаңыз:", "I feel [sick].", ["sick", "six", "sit", "set"], "sick"),
          order("Сөйлемді құрастырыңыз:", ["have", "I", "a", "headache", "."], "I have a headache."),
          order("Сөйлемді құрастырыңыз:", ["should", "I", "see", "a", "doctor", "."], "I should see a doctor.")
        ]
      }
    ]
  },
  {
    "title": "A2 Final Challenge",
    "lessons": [
      {
        "title": "Weather & Seasons",
        "theory": {
          "title": "Ауа райы мен жыл мезгілдері",
          "explanation": "Жыл мезгілдері: spring (көктем), summer (жаз), autumn (күз), winter (қыс). Ауа райы: sunny (күн шуақты), rainy (жаңбырлы), snowy (қарлы), windy (желді), cloudy (бұлтты). 'What is the weather like?' — Ауа райы қандай?",
          "examples": [
            {"kaz": "Бүгін күн шуақты.", "eng": "It is sunny today."},
            {"kaz": "Қыста қар жауады.", "eng": "It snows in winter."},
            {"kaz": "Ауа райы қандай?", "eng": "What is the weather like?"}
          ]
        },
        "tasks": [
          match("Ауа райы сөздерін аударыңыз:", [
            {"item": "Sunny", "match": "Күн шуақты"},
            {"item": "Rainy", "match": "Жаңбырлы"},
            {"item": "Snowy", "match": "Қарлы"},
            {"item": "Spring", "match": "Көктем"},
            {"item": "Winter", "match": "Қыс"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "It is [sunny] today.", ["sunny", "sun", "sunning", "suns"], "sunny"),
          gaps("Дұрыс сөзді таңдаңыз:", "It [snows] in winter.", ["snows", "snow", "snowed", "snowing"], "snows"),
          order("Сөйлемді құрастырыңыз:", ["is", "the", "What", "weather", "like", "?"], "What is the weather like?"),
          order("Сөйлемді құрастырыңыз:", ["is", "It", "cold", "today", "."], "It is cold today.")
        ]
      },
      {
        "title": "A2 Boss Battle",
        "theory": {
          "title": "A2 қорытынды тест",
          "explanation": "Барлық A2 тақырыптарын қайталау: Past Simple, хобби, дүкен, саяхат, сезімдер, болашақ жоспарлар, салыстыру, денсаулық, ауа райы. Сәттілік!",
          "examples": [
            {"kaz": "Мен кеше дүкенге бардым, сүт алдым.", "eng": "I went to the shop yesterday and bought milk."},
            {"kaz": "Ертең ауа райы жылы болады.", "eng": "Tomorrow the weather will be warm."}
          ]
        },
        "tasks": [
          match("Аралас тақырыптардан сөздерді сәйкестендіріңіз:", [
            {"item": "went", "match": "барды (past of go)"},
            {"item": "bigger", "match": "үлкенірек"},
            {"item": "will", "match": "болашақ"},
            {"item": "tired", "match": "шаршаған"},
            {"item": "expensive", "match": "қымбат"},
            {"item": "rainy", "match": "жаңбырлы"}
          ]),
          gaps("Дұрыс формасын таңдаңыз:", "She [went] to the shop yesterday.", ["went", "go", "goes", "going"], "went"),
          gaps("Дұрыс формасын таңдаңыз:", "He is [taller] than his brother.", ["taller", "tall", "tallest", "more tall"], "taller"),
          gaps("Дұрыс формасын таңдаңыз:", "I [will] visit you tomorrow.", ["will", "was", "am", "did"], "will"),
          order("Сөйлемді құрастырыңыз:", ["bought", "I", "milk", "the", "at", "shop", "."], "I bought milk at the shop."),
          order("Сөйлемді құрастырыңыз:", ["will", "The", "weather", "be", "warm", "tomorrow", "."], "The weather will be warm tomorrow.")
        ]
      }
    ]
  }
]


def seed_a2():
    old = Course.query.filter_by(level="A2").all()
    for c in old:
        mods = Module.query.filter_by(course_id=c.id).all()
        for m in mods:
            lsns = Lesson.query.filter_by(module_id=m.id).all()
            for l in lsns:
                Task.query.filter_by(lesson_id=l.id).delete()
            Lesson.query.filter_by(module_id=m.id).delete()
        Module.query.filter_by(course_id=c.id).delete()
    Course.query.filter_by(level="A2").delete()
    db.session.commit()

    course = Course(
        title="English A2: Elementary",
        description="Өткен шақ, хобби, дүкен, саяхат, сезімдер, болашақ жоспарлар, салыстыру, денсаулық.",
        language="English", level="A2"
    )
    db.session.add(course)
    db.session.flush()

    lesson_order = 0
    for m_idx, mod_data in enumerate(A2_MODULES):
        module = Module(course_id=course.id, title=mod_data["title"], order=m_idx + 1)
        db.session.add(module)
        db.session.flush()
        for l_data in mod_data["lessons"]:
            lesson_order += 1
            lesson = Lesson(module_id=module.id, title=l_data["title"], theory=l_data["theory"], order=lesson_order)
            db.session.add(lesson)
            db.session.flush()
            for t_idx, task in enumerate(l_data["tasks"]):
                task.lesson_id = lesson.id
                task.order = t_idx + 1
                db.session.add(task)
    db.session.commit()
    print(f"✅ A2 seeded: {lesson_order} lessons")


if __name__ == "__main__":
    with app.app_context():
        seed_a2()
        print("Done!")
