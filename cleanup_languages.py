import os
import re

path = '/Users/tolegenayat/SimbaAI/simpai-backend/app/services/content_service.py'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Pattern 1: Lesson titles like ("Title (Translation)", ...
# We want to keep only the English Title part.
content = re.sub(r'\("([^(\n]+)\s\([^)]+\)",', r'("\1",', content)

# Pattern 2: Ensure any specific instructions that might be in other languages (if any) are English.
# Based on grep, most instructions like "Match colors:", "The grass is green:" are already English.
# But let's check for any explicit Kazakh/Russian in instructions.

# Just in case, replace common module/lesson title translations if the regex above missed any
translations_to_remove = [
    " (Сәлемдесу)",
    " (Отбасы)",
    " (Сандар)",
    " (Түстер)",
    " (Күнделікті заттар)",
    " (Дене мүшелері)",
    " (Тағамдар мен сусындар)",
    " (Жемістер мен көкөністер)",
    " (Жануарлар)",
    " (Апта күндері)",
    " (Айлар мен мезгілдер)",
    " (Уақыт)",
    " (Ауа райы)",
    " (Үйім)",
    " (Асханада)",
    " (Киім-кешек)",
    " (Көлік)",
    " (Қаладағы орындар)"
]

for t in translations_to_remove:
    content = content.replace(t, "")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleanup done!")
