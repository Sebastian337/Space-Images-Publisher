import os
import random
import time
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
        return True
    except requests.exceptions.RequestException:
        return False


def publish_photos_loop(bot_token, chat_id, delay_hours):
    delay_seconds = delay_hours * 3600
    
    while True:
        all_images = get_all_images()
        
        if not all_images:
            print(f"В папке images нет изображений. Ожидание {delay_hours} часов...")
            time.sleep(delay_seconds)
            continue
        
        random.shuffle(all_images)
        
        for image_path in all_images:
            print(f"Публикую: {os.path.basename(image_path)}")
            
            if send_telegram_photo(bot_token, chat_id, image_path):
                print("Успешно отправлено")
            else:
                print("Ошибка отправки")
            
            print(f"Ожидание {delay_hours} часов до следующей публикации...")
            time.sleep(delay_seconds)


def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    bot_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    delay_hours = int(os.getenv('TG_DELAY_HOURS', 4))
    
    if not bot_token:
        raise ValueError("TG_BOT_TOKEN не найден в .env файле")
    if not chat_id:
        raise ValueError("TG_CHAT_ID не найден в .env файле")
    
    print(f"Запуск автоматической публикации с интервалом {delay_hours} часов")
    print("Для остановки нажмите Ctrl+C")
    
    try:
        publish_photos_loop(bot_token, chat_id, delay_hours)
    except KeyboardInterrupt:
        print("\nПубликация остановлена")


if __name__ == "__main__":
    main()
