import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_ADDRESS = 'localhost:5431/postgres'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:VupsenPupsen228@' + SQLALCHEMY_DATABASE_ADDRESS
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    port = '5431'
    host = 'localhost'
    database = 'postgres'
