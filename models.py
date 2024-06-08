# inés de la cal perez
# Importamos las bibliotecas necesarias
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Creamos una instancia de SQLAlchemy para interactuar con la base de datos
db = SQLAlchemy()  # Instancia de SQLAlchemy pa' la base de datos

# Definimos la clase User, que representa a un usuario en la base de datos
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # ID unico pa' cada usuario
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario, tiene que ser unico
    password = db.Column(db.String(80), nullable=False)  # Contraseña del usuario
    fsa_salidas = db.relationship('FsaSalidas', backref='user', lazy=True)  # Relacion con las salidas de FSA
    fsa_entradas = db.relationship('FsaEntradas', backref='user', lazy=True)  # Relacion con las entradas de FSA

# Definimos la clase Stock, que representa el inventario
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID unico pa' cada producto
    nombre = db.Column(db.String(80), unique=True, nullable=False)  # Nombre del producto, tiene que ser unico
    cantidad = db.Column(db.Integer, nullable=False)  # Cantidad disponible del producto
    precio = db.Column(db.Float, nullable=False, default=1.0)  # Precio del producto, por defecto es 1.0
    lineas_salidas = db.relationship('LineasFsaSalidas', backref='producto', lazy=True)  # Relacion con las lineas de salidas
    lineas_entradas = db.relationship('LineasFsaEntradas', backref='producto', lazy=True)  # Relacion con las lineas de entradas

# Definimos la clase FsaSalidas, que representa las salidas de productos
class FsaSalidas(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID unico pra cada salida
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID del usuario que hace la salida
    precio_total = db.Column(db.Float, nullable=False)  # Precio total de la salida
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Fecha de la salida, por defecto la fecha actual
    lineas = db.relationship('LineasFsaSalidas', backref='salida', lazy=True)  # Relacion con las lineas de salidas

# Definimos la clase LineasFsaSalidas, que representa los detalles de cada salida
class LineasFsaSalidas(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID unico pa' cada linea de salida
    cantidad_producto = db.Column(db.Integer, nullable=False, default=0)  # Cantidad de producto en la linea de salida
    fk_producto = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)  # ID del producto
    fk_salida = db.Column(db.Integer, db.ForeignKey('fsa_salidas.id'), nullable=False)  # ID de la salida
    precio_por_unidad = db.Column(db.Float, nullable=False)  # Precio por unidad del producto

# Definimos la clase FsaEntradas, que representa las entradas de productos
class FsaEntradas(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID unico pa' cada entrada
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID del usuario que hace la entrada
    precio_total = db.Column(db.Float, nullable=False)  # Precio total de la entrada
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Fecha de la entrada, por defecto la fecha actual
    lineas = db.relationship('LineasFsaEntradas', backref='entrada', lazy=True)  # Relacion con las lineas de entradas

# Definimos la clase LineasFsaEntradas, que representa los detalles de cada entrada
class LineasFsaEntradas(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID unico pa' cada linea de entrada
    cantidad_producto = db.Column(db.Integer, nullable=False, default=0)  # Cantidad de producto en la linea de entrada
    fk_producto = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)  # ID del producto
    fk_entrada = db.Column(db.Integer, db.ForeignKey('fsa_entradas.id'), nullable=False)  # ID de la entrada
    precio_por_unidad = db.Column(db.Float, nullable=False)  # Precio por unidad del producto
