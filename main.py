from flask import Flask, render_template, request, redirect, flash, session
from flask_wtf.csrf import CSRFProtect
import forms
from config import DevelopmentConfig
from datetime import datetime
from models import db, Empleados, Pedido, Venta
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
crsf = CSRFProtect()
pedidos = []

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# @app.route("/alumnos", methods = ["GET","POST"])
# def alum():
#     nom=''
#     apa=''
#     ama=''
#     alum_form = forms.UserForm(request.form)
#     if request.method == "POST" and alum_form.validate():
#         nom = alum_form.nombre.data
#         apa = alum_form.apaterno.data
#         ama = alum_form.amaterno.data
#         mensaje = 'Bienvenido {}'.format(nom)
#         flash(mensaje)
#         print("Nombre: {}".format(nom))
#         print("ApellidoPa: {}".format(apa))
#         print("ApellidoMa: {}".format(ama))
    
#     return render_template("alumnos.html", form = alum_form, nombre = nom, apePa = apa, apeMa = ama)

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

@app.route("/pedidos", methods=["GET", "POST"])
def agregar_pedido():
    if 'nombre' not in session:
        session['nombre'] = ''
    if 'direccion' not in session:
        session['direccion'] = ''
    if 'telefono' not in session:
        session['telefono'] = ''
    if 'fechaCompra' not in session:
        session['fechaCompra'] = ''
    
    #-------------------
    if request.method == "POST":
        #pedido_form = forms.PedidoForm()
        pedido_form = forms.PedidoForm(request.form)
        if pedido_form.validate():
            
            nombre = request.form['nombre']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            tamano = request.form['tamano']
            ingredientes = ', '.join(request.form.getlist('ingredientes'))  
            no_pizzas = int(request.form['no_pizzas'])
            fechaCompra = str(request.form['fechaCompra'])
            
            costo_por_ingredientes = len(request.form.getlist('ingredientes')) * 10

            if tamano == 'chica':
                subtotal = no_pizzas * 40 + (costo_por_ingredientes * no_pizzas)
            elif tamano == 'mediana':
                subtotal = no_pizzas * 80 + (costo_por_ingredientes * no_pizzas)
            else:
                subtotal = no_pizzas * 120 + (costo_por_ingredientes * no_pizzas)

            idsugerido = len(pedidos) + 1
            while idsugerido in [pedido['id'] for pedido in pedidos]:
                idsugerido += 1

            pedidos.append({
                'id': idsugerido,
                'nombre': nombre,
                'direccion': direccion,
                'telefono': telefono,
                'tamano': tamano,
                'ingredientes': ingredientes,
                'no_pizzas': no_pizzas,
                'subtotal': subtotal,
                'fechaCompra':fechaCompra
            })

            return redirect("/pedidos")
    else:
        nombre = session.get('nombre', '')
        direccion = session.get('direccion', '')
        telefono = session.get('telefono', '')
        fechaCompra = session.get('fechaCompra', '')

        pedido_form = forms.PedidoForm(nombre=nombre, direccion=direccion, telefono=telefono, fechaCompra=fechaCompra)
        
    return render_template("pizzas.html", form=pedido_form, pedidos1=pedidos)

@app.route("/quitar_pedido", methods=["POST"])
def quitar_pedido():
    global pedidos

    pedido_id = int(request.form["pedido_id"])

    pedidos = [pedido for pedido in pedidos if pedido["id"] != pedido_id]

    return redirect('/pedidos')

@app.route("/alerta", methods=["POST"])
def guardar_pedido():
    total_pedido = sum(pedido['subtotal'] for pedido in pedidos) 

    return render_template("confirmar_pedido.html", total_pedido=total_pedido)

@app.route("/confirmar_pedido", methods=["POST"])
def confirmar_pedido():
    global pedidos
    decision = request.form.get('decision')
    
    if decision == 'si':
        total_venta = 0
        for p in pedidos:
            ped = Pedido(
            nombre = p['nombre'],
            direccion = p['direccion'],
            telefono = p['telefono'],
            tamano = p['tamano'],
            ingredientes = p['ingredientes'],
            no_pizzas = p['no_pizzas'],
            fechaCompra = p['fechaCompra']
            )
            db.session.add(ped)
            db.session.commit()

        total_venta = sum(pedido['subtotal'] for pedido in pedidos) 
        venta = Venta(
            nombre = pedidos[0]['nombre'],
            total = total_venta,
            fechaVenta = pedidos[0]['fechaCompra']
        )
        db.session.add(venta)
        db.session.commit()
        pedidos = []
        return redirect("/ventas")
    else:
        return redirect("/pedidos")


@app.route("/ventas", methods=["GET", "POST"])
def mostrar_ventas():
    ventas = []
    total_ventas = 0

    if request.method == "POST":
        dia_seleccionado = request.form.get('dia')
        mes_seleccionado = request.form.get('mes')

        if dia_seleccionado:
            # Convertir el día seleccionado a su número correspondiente
            dia_numero = int(dia_seleccionado) + 1
            # Consultar las ventas para el día seleccionado
            ventas = Venta.query.filter(func.DAYOFWEEK(Venta.fechaVenta) == dia_numero).all()
        elif mes_seleccionado:
            mes_numero = int(mes_seleccionado)
            # Consultar las ventas para el mes seleccionado
            ventas = Venta.query.filter(func.extract('month', Venta.fechaVenta) == mes_numero).all()
        else:
            # Si no se selecciona un día ni un mes, obtener todas las ventas
            ventas = Venta.query.all()

        total_ventas = sum(venta.total for venta in ventas)

    return render_template("ventas.html", ventas=ventas, total_ventas=total_ventas)


if __name__ == "__main__":
    crsf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()