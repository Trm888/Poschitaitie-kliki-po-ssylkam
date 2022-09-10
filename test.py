import argparse


parser = argparse.ArgumentParser(
    description='Описание что делает программа'
)
parser.add_argument('URL', help='URL адрес')
# parser.add_argument('-l', '--last_name', help='Ваша фамилия')
args = parser.parse_args()
print(args.URL)
# print(args.last_name)