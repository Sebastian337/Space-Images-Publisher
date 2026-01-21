import os
import requests
from urllib.parse import urlparse, unquote


def download_image(url, filepath, params=None):
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ошибка загрузки изображения {url}: {e}")
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_file_extension_from_url(url):
    parsed_url = urlparse(url)
    file_path = unquote(parsed_url.path)
    file_name = os.path.split(file_path)[1]
    file_extension = os.path.splitext(file_name)[1]
    return file_extension
