import os

path = '/Users/tolegenayat/SimbaAI/simpai-backend/app/services/content_service.py'

replacements = {
    '("Colors (Түстер)", [\n                {"type": "matching", "instruction": "Match colors:", "pairs": [{"left": "Қызыл", "right": "Red"}, {"left": "Көк", "right": "Blue"}, {"left": "Сары", "right": "Yellow"}, {"left": "Ақ", "right": "White"}]}\n            ])': 
    '("Colors (Түстер)", [\n                {"type": "matching", "instruction": "Match colors:", "pairs": [{"left": "Қызыл", "right": "Red"}, {"left": "Көк", "right": "Blue"}, {"left": "Сары", "right": "Yellow"}, {"left": "Ақ", "right": "White"}]},\n                {"type": "matching", "instruction": "More colors:", "pairs": [{"left": "Қара", "right": "Black"}, {"left": "Жасыл", "right": "Green"}, {"left": "Қоңыр", "right": "Brown"}]},\n                {"type": "gaps", "instruction": "The grass is green:", "sentences": [{"text": "Шөп [жасыл].", "answer": "жасыл"}]},\n                {"type": "ordering", "instruction": "The sky is blue:", "sentences": [{"words": ["Аспан", "көк"], "correct": "Аспан көк"}]},\n                {"type": "ordering", "instruction": "Red apple:", "sentences": [{"words": ["Қызыл", "алма"], "correct": "Қызыл алма"}]}\n            ])',
    
    '("Common Objects (Күнделікті заттар)", [\n                {"type": "matching", "instruction": "Match objects:", "pairs": [{"left": "Кітап", "right": "Book"}, {"left": "Қалам", "right": "Pen"}, {"left": "Үстел", "right": "Table"}, {"left": "Орындық", "right": "Chair"}]}\n            ])':
    '("Common Objects (Күнделікті заттар)", [\n                {"type": "matching", "instruction": "Match objects:", "pairs": [{"left": "Кітап", "right": "Book"}, {"left": "Қалам", "right": "Pen"}, {"left": "Үстел", "right": "Table"}, {"left": "Орындық", "right": "Chair"}]},\n                {"type": "matching", "instruction": "Office items:", "pairs": [{"left": "Дәптер", "right": "Notebook"}, {"left": "Сызғыш", "right": "Ruler"}, {"left": "Өшіргіш", "right": "Eraser"}]},\n                {"type": "gaps", "instruction": "This is a book:", "sentences": [{"text": "Бұл [кітап].", "answer": "кітап"}]},\n                {"type": "ordering", "instruction": "My pen is on the table:", "sentences": [{"words": ["Қаламым", "үстелде", "жатыр"], "correct": "Қаламым үстелде жатыр"}]}\n            ])',
    
    '("Body Parts (Дене мүшелері)", [\n                {"type": "matching", "instruction": "Match body parts:", "pairs": [{"left": "Бас", "right": "Head"}, {"left": "Көз", "right": "Eye"}, {"left": "Қол", "right": "Hand"}, {"left": "Аяқ", "right": "Leg"}]}\n            ])':
    '("Body Parts (Дене мүшелері)", [\n                {"type": "matching", "instruction": "Match body parts:", "pairs": [{"left": "Бас", "right": "Head"}, {"left": "Көз", "right": "Eye"}, {"left": "Қол", "right": "Hand"}, {"left": "Аяқ", "right": "Leg"}]},\n                {"type": "matching", "instruction": "Face parts:", "pairs": [{"left": "Мұрын", "right": "Nose"}, {"left": "Ауыз", "right": "Mouth"}, {"left": "Құлақ", "right": "Ear"}]},\n                {"type": "ordering", "instruction": "Two eyes:", "sentences": [{"words": ["Екі", "көз"], "correct": "Екі көз"}]},\n                {"type": "gaps", "instruction": "Wash your hands:", "sentences": [{"text": "[Қолыңды] жу.", "answer": "Қолыңды"}]}\n            ])',

    '("Food and Drinks (Тағамдар мен сусындар)", [\n                {"type": "matching", "instruction": "Match food/drinks:", "pairs": [{"left": "Нан", "right": "Bread"}, {"left": "Су", "right": "Water"}, {"left": "Шай", "right": "Tea"}, {"left": "Сүт", "right": "Milk"}]}\n            ])':
    '("Food and Drinks (Тағамдар мен сусындар)", [\n                {"type": "matching", "instruction": "Match food/drinks:", "pairs": [{"left": "Нан", "right": "Bread"}, {"left": "Су", "right": "Water"}, {"left": "Шай", "right": "Tea"}, {"left": "Сүт", "right": "Milk"}]},\n                {"type": "matching", "instruction": "Main food:", "pairs": [{"left": "Ет", "right": "Meat"}, {"left": "Күріш", "right": "Rice"}, {"left": "Тұз", "right": "Salt"}]},\n                {"type": "gaps", "instruction": "I drink tea:", "sentences": [{"text": "Мен [шай] ішемін.", "answer": "шай"}]},\n                {"type": "ordering", "instruction": "The bread is tasty:", "sentences": [{"words": ["Нан", "дәмді"], "correct": "Нан дәмді"}]},\n                {"type": "ordering", "instruction": "Give me water:", "sentences": [{"words": ["Маған", "су", "беріңіз"], "correct": "Маған су беріңіз"}]}\n            ])',

    '("Animals (Жануарлар)", [\n                {"type": "matching", "instruction": "Match animals:", "pairs": [{"left": "Ат", "right": "Horse"}, {"left": "Түйе", "right": "Camel"}, {"left": "Қой", "right": "Sheep"}, {"left": "Ит", "right": "Dog"}]}\n            ])':
    '("Animals (Жануарлар)", [\n                {"type": "matching", "instruction": "Match animals:", "pairs": [{"left": "Ат", "right": "Horse"}, {"left": "Түйе", "right": "Camel"}, {"left": "Қой", "right": "Sheep"}, {"left": "Ит", "right": "Dog"}]},\n                {"type": "matching", "instruction": "More animals:", "pairs": [{"left": "Мысық", "right": "Cat"}, {"left": "Сиыр", "right": "Cow"}, {"left": "Тауық", "right": "Chicken"}]},\n                {"type": "ordering", "instruction": "The dog is big:", "sentences": [{"words": ["Ит", "үлкен"], "correct": "Ит үлкен"}]},\n                {"type": "gaps", "instruction": "The cat is small:", "sentences": [{"text": "Мысық [кішкентай].", "answer": "кішкентай"}]}\n            ])'
}

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

for old, new in replacements.items():
    if old in content:
        print(f"Replacing block...")
        content = content.replace(old, new)
    else:
        print(f"Block not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
