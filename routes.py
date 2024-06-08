# inés de la cal perez
from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from forms import LoginForm, RegisterForm
from models import User, Stock, FsaSalidas, LineasFsaSalidas, FsaEntradas, LineasFsaEntradas, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

# Creamos una instancia de Blueprint llamada 'main'
main = Blueprint('main', __name__)

# Ruta principal
@main.route("/")
def inicio():
    return render_template("index.html")

# Ruta de inicio de sesión
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.menu"))
        else:
            flash("Error en el l