# inés de la cal perez
# Config.py
# Importamos la clase Config de Flask
from flask import Config
from flask_migrate import Migrate

# Creamos una clase base de configuración llamada Config
class Config(object):
    # Definimos una clave secreta para la aplicación (puede ser cualquier cadena aleatoria)
    SECRET_KEY = 'una_llave_aleatoria'

# Creamos una subclase llamada DevConfig que hereda de la clase Config
class DevConfig(Config):
    # Configuramos la URI de la base de datos para la configuración de desarrollo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'



#notas tomadas en clase ------>
#fichero de configuracion, tiene que haber: clave secreta para los formularios y la ruta hacia la base de datos
    #la base de datos es sqlite, se maneja desde el visual no desde el worbrench