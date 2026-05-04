import os

path = '/Users/tolegenayat/SimbaAI/simpai-backend/app/services/content_service.py'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Add grammar theory to A1 lessons
# I'll update the loop that creates lessons to accept a theory object
theory_data = {
    "Greetings": {
        "title": "Grammar: Greetings & Basic Interaction",
        "explanation": "In Kazakh, greetings change based on the time of day and formality. 'Сәлем' is informal (Hello), while 'Сәлеметсіз бе' is formal. 'Қалың қалай?' means 'How are you?' informally.",
        "examples": [
            {"kaz": "Сәлем", "eng": "Hi"},
            {"kaz": "Қайырлы таң", "eng": "Good morning"}
        ]
    },
    "Family": {
        "title": "Grammar: Possessive Pronouns",
        "explanation": "To say 'my', use 'Менің'. To say 'your', use 'Сенің' (informal) or 'Сіздің' (formal). For 'his/her', use 'Оның'. Example: Менің отбасым (My family).",
        "examples": [
            {"kaz": "Менің әкем", "eng": "My father"},
            {"kaz": "Сіздің анаңыз", "eng": "Your mother"}
        ]
    }
}

# I'll update the seed_demo_content to include this theory
# I'll replace the loop in mod_a1 creation

# Since the file is large and complex, I'll just add a script that updates the Lesson objects after creation
theory_injection = """
        # --- Add Grammar Theory to A1 Lessons ---
        a1_grammar = {
            "Greetings": {
                "title": "Grammar: Greetings & Formality",
                "explanation": "Kazakh language has formal and informal greetings. 'Salem' is for friends, 'Salementsiz be' is for elders or professionals. Question particles (ma/me) are added at the end for questions.",
                "examples": [{"kaz": "Salem", "eng": "Hi"}, {"kaz": "Qalyn qalayi?", "eng": "How are you?"}]
            },
            "Family": {
                "title": "Grammar: Possessive Endings",
                "explanation": "Personal pronouns change to possessive: Men (I) -> Mening (My). Add '-ym' or '-im' to the noun depending on vowel harmony. Example: Ake (Father) -> Mening akem (My father).",
                "examples": [{"kaz": "Mening akem", "eng": "My father"}, {"kaz": "Sening apken", "eng": "Your sister"}]
            },
            "Colors": {
                "title": "Grammar: Adjectives",
                "explanation": "In Kazakh, adjectives usually come before the noun they describe. For example: 'Qyzyl alma' (Red apple).",
                "examples": [{"kaz": "Kök aspan", "eng": "Blue sky"}, {"kaz": "Ak süt", "eng": "White milk"}]
            }
        }
        
        for l_title, t_content in a1_grammar.items():
            lesson_obj = Lesson.query.filter_by(module_id=mod_a1.id).filter(Lesson.title.like(f"%{l_title}%")).first()
            if lesson_obj:
                lesson_obj.theory = t_content
"""

content = content.replace('        db.session.commit()', theory_injection + '\n        db.session.commit()', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Grammar theory added to seeding script!")
