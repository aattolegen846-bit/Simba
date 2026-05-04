import os

path = '/Users/tolegenayat/SimbaAI/simpai-backend/app/services/content_service.py'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Manual correction for the first lesson to ensure it's high quality
corrections = {
    '{"prompt": "Сәлем! Қалың қалай?", "words": [\'Order\', \'the\', \'greeting\'], "correct": "Order the greeting"}':
    '{"prompt": "Сәлем! Қалың қалай?", "words": ["Hello", "How", "are", "you"], "correct": "Hello How are you"}',
    
    '{"prompt": "Жағдайыңыз қалай?", "words": [\'Ask\', "\'How", \'are\', "you\'"], "correct": "Ask \'How are you?\'"}':
    '{"prompt": "Жағдайыңыз қалай?", "words": ["How", "is", "your", "situation", "going"], "correct": "How is your situation"}',

    '{"prompt": "Көріскенше күн жақсы", "words": [\'Say\', "\'See", \'you\', "later\'"], "correct": "Say \'See you later\'"}':
    '{"prompt": "Көріскенше күн жақсы", "words": ["See", "you", "soon", "have", "a", "good", "day"], "correct": "See you soon have a good day"}',
    
    '{"prompt": "Танысқаныма қуаныштымын", "words": [\'Nice\', \'to\', \'meet\', \'you\'], "correct": "Nice to meet you"}':
    '{"prompt": "Танысқаныма қуаныштымын", "words": ["Nice", "to", "meet", "you", "pleasure"], "correct": "Nice to meet you"}'
}

for old, new in corrections.items():
    content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Manual quality fixes applied!")
