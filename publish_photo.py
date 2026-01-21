import os
import random
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
    
    try:
        response = requests.post(url, files=files, data=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError) as e:
        raise ConnectionError(f"Ошибка отправки фото в Telegram: {e}")


def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    bot_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    if not bot_token:
        raise ValueError("TG_BOT_TOKEN не найден в .env файле")
    if not chat_id:
        raise ValueError("TG_CHAT_ID не найден в .env файле")
    
    all_images = get_all_images()
    
    if not all_images:
        raise FileNotFoundError(f"No images found in images directory")
    
    random_image = random.choice(all_images)
    print(f"Публикую: {random_image}")
    
    try:
        result = send_telegram_photo(bot_token, chat_id, random_image)
        print("Фото успешно отправлено в Telegram канал")
    except (ValueError, FileNotFoundError, ConnectionError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
