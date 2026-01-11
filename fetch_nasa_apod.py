import os
import requests
from dotenv import load_dotenv
from helpers import download_image, get_file_extension_from_url

load_dotenv()
NASA_API_KEY = os.getenv('NASA_API_KEY')


def fetch_nasa_apod(api_key, count=30):
    url = 'https://api.nasa.gov/planetary/apod'
    
    params = {'api_key': api_key, 'count': count}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except Exception:
        params = {'api_key': 'DEMO_KEY', 'count': min(5, count)}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except Exception:
            return
    
    apod_items = response.json()

    for index, item in enumerate(apod_items, start=1):
        if item.get('media_type') != 'image':
            continue

        image_url = item.get('url')
        if not image_url:
            continue

        ext = get_file_extension_from_url(image_url)
        if not ext:
            ext = '.jpg'

        filename = f"nasa_apod_{index}{ext}"
        filepath = os.path.join('images', 'nasa_apod', filename)
        
        try:
            download_image(image_url, filepath)
        except Exception:
            continue


if __name__ == "__main__":
    if not NASA_API_KEY:
        print("Ключ NASA_API_KEY не найден в .env файле.")
        fetch_nasa_apod('DEMO_KEY', count=5)
    else:
        fetch_nasa_apod(NASA_API_KEY)