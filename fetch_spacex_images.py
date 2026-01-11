import argparse
import os
import requests
from helpers import download_image


def fetch_spacex_launch(launch_id=None):
    if launch_id:
        url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    else:
        url = "https://api.spacexdata.com/v5/launches/latest"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    launch = response.json()

    image_urls = launch.get('links', {}).get('flickr', {}).get('original', [])
    if not image_urls:
        image_urls = launch.get('links', {}).get('flickr_images', [])

    if not image_urls:
        return

    for index, url in enumerate(image_urls, start=1):
        filename = f"spacex_{launch_id or 'latest'}_{index}.jpg"
        filepath = os.path.join('images', 'spacex', filename)
        download_image(url, filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Скачать фото запуска SpaceX.')
    parser.add_argument('--id', help='ID конкретного запуска')
    args = parser.parse_args()

    fetch_spacex_launch(args.id)