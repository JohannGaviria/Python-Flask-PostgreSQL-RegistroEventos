from dotenv import load_dotenv
from os import environ


# Cargar las variables de entorno desde el archivo .env en el directorio actual
load_dotenv()


# Definir una clase base para la configuración
class Config():
    SECRET_KEY = environ.get('SECRET_KEY') # Obtener la clave secreta desde las variables de entorno


# Definir una clase para la configuración de desarrollo que hereda de la clase Config
class DevelopmentConfig(Config):
    DEBUG = True # Activar el modo de depuración


# Crear un diccionario que asocie nombres de entornos con las clases de configuración correspondientes
config = {
    'development': DevelopmentConfig
}
