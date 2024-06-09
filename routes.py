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
            flash("Error en el login")
            return redirect(url_for("main.login"))
    return render_template("login.html", form=form)

# Ruta de registro
@main.route("/registro", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("Usuario ya existe")
            return redirect(url_for("main.login"))
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash("Usuario registrado con éxito")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)

# Ruta de cierre de sesión
@main.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.inicio"))

# Ruta privada del menú
@main.route("/menu")
@login_required
def menu():
    return render_template("menu.html")

# Ruta para ver el stock
@main.route("/stock")
@login_required
def view_stock():
    productos = Stock.query.all()
    return render_template("stock.html", productos=productos)

# Ruta para la transacción de salidas
@main.route("/transaccion_salidas")
@login_required
def transaccion_salidas():
    return render_template("transaccionSalidas.html")

# Ruta para procesar el pedido
@main.route("/procesar_pedido", methods=["POST"])
@login_required
def procesar_pedido():
    productos_seleccionados = {
        "platano": request.form.get("cantidad_platano", 0),
        "manzana": request.form.get("cantidad_manzana", 0),
        "pera": request.form.get("cantidad_pera", 0)
    }

    precio_total = 0
    lineas = []

    for nombre, cantidad in productos_seleccionados.items():
        if int(cantidad) > 0:
            producto = Stock.query.filter_by(nombre=nombre).first()
            if producto and producto.cantidad >= int(cantidad):
                producto.cantidad -= int(cantidad)
                db.session.commit()
                
                precio_por_unidad = producto.precio
                precio_total += precio_por_unidad * int(cantidad)
                
                linea = LineasFsaSalidas(
                    cantidad_producto=int(cantidad),
                    fk_producto=producto.id,
                    precio_por_unidad=precio_por_unidad
                )
                lineas.append(linea)
            else:
                flash(f"No hay suficiente stock disponible para {nombre}.")
                return redirect(url_for("main.view_stock"))

    zona_horaria = pytz.timezone('Europe/Madrid')
    fecha_actual = datetime.now(zona_horaria)

    nueva_salida = FsaSalidas(
        user_id=current_user.id,
        precio_total=precio_total,
        fecha=fecha_actual
    )
    db.session.add(nueva_salida)
    db.session.commit()

    for linea in lineas:
        linea.fk_salida = nueva_salida.id
        db.session.add(linea)
    db.session.commit()

    flash("Pedido procesado correctamente.")
    return redirect(url_for("main.view_stock"))

# Ruta para ver las FSA Salidas
@main.route("/fsa_salidas")
@login_required
def view_fsa_salidas():
    salidas = FsaSalidas.query.all()
    return render_template("FSA_salidas.html", salidas=salidas)

# Ruta para ver las líneas de una FSA Salida
@main.route("/lineas_fsa_salidas/<int:salida_id>")
@login_required
def view_lineas_fsa_salidas(salida_id):
    lineas = LineasFsaSalidas.query.filter_by(fk_salida=salida_id).all()
    return render_template("lineasFSA_salidas.html", lineas=lineas)

# Ruta para la transacción de entradas
@main.route("/transaccion_entradas")
@login_required
def transaccion_entradas():
    return render_template("transaccionEntradas.html")

# Ruta para procesar una entrada
@main.route("/procesar_entrada", methods=["POST"])
@login_required
def procesar_entrada():
    productos_seleccionados = {
        "platano": request.form.get("cantidad_platano", 0),
        "manzana": request.form.get("cantidad_manzana", 0),
        "pera": request.form.get("cantidad_pera", 0)
    }

    precio_total = 0
    lineas = []

    for nombre, cantidad in productos_seleccionados.items():
        if int(cantidad) > 0:
            producto = Stock.query.filter_by(nombre=nombre).first()
            if producto:
                producto.cantidad += int(cantidad)
                db.session.commit()
                
                precio_por_unidad = producto.precio
                precio_total += precio_por_unidad * int(cantidad)
                
                linea = LineasFsaEntradas(
                    cantidad_producto=int(cantidad),
                    fk_producto=producto.id,
                    precio_por_unidad=precio_por_unidad
                )
                lineas.append(linea)

    zona_horaria = pytz.timezone('Europe/Madrid')
    fecha_actual = datetime.now(zona_horaria)

    nueva_entrada = FsaEntradas(
        user_id=current_user.id,
        precio_total=precio_total,
        fecha=fecha_actual
    )
    db.session.add(nueva_entrada)
    db.session.commit()

    for linea in lineas:
        linea.fk_entrada = nueva_entrada.id
        db.session.add(linea)
    db.session.commit()

    flash("Entrada procesada correctamente.")
    return redirect(url_for("main.view_stock"))

# Ruta para ver las FSA Entradas
@main.route("/fsa_entradas")
@login_required
def view_fsa_entradas():
    entradas = FsaEntradas.query.all()
    return render_template("FSA_entradas.html", entradas=entradas)

# Ruta para ver las líneas de una FSA Entrada
@main.route("/lineas_fsa_entradas/<int:entrada_id>")
@login_required
def view_lineas_fsa_entradas(entrada_id):
    lineas = LineasFsaEntradas.query.filter_by(fk_entrada=entrada_id).all()
    return render_template("lineasFSA_entradas.html", lineas=lineas)
