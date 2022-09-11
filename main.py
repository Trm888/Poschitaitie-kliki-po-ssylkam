import requests

from urllib.parse import urlparse

from environs import Env

import argparse


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
    env = Env()
    env.read_env()
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('url', help='URL адрес')
    args = parser.parse_args()
    token = env.str("BITLY_TOKEN")
    if is_bitlink(token, args.url):
        print(count_clicks(token, args.url))
    else:
        print(shorten_link(token, args.url))


if __name__ == '__main__':
    main()
