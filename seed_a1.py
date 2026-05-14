"""A1 Beginner English curriculum for Kazakh speakers. 10 lessons, 50+ real tasks."""
import os, sys
os.environ.setdefault("SECRET_KEY", "dev")
os.environ.setdefault("WEBHOOK_SECRET", "dev")
from app.main import create_app
from app.database import db
from app.models.db_models import Course, Module, Lesson, Task

app = create_app()

# ── Task helpers ──
def match(instruction, pairs):
    return Task(task_type="matching", content={"instruction": instruction, "pairs": pairs}, order=0)

def gaps(prompt, text, options, answer):
    return Task(task_type="gaps", content={"sentences": [{"prompt": prompt, "text": text, "options": options, "answer": answer}]}, order=0)

def order(prompt, words, correct):
    return Task(task_type="ordering", content={"sentences": [{"prompt": prompt, "words": words, "correct": correct}]}, order=0)

# ══════════════════════════════════════
#  A1 CURRICULUM DATA
# ══════════════════════════════════════

A1_MODULES = [
  {
    "title": "First Words",
    "lessons": [
      {
        "title": "Hello & Goodbye",
        "theory": {
          "title": "Сәлемдесу мен қоштасу",
          "explanation": "Ағылшын тілінде амандасу: 'Hello' — ресми, 'Hi' — бейресми. Қоштасу: 'Goodbye' — ресми, 'Bye' — бейресми. 'How are you?' — Қалыңыз қалай? деген мағына береді.",
          "examples": [
            {"kaz": "Сәлем!", "eng": "Hello!"},
            {"kaz": "Қалың қалай?", "eng": "How are you?"},
            {"kaz": "Жақсымын, рахмет.", "eng": "I am fine, thank you."},
            {"kaz": "Сау бол!", "eng": "Goodbye!"}
          ]
        },
        "tasks": [
          match("Сәлемдесу сөздерін аудармасымен сәйкестендіріңіз:", [
            {"item": "Hello", "match": "Сәлем"},
            {"item": "Goodbye", "match": "Сау бол"},
            {"item": "Thank you", "match": "Рахмет"},
            {"item": "Please", "match": "Өтінемін"}
          ]),
          match("Жауаптарды сәйкестендіріңіз:", [
            {"item": "How are you?", "match": "Қалың қалай?"},
            {"item": "I am fine", "match": "Мен жақсымын"},
            {"item": "Good morning", "match": "Қайырлы таң"},
            {"item": "Good night", "match": "Қайырлы түн"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "How [are] you?", ["are", "is", "am", "do"], "are"),
          gaps("Дұрыс сөзді таңдаңыз:", "I [am] fine, thank you.", ["am", "is", "are", "do"], "am"),
          order("Сөздерді дұрыс ретпен қойыңыз:", ["are", "How", "you", "?"], "How are you?"),
          order("Сөйлемді құрастырыңыз:", ["am", "I", "fine", "."], "I am fine.")
        ]
      },
      {
        "title": "Who Am I?",
        "theory": {
          "title": "Есімдіктер және 'to be'",
          "explanation": "Ағылшын тілінде жіктеу есімдіктері: I (мен), you (сен/сіз), he (ол — ер), she (ол — әйел), it (ол — зат), we (біз), they (олар). 'To be' етістігі: I am, you are, he/she/it is, we/they are.",
          "examples": [
            {"kaz": "Мен студентпін.", "eng": "I am a student."},
            {"kaz": "Ол мұғалім.", "eng": "She is a teacher."},
            {"kaz": "Біз достармыз.", "eng": "We are friends."},
            {"kaz": "Олар дәрігерлер.", "eng": "They are doctors."}
          ]
        },
        "tasks": [
          match("Есімдіктерді аударыңыз:", [
            {"item": "I", "match": "Мен"},
            {"item": "You", "match": "Сен / Сіз"},
            {"item": "He", "match": "Ол (ер)"},
            {"item": "She", "match": "Ол (әйел)"},
            {"item": "We", "match": "Біз"},
            {"item": "They", "match": "Олар"}
          ]),
          gaps("Дұрыс 'to be' формасын таңдаңыз:", "I [am] a student.", ["am", "is", "are", "be"], "am"),
          gaps("Дұрыс 'to be' формасын таңдаңыз:", "She [is] a teacher.", ["am", "is", "are", "be"], "is"),
          gaps("Дұрыс 'to be' формасын таңдаңыз:", "We [are] friends.", ["am", "is", "are", "be"], "are"),
          order("Сөйлемді құрастырыңыз:", ["is", "He", "a", "doctor", "."], "He is a doctor."),
          order("Сөйлемді құрастырыңыз:", ["are", "They", "students", "."], "They are students.")
        ]
      },
      {
        "title": "My Family",
        "theory": {
          "title": "Менің отбасым",
          "explanation": "Отбасы мүшелерін айтқанда 'my' (менің) сөзін қолданамыз. Father — әке, mother — ана, brother — аға/іні, sister — апа/сіңлі. 'This is my...' деген үлгіні қолданамыз.",
          "examples": [
            {"kaz": "Бұл менің анам.", "eng": "This is my mother."},
            {"kaz": "Менің әкем мұғалім.", "eng": "My father is a teacher."},
            {"kaz": "Менің сіңлім бар.", "eng": "I have a sister."}
          ]
        },
        "tasks": [
          match("Отбасы мүшелерін аударыңыз:", [
            {"item": "Mother", "match": "Ана"},
            {"item": "Father", "match": "Әке"},
            {"item": "Brother", "match": "Аға / Іні"},
            {"item": "Sister", "match": "Апа / Сіңлі"},
            {"item": "Grandmother", "match": "Әже"},
            {"item": "Grandfather", "match": "Ата"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "This is my [mother].", ["mother", "student", "book", "school"], "mother"),
          gaps("Дұрыс сөзді таңдаңыз:", "I [have] a brother.", ["have", "has", "am", "is"], "have"),
          order("Сөйлемді құрастырыңыз:", ["is", "my", "This", "father", "."], "This is my father."),
          order("Сөйлемді құрастырыңыз:", ["a", "have", "I", "sister", "."], "I have a sister.")
        ]
      }
    ]
  },
  {
    "title": "Numbers & Colors",
    "lessons": [
      {
        "title": "Numbers 1–20",
        "theory": {
          "title": "Сандар 1-ден 20-ға дейін",
          "explanation": "Ағылшын тіліндегі сандар: one (1), two (2), three (3), four (4), five (5), six (6), seven (7), eight (8), nine (9), ten (10). Eleven (11), twelve (12), thirteen (13)... twenty (20). Жасты айту: 'I am ten years old.'",
          "examples": [
            {"kaz": "Маған он жас.", "eng": "I am ten years old."},
            {"kaz": "Бес алма.", "eng": "Five apples."},
            {"kaz": "Он екі кітап.", "eng": "Twelve books."}
          ]
        },
        "tasks": [
          match("Сандарды аударыңыз:", [
            {"item": "One", "match": "Бір"},
            {"item": "Three", "match": "Үш"},
            {"item": "Five", "match": "Бес"},
            {"item": "Seven", "match": "Жеті"},
            {"item": "Ten", "match": "Он"},
            {"item": "Twenty", "match": "Жиырма"}
          ]),
          gaps("Дұрыс санды таңдаңыз:", "I am [ten] years old.", ["ten", "apple", "book", "school"], "ten"),
          gaps("Дұрыс санды таңдаңыз:", "There are [three] cats.", ["three", "red", "big", "fast"], "three"),
          order("Сөйлемді құрастырыңыз:", ["am", "I", "years", "twelve", "old", "."], "I am twelve years old."),
          order("Сөйлемді құрастырыңыз:", ["five", "have", "I", "books", "."], "I have five books.")
        ]
      },
      {
        "title": "Colors & Objects",
        "theory": {
          "title": "Түстер мен заттар",
          "explanation": "Негізгі түстер: red (қызыл), blue (көк), green (жасыл), yellow (сары), black (қара), white (ақ). Түсті зат алдында қоямыз: 'a red apple' (қызыл алма). 'What color is it?' — Бұл қандай түс?",
          "examples": [
            {"kaz": "Қызыл алма.", "eng": "A red apple."},
            {"kaz": "Аспан көк.", "eng": "The sky is blue."},
            {"kaz": "Бұл қандай түс?", "eng": "What color is it?"}
          ]
        },
        "tasks": [
          match("Түстерді аударыңыз:", [
            {"item": "Red", "match": "Қызыл"},
            {"item": "Blue", "match": "Көк"},
            {"item": "Green", "match": "Жасыл"},
            {"item": "Yellow", "match": "Сары"},
            {"item": "Black", "match": "Қара"},
            {"item": "White", "match": "Ақ"}
          ]),
          gaps("Дұрыс түсті таңдаңыз:", "The sky is [blue].", ["blue", "red", "five", "big"], "blue"),
          gaps("Дұрыс түсті таңдаңыз:", "The apple is [red].", ["red", "blue", "ten", "old"], "red"),
          order("Сөйлемді құрастырыңыз:", ["is", "The", "green", "grass", "."], "The grass is green."),
          order("Сөйлемді құрастырыңыз:", ["color", "What", "is", "it", "?"], "What color is it?")
        ]
      }
    ]
  },
  {
    "title": "Everyday Life",
    "lessons": [
      {
        "title": "Food & Drinks",
        "theory": {
          "title": "Тамақ пен сусындар",
          "explanation": "Тамақтар: bread (нан), milk (сүт), water (су), apple (алма), rice (күріш), meat (ет), tea (шай). 'I like...' — Маған ұнайды. 'I want...' — Мен қалаймын. 'Can I have...?' — Маған ... бере аласыз ба?",
          "examples": [
            {"kaz": "Маған шай ұнайды.", "eng": "I like tea."},
            {"kaz": "Мен су ішкім келеді.", "eng": "I want water."},
            {"kaz": "Маған нан бере аласыз ба?", "eng": "Can I have bread?"}
          ]
        },
        "tasks": [
          match("Тамақтарды аударыңыз:", [
            {"item": "Bread", "match": "Нан"},
            {"item": "Milk", "match": "Сүт"},
            {"item": "Water", "match": "Су"},
            {"item": "Tea", "match": "Шай"},
            {"item": "Meat", "match": "Ет"},
            {"item": "Apple", "match": "Алма"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "I [like] tea.", ["like", "likes", "am", "have"], "like"),
          gaps("Дұрыс сөзді таңдаңыз:", "Can I [have] water?", ["have", "has", "am", "like"], "have"),
          order("Сөйлемді құрастырыңыз:", ["like", "I", "bread", "."], "I like bread."),
          order("Сөйлемді құрастырыңыз:", ["want", "I", "milk", "."], "I want milk.")
        ]
      },
      {
        "title": "My Daily Routine",
        "theory": {
          "title": "Күнделікті іс-әрекет — Present Simple",
          "explanation": "Present Simple — әр күні қайталанатын іс-әрекеттер үшін: I wake up (мен оянамын), I eat (мен тамақтанамын), I go to school (мектепке барамын). He/she/it — етістікке -s/-es жалғанады: He eats, she goes.",
          "examples": [
            {"kaz": "Мен жеті сағатта оянамын.", "eng": "I wake up at seven."},
            {"kaz": "Ол мектепке барады.", "eng": "She goes to school."},
            {"kaz": "Біз кешке тамақтанамыз.", "eng": "We eat dinner."}
          ]
        },
        "tasks": [
          match("Күнделікті іс-әрекеттерді аударыңыз:", [
            {"item": "Wake up", "match": "Ояну"},
            {"item": "Eat breakfast", "match": "Таңғы ас ішу"},
            {"item": "Go to school", "match": "Мектепке бару"},
            {"item": "Do homework", "match": "Үй тапсырмасын орындау"},
            {"item": "Sleep", "match": "Ұйықтау"}
          ]),
          gaps("Дұрыс етістікті таңдаңыз:", "She [goes] to school.", ["goes", "go", "going", "gone"], "goes"),
          gaps("Дұрыс етістікті таңдаңыз:", "I [wake] up at seven.", ["wake", "wakes", "waking", "woke"], "wake"),
          gaps("Дұрыс етістікті таңдаңыз:", "He [eats] breakfast.", ["eats", "eat", "eating", "ate"], "eats"),
          order("Сөйлемді құрастырыңыз:", ["go", "I", "to", "school", "."], "I go to school."),
          order("Сөйлемді құрастырыңыз:", ["at", "up", "wake", "I", "seven", "."], "I wake up at seven.")
        ]
      },
      {
        "title": "At School",
        "theory": {
          "title": "Мектепте",
          "explanation": "Мектеп заттары: book (кітап), pen (қалам), desk (парта), teacher (мұғалім). Пәндер: math (математика), English (ағылшын тілі), science (жаратылыстану). 'I study...' — Мен ... оқимын.",
          "examples": [
            {"kaz": "Мен ағылшын тілін оқимын.", "eng": "I study English."},
            {"kaz": "Менің кітабым партада.", "eng": "My book is on the desk."},
            {"kaz": "Мұғалім жақсы.", "eng": "The teacher is good."}
          ]
        },
        "tasks": [
          match("Мектеп сөздерін аударыңыз:", [
            {"item": "Book", "match": "Кітап"},
            {"item": "Pen", "match": "Қалам"},
            {"item": "Desk", "match": "Парта"},
            {"item": "Teacher", "match": "Мұғалім"},
            {"item": "Student", "match": "Оқушы"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "I [study] English.", ["study", "studies", "eat", "go"], "study"),
          gaps("Дұрыс сөзді таңдаңыз:", "My book is [on] the desk.", ["on", "in", "at", "to"], "on"),
          order("Сөйлемді құрастырыңыз:", ["study", "I", "math", "."], "I study math."),
          order("Сөйлемді құрастырыңыз:", ["is", "The", "good", "teacher", "."], "The teacher is good.")
        ]
      }
    ]
  },
  {
    "title": "Questions & Places",
    "lessons": [
      {
        "title": "Asking Questions",
        "theory": {
          "title": "Сұрақтар қою",
          "explanation": "Ағылшын тілінде сұрақ сөздері: What (не?), Where (қайда?), Who (кім?), When (қашан?), How (қалай?). Сұрақтарда сөз тәртібі: сұрақ сөзі + am/is/are + бастауыш. 'What is your name?' — Сенің атың кім?",
          "examples": [
            {"kaz": "Сенің атың кім?", "eng": "What is your name?"},
            {"kaz": "Сен қайда тұрасың?", "eng": "Where do you live?"},
            {"kaz": "Бұл кім?", "eng": "Who is this?"}
          ]
        },
        "tasks": [
          match("Сұрақ сөздерін аударыңыз:", [
            {"item": "What", "match": "Не?"},
            {"item": "Where", "match": "Қайда?"},
            {"item": "Who", "match": "Кім?"},
            {"item": "When", "match": "Қашан?"},
            {"item": "How", "match": "Қалай?"},
            {"item": "Why", "match": "Неге?"}
          ]),
          gaps("Дұрыс сұрақ сөзін таңдаңыз:", "[What] is your name?", ["What", "Where", "Who", "When"], "What"),
          gaps("Дұрыс сұрақ сөзін таңдаңыз:", "[Where] do you live?", ["Where", "What", "Who", "How"], "Where"),
          order("Сұрақты құрастырыңыз:", ["is", "What", "your", "name", "?"], "What is your name?"),
          order("Сұрақты құрастырыңыз:", ["old", "How", "are", "you", "?"], "How old are you?")
        ]
      },
      {
        "title": "Places Around Me",
        "theory": {
          "title": "Менің айналамдағы орындар",
          "explanation": "Жиі қолданылатын орындар: home (үй), school (мектеп), shop (дүкен), park (саябақ), hospital (аурухана). Орын көрсету: 'in' (ішінде), 'on' (үстінде), 'at' (жанында), 'near' (қасында).",
          "examples": [
            {"kaz": "Мен мектептемін.", "eng": "I am at school."},
            {"kaz": "Дүкен саябақтың қасында.", "eng": "The shop is near the park."},
            {"kaz": "Ол үйде.", "eng": "She is at home."}
          ]
        },
        "tasks": [
          match("Орындарды аударыңыз:", [
            {"item": "Home", "match": "Үй"},
            {"item": "School", "match": "Мектеп"},
            {"item": "Shop", "match": "Дүкен"},
            {"item": "Park", "match": "Саябақ"},
            {"item": "Hospital", "match": "Аурухана"}
          ]),
          gaps("Дұрыс предлогты таңдаңыз:", "I am [at] school.", ["at", "on", "in", "to"], "at"),
          gaps("Дұрыс предлогты таңдаңыз:", "The cat is [on] the table.", ["on", "at", "in", "to"], "on"),
          order("Сөйлемді құрастырыңыз:", ["is", "She", "at", "home", "."], "She is at home."),
          order("Сөйлемді құрастырыңыз:", ["the", "near", "is", "The", "shop", "park", "."], "The shop is near the park.")
        ]
      }
    ]
  },
  {
    "title": "A1 Final Challenge",
    "lessons": [
      {
        "title": "A1 Boss Battle",
        "theory": {
          "title": "A1 қорытынды тест",
          "explanation": "Бұл A1 деңгейінің соңғы сабағы. Барлық тақырыптарды қайталаймыз: сәлемдесу, есімдіктер, отбасы, сандар, түстер, тамақ, күнделікті іс-әрекеттер, мектеп, сұрақтар, орындар. Сәттілік!",
          "examples": [
            {"kaz": "Менің атым Айдос. Маған 15 жас.", "eng": "My name is Aidos. I am 15 years old."},
            {"kaz": "Мен мектепке барамын. Маған математика ұнайды.", "eng": "I go to school. I like math."}
          ]
        },
        "tasks": [
          match("Барлық тақырыптан сөздерді сәйкестендіріңіз:", [
            {"item": "Good morning", "match": "Қайырлы таң"},
            {"item": "Grandfather", "match": "Ата"},
            {"item": "Fifteen", "match": "Он бес"},
            {"item": "Yellow", "match": "Сары"},
            {"item": "Hospital", "match": "Аурухана"},
            {"item": "Homework", "match": "Үй тапсырмасы"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "She [is] my sister.", ["is", "am", "are", "have"], "is"),
          gaps("Дұрыс сөзді таңдаңыз:", "He [goes] to school every day.", ["goes", "go", "going", "gone"], "goes"),
          gaps("Дұрыс сөзді таңдаңыз:", "[Where] is the park?", ["Where", "What", "Who", "How"], "Where"),
          order("Сөйлемді құрастырыңыз:", ["name", "My", "is", "Aidos", "."], "My name is Aidos."),
          order("Сөйлемді құрастырыңыз:", ["like", "I", "and", "tea", "bread", "."], "I like tea and bread.")
        ]
      }
    ]
  }
]


def seed_a1():
    """Seed A1 course with all modules, lessons and tasks."""
    # Remove old A1 data
    old = Course.query.filter_by(level="A1").all()
    for c in old:
        mods = Module.query.filter_by(course_id=c.id).all()
        for m in mods:
            lsns = Lesson.query.filter_by(module_id=m.id).all()
            for l in lsns:
                Task.query.filter_by(lesson_id=l.id).delete()
            Lesson.query.filter_by(module_id=m.id).delete()
        Module.query.filter_by(course_id=c.id).delete()
    Course.query.filter_by(level="A1").delete()
    db.session.commit()

    course = Course(
        title="English A1: Beginner",
        description="Ағылшын тілін нөлден үйрену. Сәлемдесу, отбасы, сандар, түстер, тамақ, күнделікті іс-әрекеттер.",
        language="English",
        level="A1"
    )
    db.session.add(course)
    db.session.flush()

    lesson_order = 0
    for m_idx, mod_data in enumerate(A1_MODULES):
        module = Module(course_id=course.id, title=mod_data["title"], order=m_idx + 1)
        db.session.add(module)
        db.session.flush()

        for l_data in mod_data["lessons"]:
            lesson_order += 1
            lesson = Lesson(
                module_id=module.id,
                title=l_data["title"],
                theory=l_data["theory"],
                order=lesson_order
            )
            db.session.add(lesson)
            db.session.flush()

            for t_idx, task in enumerate(l_data["tasks"]):
                task.lesson_id = lesson.id
                task.order = t_idx + 1
                db.session.add(task)

    db.session.commit()
    print(f"✅ A1 seeded: {lesson_order} lessons")


if __name__ == "__main__":
    with app.app_context():
        seed_a1()
        print("Done!")
