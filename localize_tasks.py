import os
import re

path = '/Users/tolegenayat/SimbaAI/simpai-backend/app/services/content_service.py'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

new_lines = []

# Translation map for instructions
instruction_map = {
    "Match colors:": "Түстерді сәйкестендіріңіз:",
    "Match objects:": "Заттарды сәйкестендіріңіз:",
    "Match body parts:": "Дене мүшелерін сәйкестендіріңіз:",
    "Match food/drinks:": "Тағамдар мен сусындарды сәйкестендіріңіз:",
    "Match plants:": "Өсімдіктерді сәйкестендіріңіз:",
    "Match animals:": "Жануарларды сәйкестендіріңіз:",
    "Match seasons:": "Мезгілдерді сәйкестендіріңіз:",
    "Match weather:": "Ауа райын сәйкестендіріңіз:",
    "Match rooms:": "Бөлмелерді сәйкестендіріңіз:",
    "Match kitchen items:": "Асхана заттарын сәйкестендіріңіз:",
    "Match clothes:": "Киімдерді сәйкестендіріңіз:",
    "Match transport:": "Көліктерді сәйкестендіріңіз:",
    "Match places:": "Орындарды сәйкестендіріңіз:",
    "Translate to English:": "Ағылшыншаға аударыңыз:",
    "Order the words:": "Сөздерді ретімен қойыңыз:",
    "Fill the gap:": "Бос орынды толтырыңыз:",
    "One, two, three:": "Бір, екі, үш:",
    "Good night:": "Қайырлы түн:",
    "The grass is green:": "Шөп жасыл:"
}

for line in lines:
    # 1. Reverse Matching pairs
    if '"type": "matching"' in line:
        # Example: "pairs": [{"left": "Қызыл", "right": "Red"}, ...]
        # We want: "pairs": [{"left": "Red", "right": "Қызыл"}, ...] 
        # Wait, user said "English person learning Kazakh, task is Kazakh, student does in English".
        # So for matching: Student sees Kazakh word, finds English match.
        # Current: {"left": "Қызыл", "right": "Red"}. Left is prompt, right is target.
        # This is already Kazakh -> English. I'll leave matching as is or ensure it's Kazakh -> English.
        pass

    # 2. Reverse Ordering tasks
    if '"type": "ordering"' in line:
        # If it has a 'correct' and 'prompt', and prompt is Kazakh, it's already reversed.
        # If it has 'correct' as Kazakh and 'prompt' is missing/English, we reverse it.
        # Logic: If 'correct' contains Kazakh (Cyrillic), we should probably swap it.
        if '"correct": "' in line and any(c in 'әіңғүұқөһӘІҢҒҮҰҚӨҺ' for c in line):
             # This is a very rough check. Let's be more specific.
             pass

    # Actually, a better way is to globally replace the instructions to Kazakh
    for eng, kaz in instruction_map.items():
        line = line.replace(eng, kaz)
    
    # Change any remaining generic instructions
    line = line.replace('"instruction": "Match', '"instruction": "Сәйкестендіріңіз: Match')
    line = line.replace('"instruction": "Translate', '"instruction": "Аударыңыз: Translate')

    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Instructions localized to Kazakh!")
