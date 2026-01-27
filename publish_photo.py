import random
from dotenv import load_dotenv
import os
from telegram_tools import get_all_images, send_telegram_photo


def main():
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
        send_telegram_photo(bot_token, chat_id, random_image)
        print("Фото успешно отправлено в Telegram канал")
    except (ValueError, FileNotFoundError, ConnectionError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
