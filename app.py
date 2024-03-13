from config import config # Importamos configuraciones del módulo config
from src import init_app # Importamos la función init_app del módulo src
from src.Utils.Database import db


# Selecionamos la configuración de desarrollo del diccionario de configuraciones
configuration = config['development']

# Inicializamos la aplicacion con la configuración selecionada
app = init_app(configuration)

# Entramos al contexto de la aplicación de flask
with app.app_context():
    db.create_all() # Creamos todas las tablas en la base de datos


# Si este script se ejecuta directamente...
if __name__ == '__main__':
    app.run() # Ejecutamos la aplicación Flask
