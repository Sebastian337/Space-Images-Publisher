import argparse
import os
import requests
from helpers import download_image


def fetch_spacex_launch(launch_id='latest'):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к SpaceX API: {e}")
        return

    launch = response.json()

    image_urls = launch.get('links', {}).get('flickr', {}).get('original', [])
    if not image_urls:
        image_urls = launch.get('links', {}).get('flickr_images', [])

    if not image_urls:
        print("Для данного запуска не найдено фотографий.")
        return

    for index, url in enumerate(image_urls, start=1):
        filename = f"spacex_{launch_id}_{index}.jpg"
        filepath = os.path.join('images', 'spacex', filename)
        try:
            download_image(url, filepath)
            print(f"Скачано: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке {url}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Скачать фото запуска SpaceX.')
    parser.add_argument(
        '--id', 
        default='latest',
        help='ID конкретного запуска (по умолчанию: последний)'
    )
    args = parser.parse_args()
    fetch_spacex_launch(args.id)


if __name__ == "__main__":
    main()
