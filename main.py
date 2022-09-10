import requests

from urllib.parse import urlparse

from environs import Env

import argparse

parser = argparse.ArgumentParser(
    description=''
)

parser.add_argument('URL', help='URL адрес')
args = parser.parse_args()

env = Env()
env.read_env()


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten',
                             json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, url):
    url_parts = urlparse(url)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/' \
              f'{url_parts.netloc}{url_parts.path}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, url):
    url_parts = urlparse(url)
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/' \
              f'{url_parts.netloc}{url_parts.path}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)
    return response.ok


def main():
    url = args.URL
    token = env.str("BITLY_TOKEN")
    if is_bitlink(token, url):
        print(count_clicks(token, url))
    else:
        print(shorten_link(token, url))


if __name__ == '__main__':
    main()
