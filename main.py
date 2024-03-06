from flask import Flask, render_template, request, flash, Response
import forms
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import g 
from config import DevelopmentConfig
from models import db
from models import *

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route("/index", methods = ["GET","POST"])
def index():
    alum_form = forms.UserForm2(request.form)
    if request.method == "POST":
        alum = Alumnos(nombre=alum_form.nombre.data,
                       apaterno=alum_form.apaterno.data,
                       email= alum_form.email.data)
        db.session.add(alum)
        db.session.commit()
        
        
    return render_template("index.html" , form=alum_form)

@app.route('/ABC_Completo', methods = ["GET","POST"])
def ABC_Completo():
    alum_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    return render_template('ABC_Completo.html', alumnos=alumno)

@app.route("/alumnos", methods = ["GET","POST"])
def alum():
    nom=''
    apa=''
    ama=''
    alum_form = forms.UserForm(request.form)
    if request.method == "POST" and alum_form.validate():
        nom = alum_form.nombre.data
        apa = alum_form.apaterno.data
        ama = alum_form.amaterno.data
        mensaje = 'Bienvenido {}'.format(nom)
        flash(mensaje)
        print("Nombre: {}".format(nom))
        print("ApellidoPa: {}".format(apa))
        print("ApellidoMa: {}".format(ama))
    
    return render_template("alumnos.html", form = alum_form, nombre = nom, apePa = apa, apeMa = ama)

@app.route('/empleados', methods=['GET', 'POST'])
def empleado():
    emp_form = forms.Empleado(request.form)
    if request.method == "POST":
        empleado = Empleados(nombre=emp_form.nombre.data,
                             correo=emp_form.correo.data,
                             telefono=emp_form.telefono.data,
                             direccion=emp_form.direccion.data,
                             sueldo=emp_form.sueldo.data)
        db.session.add(empleado)
        db.session.commit()
    return render_template("empleados.html" , form=emp_form)
 #-------------------------------------------------------------------------------------
@app.route('/listado_empleados', methods = ["GET","POST"])
def listado_empleado():
    
    empleado = Empleados.query.all()
    return render_template('listado_empleados.html', empleados=empleado)

@app.route('/eliminar',methods = ["GET","POST"])
def eliminar():
    emp_form = forms.Empleado(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        emp1 = db.session.query(Empleados).filter(Empleados.id==id).first()
        emp_form.id.data = request.args.get('id')
        emp_form.nombre.data = emp1.nombre
        emp_form.correo.data = emp1.correo
        emp_form.telefono.data = emp1.telefono
        emp_form.direccion.data = emp1.direccion
        emp_form.sueldo.data = emp1.sueldo
    elif request.method == 'POST':
        id = emp_form.id.data
        emp = Empleados.query.get(id)
        db.session.delete(emp)
        db.session.commit()
        return redirect('listado_empleados')
    return render_template('eliminar.html', form = emp_form)

@app.route('/modificar',methods = ["GET","POST"])
def modificar():
    emp_form = forms.Empleado(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        emp1 = db.session.query(Empleados).filter(Empleados.id==id).first()
        emp_form.id.data = request.args.get('id')
        emp_form.nombre.data = emp1.nombre
        emp_form.correo.data = emp1.correo
        emp_form.telefono.data = emp1.telefono
        emp_form.direccion.data = emp1.direccion
        emp_form.sueldo.data = emp1.sueldo
    elif request.method == 'POST':
        id = emp_form.id.data
        emp1 = db.session.query(Empleados).filter(Empleados.id==id).first()
        emp1.nombre = emp_form.nombre.data
        emp1.correo = emp_form.correo.data
        emp1.telefono = emp_form.telefono.data
        emp1.direccion = emp_form.direccion.data
        emp1.sueldo = emp_form.sueldo.data
        db.session.add(emp1)
        db.session.commit()
        return redirect('listado_empleados')
    return render_template('modificar.html', form = emp_form)

# PIZZAS----------------------------------------------------------------------------------------
@app.route('/pizzas', methods=['GET', 'POST'])
def cliente():
    cliente_form = forms.Cliente(request.form)
    pizza_form = forms.Pizzas(request.form)
    total = 0
    extra = 0
    numeroPizzas = 0
    precioVenta = 0
    consultaVista = 'SELECT * FROM vista_detalle_pizzas'
    if request.method == "POST" and cliente_form.validate() and pizza_form.validate():
        # Crear instancia de Cliente
        cliente = Cliente(nombre=cliente_form.nombre.data,
                          direccion=cliente_form.direccion.data,
                          telefono=cliente_form.telefono.data)
        db.session.add(cliente)

        # Recolectar ingredientes seleccionados
        ingredientes_seleccionados = []
        if pizza_form.jamon.data:
            ingredientes_seleccionados.append('Jamón')
            extra += 10
        if pizza_form.pina.data:
            ingredientes_seleccionados.append('Piña')
            extra += 10
        if pizza_form.champinones.data:
            ingredientes_seleccionados.append('Champiñones')
            extra += 10
        
        # Convertir la lista de ingredientes a una cadena de texto
        ingredientes_str = ', '.join(ingredientes_seleccionados)

        # Crear instancia de Pizza
        pizza = Pizza(tamanio=pizza_form.tamanio.data,
                      ingredientes=ingredientes_str,  # Usar la cadena de texto de ingredientes
                      nombre=cliente_form.nombre.data,
                      num_pizzas=pizza_form.num_pizzas.data)
        db.session.add(pizza)
        
        tamanioVenta = pizza_form.tamanio.data
        numeroPizzas = pizza_form.num_pizzas.data
        
        if tamanioVenta == "chica":
            precioVenta = 40
        elif tamanioVenta == "mediana":
            precioVenta = 80
        elif tamanioVenta == "grande":
            precioVenta = 120
            
        total = (precioVenta + extra) * numeroPizzas
        
        venta = Venta(nombre_cliente = cliente_form.nombre.data,
                      total = total)
        
        db.session.add(venta)
        
        detalles_pizza = db.session.execute(consultaVista).fetchall()

        db.session.commit()
    

    return render_template("pizzas.html", form=cliente_form, formPi=pizza_form, vistaPizzas = detalles_pizza)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()