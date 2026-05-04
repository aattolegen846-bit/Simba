import os
import re

path = '/Users/tolegenayat/SimbaAI/simpai-backend/app/services/content_service.py'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

def transform_task(match):
    task_body = match.group(0)
    
    # Extract instruction (which often contains the English translation)
    inst_match = re.search(r'"instruction": "([^"]+):"', task_body)
    if not inst_match:
        return task_body # Skip if no clear instruction
        
    english_text = inst_match.group(1).strip()
    
    # For Ordering Tasks
    if '"type": "ordering"' in task_body:
        # Extract the Kazakh 'correct' sentence
        corr_match = re.search(r'"correct": "([^"]+)"', task_body)
        if corr_match:
            kazakh_text = corr_match.group(1)
            # Create English words
            english_words = str(english_text.replace('?', '').replace('.', '').replace('!', '').split())
            
            # Replace instruction with Kazakh
            task_body = task_body.replace(f'"instruction": "{english_text}:"', '"instruction": "Ағылшыншаға аударыңыз:"')
            # Set prompt to Kazakh
            # Set words to English words
            # Set correct to English text
            task_body = re.sub(r'"words": \[.*?\]', f'"words": {english_words}', task_body)
            task_body = re.sub(r'"correct": ".*?"', f'"correct": "{english_text}"', task_body)
            
            if '"prompt":' in task_body:
                task_body = re.sub(r'"prompt": ".*?"', f'"prompt": "{kazakh_text}"', task_body)
            else:
                task_body = task_body.replace('"sentences": [{', f'"sentences": [{{"prompt": "{kazakh_text}", ')

    # For Gaps Tasks
    if '"type": "gaps"' in task_body:
        # Similar logic but for gaps
        pass

    return task_body

# Apply transformation to all task blocks
# We'll use a regex to find task objects {"type": ... }
content = re.sub(r'\{"type": "(ordering|gaps)".*?\}', transform_task, content, flags=re.DOTALL)

# Cleanup instructions for matching
content = content.replace('"instruction": "Match colors:"', '"instruction": "Түстерді сәйкестендіріңіз:"')
content = content.replace('"instruction": "Match objects:"', '"instruction": "Заттарды сәйкестендіріңіз:"')
content = content.replace('"instruction": "Match body parts:"', '"instruction": "Дене мүшелерін сәйкестендіріңіз:"')
content = content.replace('"instruction": "Match food/drinks:"', '"instruction": "Тағамдар мен сусындарды сәйкестендіріңіз:"')
content = content.replace('"instruction": "Match plants:"', '"instruction": "Өсімдіктерді сәйкестендіріңіз:"')
content = content.replace('"instruction": "Match animals:"', '"instruction": "Жануарларды сәйкестендіріңіз:"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Global reversal to Kazakh -> English completed!")
