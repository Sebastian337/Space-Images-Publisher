import random
import time
from dotenv import load_dotenv
import os
from telegram_tools import get_all_images, send_telegram_photo


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
            
            try:
                send_telegram_photo(bot_token, chat_id, image_path)
                print("Успешно отправлено")
            except (requests.exceptions.Timeout,
                    requests.exceptions.HTTPError,
                    requests.exceptions.ConnectionError) as e:
                print(f"Ошибка отправки: {e}")
            
            print(f"Ожидание {delay_hours} часов до следующей публикации...")
            time.sleep(delay_seconds)


def main():
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
