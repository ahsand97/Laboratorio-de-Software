import os
basedirectorio = os.path.abspath(os.path.dirname(__file__))

class Configuracion(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedirectorio, 'DataBase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False