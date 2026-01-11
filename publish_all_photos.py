import os
import random
import time
from dotenv import load_dotenv
import requests

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
delay_hours = int(os.getenv('DELAY_HOURS', 4))
delay_seconds = delay_hours * 3600

images_dir = 'images'

while True:
    all_images = []
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                all_images.append(os.path.join(root, file))
    
    if not all_images:
        time.sleep(delay_seconds)
        continue
    
    random.shuffle(all_images)
    
    for image_path in all_images:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': chat_id}
            
            try:
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
            except Exception:
                continue
        
        time.sleep(delay_seconds)