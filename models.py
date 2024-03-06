from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    amaterno = db.Column(db.String(50))
    email = db.Column(db.String(50))
    create_date = db.Column(db.DateTime,default=datetime.datetime.now)
    
class Empleados(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    telefono = db.Column(db.String(10))
    direccion = db.Column(db.String(50))
    sueldo = db.Column(db.String(50))
    
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(10))
    create_date = db.Column(db.DateTime,default=datetime.datetime.now)
    
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tamanio = db.Column(db.String(50))
    ingredientes = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    num_pizzas = db.Column(db.String(50))

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(50))
    total = db.Column(db.Float(10))
