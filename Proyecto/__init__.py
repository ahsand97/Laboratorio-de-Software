#Archivo que indica que es un paquete de Flask
from flask import Flask
from config import Configuracion #Clase configuracion del archivo config.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Configuracion)

db = SQLAlchemy(app)
Migracion = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'


from Proyecto import rutas, modelos