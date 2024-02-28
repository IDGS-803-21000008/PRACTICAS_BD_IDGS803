from flask import Flask, render_template, request, flash, Response
import forms
from flask_wtf.csrf import CSRFProtect
from flask import redirect
from flask import g 
from config import DevelopmentConfig
from models import db
from models import Alumnos, Empleados

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

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()