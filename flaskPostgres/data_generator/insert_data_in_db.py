from dataclasses import dataclass
import random as rnd
import pickle
import json

import psycopg2
from psycopg2.extensions import connection as psycopg_connection
from RandomWordGenerator import RandomWord

from config import Config

# backend_connection: psycopg_connection = psycopg2.connect(
#     database=Config.database,
#     user='postgres',
#     password='VupsenPupsen228',
#     host=Config.host,
#     port=Config.port)

# Creating a random word object
rw = RandomWord(12,
                include_digits=True,
                special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                include_special_chars=True)

with open('names.txt', encoding="utf-8") as f:
    names = f.read().splitlines()

with open('middle_names.txt', encoding="utf-8") as f:
    middle_names = f.read().splitlines()

with open('last_names.txt', encoding="utf-8") as f:
    last_names = f.read().splitlines()

emails = [
    'mail.ru',
    'gmail.com',
    'ya.ru'
]

roles = [
    'client',
    'freelancer'
]

images = [
    '1-101-128.png',
    '1-102-128.png',
    '1-103-128.png',
    '1-107-128.png',
    '1-108-128.png',
    '1-126-128.png',
    'no_image.png'
]


@dataclass()
class Profile:
    '''
	first_name CHARACTER VARYING(50),
	middle_name CHARACTER VARYING(50),
	last_name CHARACTER VARYING(50),
	email CHARACTER VARYING(50),
	phone BIGINT,
	user_nickname CHARACTER VARYING(12),
	user_password CHARACTER VARYING(20),
	role_name CHARACTER VARYING(20),
	second_auth_req BOOLEAN DEFAULT FALSE,
	image_path TEXT DEFAULT 'no_image.jpg'
	'''

    first_name: str
    middle_name: str
    last_name: str
    email: str
    phone: int
    user_nickname: str
    user_password: str
    role_name: str
    second_auth_req: bool
    image_path: str

    def __str__(self):
        return ', '.join(self.__dict__.values())


from random_word import RandomWords

count = 500

random_words = RandomWords()
words_list = list()
for n in range(500):
    if n % (count // 100 * 10) == 0:
        print(f'{n}%')
    words_list.append(random_words.get_random_word())

usernames = list(set(words_list))
names_list = rnd.choices(names, k=count)
middle_names_list = rnd.choices(last_names, k=count)
last_names_list = rnd.choices(middle_names, k=count)
passwords = rw.getList(count)
image_paths = rnd.choices(images, k=count)

profiles: list[Profile] = list()
for n, nick in enumerate(usernames):
    profile = Profile(
        first_name=names_list[n],
        middle_name=middle_names_list[n],
        last_name=last_names_list[n],
        email=f'{nick}@{rnd.choice(emails)}',
        phone=int(f'89{rnd.randint(100000000, 809999999)}'),
        user_nickname=nick,
        user_password=passwords[n],
        role_name=roles[0] if n % 2 == 0 else roles[1],
        second_auth_req=False,
        image_path=image_paths[n]
    )

# result_str = '\n'.join((str(i) for i in profiles))

with open('accounts.json', 'w', encoding="utf-8") as f:
    json_dict = {'data': [o.__dict__ for o in profiles]}
    json.dump(json_dict, f)

print('done')
