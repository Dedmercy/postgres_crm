from dataclasses import dataclass
import random as rnd
import pickle
import json

import psycopg2
from psycopg2.extensions import connection as psycopg_connection
from RandomWordGenerator import RandomWord
from random_word import RandomWords

from config import Config

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

    @classmethod
    def parse_from_json(cls, jsons_list: list):
        profiles = []
        for p in jsons_list:
            profile = Profile(**p)
            profiles.append(profile)
        return profiles

    def __str__(self):
        return ', '.join(self.__dict__.values())


def generate_users(count):
    random_words = RandomWords()
    words_list = list()
    for n in range(count):
        if n % (count // 10) if count // 10 != 0 else 1 == 0:
            print(f'generate users: {round(n / count * 100)}%')
        words_list.append(random_words.get_random_word())

    usernames = [n[:12] for n in set(words_list)]
    names_list = rnd.choices(names, k=count)
    middle_names_list = rnd.choices(middle_names, k=count)
    last_names_list = rnd.choices(last_names, k=count)
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
        profiles.append(profile)

    # result_str = '\n'.join((str(i) for i in profiles))

    with open('accounts.json', 'w', encoding="utf-8") as f:
        users = [o.__dict__ for o in profiles]
        json.dump(users, f)

    print(f'generate users done, count users= {len(profiles)}')
    return profiles


def query_executor(connection, query: str, params: tuple):
    result = None

    with connection.cursor() as cursor:
        connection.autocommit = True
        cursor.execute(query, params)
        if cursor.pgresult_ptr is not None:
            result = cursor.fetchall()

        return result


if __name__ == '__main__':
    flag_from_disk = True

    connection: psycopg_connection = psycopg2.connect(
        database=Config.database,
        user='postgres',
        password='VupsenPupsen228',
        host=Config.host,
        port=Config.port)

    if flag_from_disk:
        with open('accounts.json', 'r', encoding='utf-8') as f:
            accounts = json.load(f)

        users = Profile.parse_from_json(accounts)
    else:
        count_users = 1000

        users = generate_users(count_users)

    query = f'''
        CALL create_user(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''

    print('processing')
    count = len(users)
    for n, u in enumerate(users):
        if n % (count // 10) if count // 10 != 0 else 1 == 0:
            print(f'generate users: {round(n / count * 100)}%')
        params = (u.first_name,
                  u.middle_name,
                  u.last_name,
                  u.email,
                  u.phone,
                  u.user_nickname,
                  u.user_password,
                  u.role_name,
                  u.second_auth_req,
                  u.image_path)
        query_executor(connection, query, params)
    print(f'inserting users done')
