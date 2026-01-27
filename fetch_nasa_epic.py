import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from helpers import download_image


def format_date_for_url(date_str):
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime('%Y/%m/%d')
    except (ValueError, TypeError):
        return date_str.split()[0].replace('-', '/')


def fetch_epic_metadata(api_key):
    metadata_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': api_key}
    
    try:
        response = requests.get(metadata_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError) as e:
        raise ConnectionError(f"Не удалось получить метаданные EPIC: {e}")


def build_epic_image_url(image_name, date_str, api_key):
    date_path = format_date_for_url(date_str)
    image_url = (
        f"https://api.nasa.gov/EPIC/archive/natural/"
        f"{date_path}/png/{image_name}.png"
    )
    download_params = {'api_key': api_key}
    return image_url, download_params


def download_epic_images(api_key, download_count=5):
    try:
        epic_metadata = fetch_epic_metadata(api_key)
    except (requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError) as e:
        print(f"Пробуем использовать DEMO_KEY из-за ошибки: {e}")
        epic_metadata = fetch_epic_metadata('DEMO_KEY')
        api_key = 'DEMO_KEY'
    
    downloaded = 0
    
    for index, meta in enumerate(epic_metadata[:download_count], start=1):
        image_name = meta.get('image')
        date_str = meta.get('date')
        
        if not image_name or not date_str:
            continue
        
        image_url, download_params = build_epic_image_url(image_name, date_str, api_key)
        filename = f"nasa_epic_{index}.png"
        filepath = os.path.join('images', 'nasa_epic', filename)
        
        try:
            download_image(image_url, filepath, params=download_params)
            downloaded += 1
        except (requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError) as e:
            print(f"Ошибка загрузки {image_name}: {e}")
            continue
    
    return downloaded


def fetch_nasa_epic(api_key, download_count=5):
    downloaded = download_epic_images(api_key, download_count)
    return downloaded


def main():
    load_dotenv()
    
    nasa_api_key = os.getenv('NASA_API_KEY')
    
    api_key_to_use = nasa_api_key if nasa_api_key else 'DEMO_KEY'
    
    try:
        downloaded = fetch_nasa_epic(api_key_to_use)
        print(f"Успешно скачано {downloaded} фото EPIC")
    except (ValueError, ConnectionError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
