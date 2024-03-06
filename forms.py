from wtforms import Form
from wtforms import StringField, SelectField, RadioField, EmailField, IntegerField, FloatField, SelectMultipleField,BooleanField
from wtforms import validators
from wtforms.validators import DataRequired


    
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
    
class Cliente(Form):
    id=IntegerField('id')
    nombre = StringField('nombre', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4, max=10, message='ingresa un nombre valido')
    ])
    telefono = StringField('telefono', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=10, max=10, message='ingresa un telefono valido')
    ])
    direccion = StringField('direccion', [
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=10, max=100, message='ingresa una direccion valida')
    ])
    
# class Pizzas(Form):
#     tamanio = RadioField('Tamaño', 
#                          choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')],
#                          validators=[DataRequired(message="Este campo es obligatorio.")])
#     ingredientes = SelectMultipleField('Ingredientes', 
#                          choices=[('jamon', 'Jamon $10'), ('pinia', 'Piña $10'), ('champi', 'Champiñones $10')],
#                          validators=[DataRequired(message="Este campo es obligatorio.")])
#     num_pizzas = IntegerField('NumeroPizzas', [
#         validators.DataRequired(message='el campo es requerido'),
#         validators.length(min=1, max=10, message='ingresa un numero valido')
#     ])

class Pizzas(Form):
    tamanio = RadioField('Tamaño', 
                         choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')],
                         validators=[DataRequired()])
    jamon = BooleanField('Jamón $10')
    pina = BooleanField('Piña $10')
    champinones = BooleanField('Champiñones $10')
    num_pizzas = IntegerField('Número de Pizzas', validators=[DataRequired()])