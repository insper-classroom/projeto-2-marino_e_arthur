import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://usuario:senha@host/nome_banco')
    SQLALCHEMY_TRACK_MODIFICATIONS = False