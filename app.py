# inés de la cal perez
# Importamos Flask y otras dependencias necesarias
from flask import Flask
from models import db, User
from routes import main
from flask_login import LoginManager
from flask_migrate import Migrate

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Importamos la configurtacion del proyecto desde el archivo config.py
app.config.from_object('config.DevConfig')

# Configuramos Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"

# Definimos una funcion para cargar un usuario en Flask Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Inicializamos la base de datos
db.init_app(app)

# Creamos las tablas en la base de datos (Si no estan creadas)
with app.app_context():
    db.create_all()

# Registramos las rutas definidas en el archivo routes.py en la aplicacion
app.register_blueprint(main)

# Ejecutar el servidor solo si este archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
