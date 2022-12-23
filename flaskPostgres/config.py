import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    port = '5431'
    host = 'localhost'
    database = 'postgres'
