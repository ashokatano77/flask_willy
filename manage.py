# inés de la cal perez
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db  # Importa tu aplicación Flask y la instancia de SQLAlchemy

# Crea una instancia de la aplicación Flask
app = create_app()

# Crea una instancia de Migrate y asóciala con tu aplicación Flask y tu instancia de SQLAlchemy
migrate = Migrate(app, db)

# Crea un objeto Manager para gestionar los comandos personalizados
manager = Manager(app)

# Agrega el comando 'db' para gestionar las migraciones, aunque no las he implementado
manager.add_command('db', Migrate