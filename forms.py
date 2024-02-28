from wtforms import Form
from wtforms import StringField, SelectField, RadioField, EmailField, IntegerField, FloatField
from wtforms import validators

    
class Empleado(Form):
    id=IntegerField('id')
    nombre = StringField('nombre', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4, max=10, message='ingresa un nombre valido')
    ])
    correo = EmailField('correo',[
        validators.Email(message='Ingrese un correo válido')
    ])
    telefono = StringField('telefono', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=10, max=10, message='ingresa un nombre valido')
    ])
    direccion = StringField('direccion', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=10, max=100, message='ingresa un nombre valido')
    ])
    sueldo = StringField('sueldo', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=10, max=100, message='ingresa un nombre valido')
    ])