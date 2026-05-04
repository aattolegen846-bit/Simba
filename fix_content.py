import os

path = '/Users/tolegenayat/SimbaAI/simpai-backend/app/services/content_service.py'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

garbage = """әрігер"}]},
                {"type": "matching", "instruction": "Relatives:", "pairs": [{"left": "Туысқан", "right": "Relative"}, {"left": "Жиен", "right": "Nephew/Niece"}]},
                {"type": "ordering", "instruction": "We are a big family:", "sentences": [{"words": ["Біз", "үлкен", "отбасымыз"], "correct": "Біз үлкен отбасымыз"}]}
            ]),"""

if garbage in content:
    print("Found garbage, removing...")
    content = content.replace(garbage, "")
else:
    print("Garbage not found exactly. Trying partial match...")
    # Maybe indentation or line endings differ
    import re
    content = re.sub(r'әрігер"}\]},\s+{"type": "matching", "instruction": "Relatives:".*?\]\)\),', '', content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fix attempt done.")
