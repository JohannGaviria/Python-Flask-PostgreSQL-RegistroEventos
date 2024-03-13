from flask import Flask
from .Routes.Users import CreateUser, GetUser, DeleteUser, UpdateUser
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

    app.config['WTF_CSRF_ENABLED'] = False # Desactivamos la proteción CRSF para simplificar la prueba de la API

    # Registramos todas las rutas
    app.register_blueprint(CreateUser.main, url_prefix='/')
    app.register_blueprint(GetUser.main, url_prefix='/')
    app.register_blueprint(DeleteUser.main, url_prefix='/')
    app.register_blueprint(UpdateUser.main, url_prefix='/')

    return app # Retonarmos la aplicación inicializada
