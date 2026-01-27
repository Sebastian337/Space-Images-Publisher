import os
import requests


def get_all_images(images_dir='images'):
    all_images = []
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                all_images.append(os.path.join(root, file))
    return all_images


def send_telegram_photo(bot_token, chat_id, image_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    with open(image_path, 'rb') as photo_file:
        photo_data = photo_file.read()
    
    files = {'photo': ('photo.jpg', photo_data)}
    data = {'chat_id': chat_id}
    
    response = requests.post(url, files=files, data=data, timeout=30)
    response.raise_for_status()