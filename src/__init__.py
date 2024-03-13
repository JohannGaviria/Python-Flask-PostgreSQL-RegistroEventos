from flask import Flask
from .Routes import Index
from .Utils.Database import db
from dotenv import load_dotenv
from os import environ


# Cargamos las variables de entorno desde el archivo .env
load_dotenv()


# Inicializamos la aplicación flask
app = Flask(__name__)


# Función para inicializar la aplicación con la configuración proporcionada 
def init_app(config):
    app.config.from_object(config) # Configuramos la aplicación con el objecto de configuración

    # Configuracion de conexión a la base de datos de postgreSQL usando variables de entorno
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@{environ.get('DB_HOST')}/{environ.get('DB_DATABASE')}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactivamos el seguimiento de modificaciones de SQLAlchemy

    db.init_app(app) # Inicializamos la base de datos con la aplicación

    # Registramos todas las rutas
    app.register_blueprint(Index.main, url_prefix='/')

    return app # Retonarmos la aplicación inicializada
