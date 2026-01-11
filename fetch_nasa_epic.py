import os
import requests
from dotenv import load_dotenv
from helpers import download_image

load_dotenv()
NASA_API_KEY = os.getenv('NASA_API_KEY')


def fetch_nasa_epic(api_key, download_count=5):
    metadata_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    
    params = {'api_key': api_key}
    
    try:
        response = requests.get(metadata_url, params=params, timeout=10)
        response.raise_for_status()
    except Exception:
        params = {'api_key': 'DEMO_KEY'}
        try:
            response = requests.get(metadata_url, params=params, timeout=10)
            response.raise_for_status()
            api_key = 'DEMO_KEY'
        except Exception:
            return
    
    epic_metadata = response.json()

    for index, meta in enumerate(epic_metadata[:download_count], start=1):
        image_name = meta['image']
        date = meta['date'].split()[0].replace('-', '/')
        image_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{date}/png/{image_name}.png?api_key={api_key}"
        )
        filename = f"nasa_epic_{index}.png"
        filepath = os.path.join('images', 'nasa_epic', filename)
        
        try:
            download_image(image_url, filepath)
        except Exception:
            continue


if __name__ == "__main__":
    if not NASA_API_KEY:
        print("Ключ NASA_API_KEY не найден в .env файле.")
        fetch_nasa_epic('DEMO_KEY')
    else:
        fetch_nasa_epic(NASA_API_KEY)