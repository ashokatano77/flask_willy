# inés de la cal perez
# Importamos las clases necesarias de Flask-WTF y WTForms
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from flask_migrate import Migrate

# Definimos la clase LoginForm que hereda de FlaskForm
class LoginForm(FlaskForm):
    # Creamos el campo "username" para el nombre de usuario
    username = StringField("Username", [validators.Length(min=4, max=25)])
    
    # Creamos el campo "password" para la contraseña
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=15)])

# Definimos la clase RegisterForm que hereda de FlaskForm
class RegisterForm(FlaskForm):
    # Creamos el campo "username" para el nombre de usuario
    username = StringField("Username", [validators.Length(min=4, max=25)])
    
    # Creamos el campo "password" para la contraseña
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=15)])
    
    # Creamos el campo "confirm" para confirmar la contraseña
    confirm = PasswordField("Repeat password", [validators.EqualTo('password', message="Las contraseñas deben ser iguales")])
#añadir ventas y pedidos


 #aqui tenemos los formularios, el de login y el de registro
 # todo:los formularios de factu