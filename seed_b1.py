"""B1 Intermediate English curriculum for Kazakh speakers. 10 lessons."""
import os
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

B1_MODULES = [
  {
    "title": "Experiences",
    "lessons": [
      {
        "title": "Have You Ever...?",
        "theory": {
          "title": "Present Perfect — Тәжірибе",
          "explanation": "Present Perfect 'have/has + V3' өмірдегі тәжірибені білдіреді. 'I have visited London' — Мен Лондонда болдым (қашан екені маңызды емес). Ever — қашан да болса, never — ешқашан. 'Have you ever tried sushi?' — Сен суши жеп көрдің бе?",
          "examples": [
            {"kaz": "Мен Лондонда болдым.", "eng": "I have visited London."},
            {"kaz": "Ол ешқашан ұшақпен ұшқан жоқ.", "eng": "She has never flown on a plane."},
            {"kaz": "Сен суши жеп көрдің бе?", "eng": "Have you ever tried sushi?"}
          ]
        },
        "tasks": [
          match("Past Participle (V3) формаларын сәйкестендіріңіз:", [
            {"item": "go", "match": "gone"},
            {"item": "see", "match": "seen"},
            {"item": "eat", "match": "eaten"},
            {"item": "fly", "match": "flown"},
            {"item": "write", "match": "written"},
            {"item": "speak", "match": "spoken"}
          ]),
          gaps("Дұрыс формасын таңдаңыз:", "I have [visited] London.", ["visited", "visit", "visiting", "visits"], "visited"),
          gaps("Дұрыс формасын таңдаңыз:", "She has [never] flown on a plane.", ["never", "ever", "always", "already"], "never"),
          gaps("Дұрыс формасын таңдаңыз:", "Have you [ever] tried sushi?", ["ever", "never", "always", "yet"], "ever"),
          order("Сөйлемді құрастырыңыз:", ["have", "I", "seen", "that", "movie", "."], "I have seen that movie."),
          order("Сұрақты құрастырыңыз:", ["you", "Have", "ever", "been", "to", "Paris", "?"], "Have you ever been to Paris?")
        ]
      },
      {
        "title": "Telling Stories",
        "theory": {
          "title": "Оқиға айту — Past Simple vs Past Continuous",
          "explanation": "Past Continuous 'was/were + -ing' — өткен шақтағы үдеріс. Past Simple — аяқталған іс. Екеуін бірге қолданамыз: 'I was walking when it started to rain.' — Мен жүріп бара жатқанда жаңбыр жауа бастады. 'While' — кезінде, 'when' — қашан.",
          "examples": [
            {"kaz": "Мен жүріп бара жатқанда жаңбыр жауды.", "eng": "I was walking when it started to rain."},
            {"kaz": "Ол кітап оқып отырған кезде телефон шылдырлады.", "eng": "She was reading when the phone rang."},
            {"kaz": "Олар ұйықтап жатқан кезде не болды?", "eng": "What happened while they were sleeping?"}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "I [was walking] when it started to rain.", ["was walking", "walked", "walk", "am walking"], "was walking"),
          gaps("Дұрыс формасын таңдаңыз:", "She was reading when the phone [rang].", ["rang", "ring", "was ringing", "rings"], "rang"),
          gaps("Дұрыс формасын таңдаңыз:", "While they [were sleeping], the cat escaped.", ["were sleeping", "slept", "sleep", "are sleeping"], "were sleeping"),
          order("Сөйлемді құрастырыңыз:", ["was", "I", "cooking", "when", "he", "arrived", "."], "I was cooking when he arrived."),
          order("Сөйлемді құрастырыңыз:", ["were", "They", "playing", "when", "it", "started", "raining", "."], "They were playing when it started raining.")
        ]
      }
    ]
  },
  {
    "title": "Work & Study",
    "lessons": [
      {
        "title": "My Job",
        "theory": {
          "title": "Жұмыс туралы сөйлесу",
          "explanation": "Мамандықтар: engineer (инженер), lawyer (заңгер), nurse (медбике), programmer (бағдарламашы). 'What do you do?' — Сіз кім боласыз? (мамандық туралы). 'I work as a...' — Мен ... болып жұмыс істеймін. 'I am responsible for...' — Мен ... жауаптымын.",
          "examples": [
            {"kaz": "Мен бағдарламашымын.", "eng": "I am a programmer."},
            {"kaz": "Ол мұғалім болып жұмыс істейді.", "eng": "She works as a teacher."},
            {"kaz": "Мен жобаларға жауаптымын.", "eng": "I am responsible for projects."}
          ]
        },
        "tasks": [
          match("Мамандықтарды аударыңыз:", [
            {"item": "Engineer", "match": "Инженер"},
            {"item": "Lawyer", "match": "Заңгер"},
            {"item": "Nurse", "match": "Медбике"},
            {"item": "Programmer", "match": "Бағдарламашы"},
            {"item": "Accountant", "match": "Бухгалтер"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "She works [as] a teacher.", ["as", "like", "is", "for"], "as"),
          gaps("Дұрыс сөзді таңдаңыз:", "I am [responsible] for projects.", ["responsible", "response", "respond", "responsibility"], "responsible"),
          order("Сөйлемді құрастырыңыз:", ["do", "What", "you", "do", "?"], "What do you do?"),
          order("Сөйлемді құрастырыңыз:", ["as", "works", "He", "an", "engineer", "."], "He works as an engineer.")
        ]
      },
      {
        "title": "Education & Skills",
        "theory": {
          "title": "Білім мен дағдылар — Modal verbs",
          "explanation": "Can — қабілет: 'I can speak English.' Should — кеңес: 'You should study more.' Must — міндет: 'You must pass the exam.' Have to — керек: 'I have to finish my homework.'",
          "examples": [
            {"kaz": "Мен ағылшынша сөйлей аламын.", "eng": "I can speak English."},
            {"kaz": "Сен көбірек оқу керек.", "eng": "You should study more."},
            {"kaz": "Мен емтиханды тапсыруым керек.", "eng": "I must pass the exam."}
          ]
        },
        "tasks": [
          match("Модальді етістіктерді мағынасымен сәйкестендіріңіз:", [
            {"item": "can", "match": "қабілет (алу)"},
            {"item": "should", "match": "кеңес (керек)"},
            {"item": "must", "match": "міндет (тиіс)"},
            {"item": "have to", "match": "қажеттілік (керек)"},
            {"item": "might", "match": "мүмкіндік (шығар)"}
          ]),
          gaps("Дұрыс модальді етістікті таңдаңыз:", "You [should] study more.", ["should", "can", "will", "are"], "should"),
          gaps("Дұрыс модальді етістікті таңдаңыз:", "I [can] speak three languages.", ["can", "should", "must", "have"], "can"),
          gaps("Дұрыс модальді етістікті таңдаңыз:", "You [must] wear a uniform at school.", ["must", "can", "might", "would"], "must"),
          order("Сөйлемді құрастырыңыз:", ["can", "I", "speak", "English", "."], "I can speak English."),
          order("Сөйлемді құрастырыңыз:", ["should", "You", "study", "harder", "."], "You should study harder.")
        ]
      }
    ]
  },
  {
    "title": "Opinions & Social",
    "lessons": [
      {
        "title": "What Do You Think?",
        "theory": {
          "title": "Пікір білдіру",
          "explanation": "'I think...' — Менің ойымша. 'In my opinion...' — Менің пікірімше. 'I agree/disagree' — Мен келісемін/келіспеймін. 'I believe...' — Мен сенемін. Пікір сұрау: 'What do you think about...?' — ...туралы не ойлайсың?",
          "examples": [
            {"kaz": "Менің ойымша, бұл жақсы идея.", "eng": "I think this is a good idea."},
            {"kaz": "Мен келіспеймін.", "eng": "I disagree."},
            {"kaz": "Білім туралы не ойлайсың?", "eng": "What do you think about education?"}
          ]
        },
        "tasks": [
          match("Пікір сөздерін аударыңыз:", [
            {"item": "I think", "match": "Менің ойымша"},
            {"item": "I agree", "match": "Мен келісемін"},
            {"item": "I disagree", "match": "Мен келіспеймін"},
            {"item": "In my opinion", "match": "Менің пікірімше"},
            {"item": "I believe", "match": "Мен сенемін"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "I [think] this is a good idea.", ["think", "thinking", "thought", "thinks"], "think"),
          gaps("Дұрыс сөзді таңдаңыз:", "What do you think [about] education?", ["about", "for", "to", "on"], "about"),
          order("Сөйлемді құрастырыңыз:", ["think", "I", "is", "this", "important", "."], "I think this is important."),
          order("Сөйлемді құрастырыңыз:", ["you", "do", "What", "think", "?"], "What do you think?")
        ]
      },
      {
        "title": "Making Plans Together",
        "theory": {
          "title": "Бірге жоспар құру",
          "explanation": "Ұсыну: 'Let\\'s go...' — Жүр, барайық. 'How about...?' — ...қалай? 'Why don\\'t we...?' — Неге ... жасамасқа? Келісу: 'Sure!' — Әрине! 'Sounds good!' — Жақсы естіледі! Бас тарту: 'Sorry, I can\\'t.' — Кешіріңіз, мен жасай алмаймын.",
          "examples": [
            {"kaz": "Жүр, кинога барайық.", "eng": "Let's go to the cinema."},
            {"kaz": "Саябақта серуендеу қалай?", "eng": "How about walking in the park?"},
            {"kaz": "Жақсы естіледі!", "eng": "Sounds good!"}
          ]
        },
        "tasks": [
          match("Ұсыну сөздерін сәйкестендіріңіз:", [
            {"item": "Let's go", "match": "Жүр, барайық"},
            {"item": "How about...?", "match": "...қалай?"},
            {"item": "Sure!", "match": "Әрине!"},
            {"item": "Sounds good!", "match": "Жақсы естіледі!"},
            {"item": "Sorry, I can't", "match": "Кешіріңіз, алмаймын"}
          ]),
          gaps("Дұрыс сөзді таңдаңыз:", "[Let's] go to the cinema.", ["Let's", "Let", "Lets", "Let is"], "Let's"),
          gaps("Дұрыс сөзді таңдаңыз:", "How [about] walking in the park?", ["about", "for", "to", "is"], "about"),
          order("Сөйлемді құрастырыңыз:", ["go", "Let's", "to", "the", "cinema", "."], "Let's go to the cinema."),
          order("Сөйлемді құрастырыңыз:", ["about", "How", "having", "dinner", "together", "?"], "How about having dinner together?")
        ]
      }
    ]
  },
  {
    "title": "Problem Solving",
    "lessons": [
      {
        "title": "If This, Then That",
        "theory": {
          "title": "Шартты сөйлемдер — First Conditional",
          "explanation": "First Conditional — нақты болашақ мүмкіндік: 'If + Present Simple, will + V1'. 'If it rains, I will stay home.' — Егер жаңбыр жауса, мен үйде қаламын. 'If you study hard, you will pass.' — Егер жақсы оқысаң, тапсырасың.",
          "examples": [
            {"kaz": "Егер жаңбыр жауса, мен үйде қаламын.", "eng": "If it rains, I will stay home."},
            {"kaz": "Егер жақсы оқысаң, емтиханды тапсырасың.", "eng": "If you study hard, you will pass the exam."},
            {"kaz": "Егер ол келсе, мен қуанамын.", "eng": "If she comes, I will be happy."}
          ]
        },
        "tasks": [
          gaps("Дұрыс формасын таңдаңыз:", "If it [rains], I will stay home.", ["rains", "rain", "will rain", "rained"], "rains"),
          gaps("Дұрыс формасын таңдаңыз:", "If you study hard, you [will] pass.", ["will", "would", "can", "did"], "will"),
          gaps("Дұрыс формасын таңдаңыз:", "If she [comes], I will be happy.", ["comes", "come", "will come", "came"], "comes"),
          order("Сөйлемді құрастырыңыз:", ["rains", "If", "it", ",", "will", "I", "stay", "home", "."], "If it rains, I will stay home."),
          order("Сөйлемді құрастырыңыз:", ["study", "If", "you", ",", "will", "you", "pass", "."], "If you study, you will pass.")
        ]
      },
      {
        "title": "Giving Advice",
        "theory": {
          "title": "Кеңес беру",
          "explanation": "'You should...' — Сен ... керексің. 'If I were you, I would...' — Мен сенің орнында ... істер едім. 'Why don\\'t you...?' — Неге ... жасамайсың? 'It might help to...' — ...көмектесуі мүмкін.",
          "examples": [
            {"kaz": "Сен дәрігерге бару керексің.", "eng": "You should see a doctor."},
            {"kaz": "Мен сенің орнында демалар едім.", "eng": "If I were you, I would take a rest."},
            {"kaz": "Неге жаттығу жасамайсың?", "eng": "Why don't you exercise?"}
          ]
        },
        "tasks": [
          gaps("Дұрыс сөзді таңдаңыз:", "You [should] see a doctor.", ["should", "would", "can", "will"], "should"),
          gaps("Дұрыс сөзді таңдаңыз:", "If I [were] you, I would rest.", ["were", "was", "am", "is"], "were"),
          gaps("Дұрыс сөзді таңдаңыз:", "Why [don't] you try again?", ["don't", "do", "didn't", "won't"], "don't"),
          order("Сөйлемді құрастырыңыз:", ["should", "You", "see", "a", "doctor", "."], "You should see a doctor."),
          order("Сөйлемді құрастырыңыз:", ["were", "If", "I", "you", ",", "would", "I", "rest", "."], "If I were you, I would rest.")
        ]
      }
    ]
  },
  {
    "title": "B1 Final Challenge",
    "lessons": [
      {
        "title": "Passive Voice",
        "theory": {
          "title": "Ырықсыз етіс — Passive Voice",
          "explanation": "Passive Voice — іс-әрекет бастауышқа бағытталған: 'is/are/was/were + V3'. 'The book was written by Abai.' — Кітапты Абай жазды. 'English is spoken worldwide.' — Ағылшын тілі бүкіл әлемде сөйленеді.",
          "examples": [
            {"kaz": "Кітапты Абай жазды.", "eng": "The book was written by Abai."},
            {"kaz": "Ағылшын тілі бүкіл әлемде сөйленеді.", "eng": "English is spoken worldwide."},
            {"kaz": "Бұл мейрамхана 2020 жылы ашылды.", "eng": "This restaurant was opened in 2020."}
          ]
        },
        "tasks": [
          gaps("Passive Voice формасын таңдаңыз:", "The book [was written] by Abai.", ["was written", "wrote", "writes", "is writing"], "was written"),
          gaps("Passive Voice формасын таңдаңыз:", "English [is spoken] worldwide.", ["is spoken", "speaks", "spoke", "speaking"], "is spoken"),
          gaps("Дұрыс формасын таңдаңыз:", "The cake [was made] by my mother.", ["was made", "made", "makes", "is making"], "was made"),
          order("Сөйлемді құрастырыңыз:", ["was", "The", "letter", "written", "yesterday", "."], "The letter was written yesterday."),
          order("Сөйлемді құрастырыңыз:", ["is", "Rice", "eaten", "in", "many", "countries", "."], "Rice is eaten in many countries.")
        ]
      },
      {
        "title": "B1 Boss Battle",
        "theory": {
          "title": "B1 қорытынды тест",
          "explanation": "Барлық B1 тақырыптарын қайталау: Present Perfect, Past Continuous, мамандықтар, модальді етістіктер, пікір білдіру, шартты сөйлемдер, кеңес беру, Passive Voice. Сәттілік!",
          "examples": [
            {"kaz": "Мен Лондонда болдым, ол маған ұнады.", "eng": "I have been to London, I liked it."},
            {"kaz": "Егер жақсы оқысаң, жұмыс табасың.", "eng": "If you study well, you will find a job."}
          ]
        },
        "tasks": [
          match("B1 тақырыптарынан сөздерді сәйкестендіріңіз:", [
            {"item": "have visited", "match": "болдым (Present Perfect)"},
            {"item": "was walking", "match": "жүріп бара жатты (Past Continuous)"},
            {"item": "should", "match": "керек (кеңес)"},
            {"item": "If...will", "match": "Егер...болады (First Conditional)"},
            {"item": "was written", "match": "жазылды (Passive Voice)"}
          ]),
          gaps("Дұрыс формасын таңдаңыз:", "I [have been] to London twice.", ["have been", "was", "am", "went"], "have been"),
          gaps("Дұрыс формасын таңдаңыз:", "The letter [was sent] yesterday.", ["was sent", "sent", "sends", "is sending"], "was sent"),
          gaps("Дұрыс формасын таңдаңыз:", "If you [practice], you will improve.", ["practice", "will practice", "practiced", "practices"], "practice"),
          order("Сөйлемді құрастырыңыз:", ["have", "I", "never", "been", "to", "Japan", "."], "I have never been to Japan."),
          order("Сөйлемді құрастырыңыз:", ["should", "You", "read", "more", "books", "."], "You should read more books.")
        ]
      }
    ]
  }
]

def seed_b1():
    old = Course.query.filter_by(level="B1").all()
    for c in old:
        for m in Module.query.filter_by(course_id=c.id).all():
            for l in Lesson.query.filter_by(module_id=m.id).all():
                Task.query.filter_by(lesson_id=l.id).delete()
            Lesson.query.filter_by(module_id=m.id).delete()
        Module.query.filter_by(course_id=c.id).delete()
    Course.query.filter_by(level="B1").delete()
    db.session.commit()

    course = Course(title="English B1: Intermediate", description="Present Perfect, Past Continuous, модальді етістіктер, шартты сөйлемдер, Passive Voice.", language="English", level="B1")
    db.session.add(course); db.session.flush()
    lo = 0
    for mi, md in enumerate(B1_MODULES):
        mod = Module(course_id=course.id, title=md["title"], order=mi+1)
        db.session.add(mod); db.session.flush()
        for ld in md["lessons"]:
            lo += 1
            les = Lesson(module_id=mod.id, title=ld["title"], theory=ld["theory"], order=lo)
            db.session.add(les); db.session.flush()
            for ti, t in enumerate(ld["tasks"]):
                t.lesson_id = les.id; t.order = ti+1; db.session.add(t)
    db.session.commit()
    print(f"✅ B1 seeded: {lo} lessons")

if __name__ == "__main__":
    with app.app_context(): seed_b1()
