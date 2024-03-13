from wtforms import Form
from wtforms import StringField, SelectField, RadioField, EmailField, IntegerField, SelectMultipleField, DateField
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

class ClienteForm(Form):
    id = IntegerField('id')
    nombre = StringField('nombre', [
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4, max=50, message='Ingresa un nombre válido.')
    ])
    direccion = StringField('direccion', [
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4, max=50, message='Ingresa una dirección válida.')
    ])
    telefono = StringField('telefono', [
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=1, max=10, message='Ingresa un teléfono válido.')
    ])

class PizzaForm(Form):
    id = IntegerField('id')
    tamano = RadioField('tamano', choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')], validators=[validators.DataRequired(message='El campo es requerido.')])
    ingredientes = SelectField('ingredientes', choices=[('jamon', 'Jamon $10'), ('piña', 'Piña $10'), ('champiñones', 'Champiñones $10')], validators=[validators.DataRequired(message='El campo es requerido.')])
    no_pizzas = IntegerField('no_pizzas', [
        validators.DataRequired(message='El campo es requerido.'),
        validators.number_range(min=1, max=7, message='Ingresa una cantidad válida.')
    ])

class PedidoForm(Form):
    id = IntegerField('id')
    nombre = StringField('nombre', [
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4, max=50, message='Ingresa un nombre válido.')
    ])
    direccion = StringField('direccion', [
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=4, max=50, message='Ingresa una dirección válida.')
    ])
    telefono = StringField('telefono', [
        validators.DataRequired(message='El campo es requerido.'),
        validators.length(min=1, max=10, message='Ingresa un teléfono válido.')
    ])
    tamano = RadioField('tamano', choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')], validators=[validators.DataRequired(message='El campo es requerido.')])
    ingredientes = SelectMultipleField('ingredientes', choices=[('jamon', 'Jamon $10'), ('piña', 'Piña $10'), ('champiñones', 'Champiñones $10')], validators=[validators.DataRequired(message='El campo es requerido.')])
    no_pizzas = IntegerField('no_pizzas', [
        validators.DataRequired(message='El campo es requerido.'),
        validators.number_range(min=1, message='Ingresa una cantidad válida.')
    ])
    fechaCompra = DateField('fechaCompra', format='%Y-%m-%d', validators=[validators.DataRequired(message='El campo es requerido.')])