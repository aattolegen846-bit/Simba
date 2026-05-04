import os

path = '/Users/tolegenayat/SimbaAI/simpai-backend/app/services/content_service.py'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# We want to add or modify tasks to be "Translate from Kazakh to English"
# Currently, most ordering tasks are English -> Kazakh.
# Let's add some Kazakh -> English ones.

# Example modification:
# Original: {"words": ["Менің", "әжем", "мейірімді"], "correct": "Менің әжем мейірімді"} (English Speaker learning Kazakh, output is Kazakh)
# Requested: Task is Kazakh, Student responds in English.

# I'll add a new set of tasks to the A1 course that are specifically "Kazakh to English"
new_tasks_snippet = """
                {"type": "ordering", "instruction": "Translate to English:", "sentences": [{"words": ["I", "am", "from", "Kazakhstan"], "correct": "I am from Kazakhstan", "prompt": "Мен Қазақстаннанмын"}]},
                {"type": "ordering", "instruction": "Translate to English:", "sentences": [{"words": ["What", "is", "your", "name?"], "correct": "What is your name?", "prompt": "Сіздің атыңыз кім?"}]},
                {"type": "gaps", "instruction": "Translate the missing word to English:", "sentences": [{"text": "Менің [name] Арман.", "answer": "name", "prompt": "Менің атым Арман"}]},
"""

# I'll use a script to inject these into the "Basics of Kazakh" module
if 'mod_a1 = Module(course_id=kazakh_a1.id, title="Basics of Kazakh", order=1)' in content:
    # Find where the tasks are added for the first lessons of mod_a1
    # I'll just add a new lesson specifically for Kazakh to English practice
    
    injection = """
        les_rev = Lesson(module_id=mod_a1.id, title="Kazakh to English Practice", order=10)
        db.session.add(les_rev)
        db.session.flush()
        
        rev_tasks = [
            {"type": "ordering", "instruction": "Translate to English:", "sentences": [{"words": ["My", "name", "is", "Arman"], "correct": "My name is Arman", "prompt": "Менің атым Арман"}]},
            {"type": "ordering", "instruction": "Translate to English:", "sentences": [{"words": ["How", "are", "you?"], "correct": "How are you?", "prompt": "Қалыңыз қалай?"}]},
            {"type": "ordering", "instruction": "Translate to English:", "sentences": [{"words": ["The", "apple", "is", "red"], "correct": "The apple is red", "prompt": "Алма қызыл"}]},
            {"type": "ordering", "instruction": "Translate to English:", "sentences": [{"words": ["I", "drink", "tea"], "correct": "I drink tea", "prompt": "Мен шай ішемін"}]},
            {"type": "gaps", "instruction": "Translate to English:", "sentences": [{"text": "The [grass] is green.", "answer": "grass", "prompt": "Шөп жасыл"}]}
        ]
        for t_data in rev_tasks:
            db.session.add(Task(lesson_id=les_rev.id, task_type=t_data["type"], content=t_data))
    """
    
    # Insert before the end of the seed function
    content = content.replace('        db.session.commit()', injection + '\n        db.session.commit()', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reversed tasks added!")
