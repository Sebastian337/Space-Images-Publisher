import os
import requests
from dotenv import load_dotenv
from helpers import download_image, get_file_extension_from_url


def fetch_nasa_apod(api_key, count=30):
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key, 'count': count}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
    except (requests.exceptions.Timeout, 
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError) as e:
        raise ConnectionError(f"Не удалось получить данные от NASA APOD API: {e}")
    
    apod_items = response.json()
    downloaded = 0

    for index, item in enumerate(apod_items, start=1):
        if not isinstance(item, dict) or item.get('media_type') != 'image':
            continue

        image_url = item.get('url')
        if not image_url:
            continue

        ext = get_file_extension_from_url(image_url) or '.jpg'
        filename = f"nasa_apod_{index}{ext}"
        filepath = os.path.join('images', 'nasa_apod', filename)
        
        try:
            download_image(image_url, filepath)
            downloaded += 1
        except (requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError) as e:
            print(f"Ошибка загрузки {image_url}: {e}")
            continue
    
    return downloaded


def main():
    load_dotenv()
    
    nasa_api_key = os.getenv('NASA_API_KEY')
    
    if not nasa_api_key:
        print("Ключ NASA_API_KEY не найден в .env файле.")
        print("Используйте DEMO_KEY для тестирования.")
        nasa_api_key = 'DEMO_KEY'
    
    try:
        count = 5 if nasa_api_key == 'DEMO_KEY' else 30
        downloaded = fetch_nasa_apod(nasa_api_key, count)
        print(f"Успешно скачано {downloaded} фото APOD")
    except (ValueError, ConnectionError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()


