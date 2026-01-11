import os
import random
from dotenv import load_dotenv
import requests

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

images_dir = 'images'
all_images = []

for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            all_images.append(os.path.join(root, file))

if not all_images:
    raise FileNotFoundError(f"No images found in {images_dir}")

random_image = random.choice(all_images)

url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

with open(random_image, 'rb') as photo:
    files = {'photo': photo}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()