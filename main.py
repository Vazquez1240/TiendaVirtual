import uuid
from utils import utils
from flask.globals import session
import os
from flask import redirect, url_for, render_template, flash, request, Flask, send_file
from models import Cliente, Administrador, Ventas, Proveedor, Producto
import db
from werkzeug.utils import secure_filename
from datetime import datetime
import time

#-----------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)
UPLOAD_FOLDER = '/proyecto tokio/TiendaVirtual/static/imagenes'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SESSION_TYPE"] = 'filesystem'
app.secret_key = "adbcdefg23533@!#-$3$!EDFw"

#-----------------------------------------------------------------------------------------------------------------------

# Definimos la raiz de la aplicacion
@app.route('/')
def home():
    return render_template("index.html")


def check_inactivity():
    if('last_activity' in session):
        now = int(time.time())
        last_activity = session['last_activity']
        if(now - last_activity > 60):
            session.clear()
            return render_template('index.html')

    session['last_activity'] = int(time.time())

#-----------------------------------------------------------------------------------------------------------------------
# Creamos la ruta de crear-personal que nos sirve para crear personal nuevo que ingrese


@app.route('/crear-personal', methods=["POST","GET"])
def crear_personal():
    if(request.method == "POST"):
        name = request.form['nombre']
        surnames = request.form["apellidos"]
        correo = request.form['email']
        telefono = request.form['telefono']
        username = request.form['username']
        contrasenia = request.form["password"]
        confirm_password = request.form['conpass']
        fotografia = request.files["foto"]
        print(fotografia)
        if(contrasenia != confirm_password):
            flash("Las contraseñas no coinciden")
            return render_template("crear_personal.html")
        else:
            comprobation = utils.comprobacion_datos(username,correo)
            if(comprobation == True):
                if 'foto' not in request.files:
                    flash('Archivo inexistente')
                    return render_template("crear_personal.html")
                file = request.files['foto']
                if file.filename == '':
                    flash('No selecciono un archivo')
                    return render_template("crear_personal.html")
                if file and utils.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    pic_name = str(uuid.uuid1()) + "_" + filename

                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))
                    personal = Cliente(nombre_personal=name, apellidos_personal=surnames, correo_personal=correo,usuario_personal=username,
                                    password_personal=contrasenia, telefono_cliente=telefono, fotografia_personal=pic_name,rango_personal="personal", ventas_personal=0)
                    db.session.add(personal)
                    db.session.commit()
                    utils.send_email(name,correo)
                    flash("Se ha creado Correctamente el personal")
                    return redirect(url_for('logeo'))
            else:
                return render_template("crear_personal.html")
    return render_template("crear_personal.html")

@app.route('/crear-proveedor', methods=["POST","GET"])
def crear_proveedor():
    if (request.method == "POST"):
        name = request.form['empresa']
        telefono = request.form["telefono"]
        correo = request.form['email']
        direccion = request.form['direccion']
        precios = request.form['precios']
        descuento = request.form["descuento"]
        iva = request.form['iva']
        username = request.form["username"]
        contrasenia = request.form["password"]
        confirm_password = request.form["conpass"]
        if (contrasenia != confirm_password):
            flash("Las contraseñas no coinciden")
            return render_template("crear_personal.html")
        else:
            comprobation = utils.comprobacion_datos(username, correo)
            if (comprobation == True):
                if 'foto' not in request.files:
                    flash('Archivo inexistente')
                    return render_template("crear_proveedor.html")
                file = request.files['foto']
                if file.filename == '':
                    flash('No selecciono un archivo')
                    return render_template("crear_proveedor.html")
                if file and utils.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    pic_name = str(uuid.uuid1()) + "_" + filename

                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                    proveedor = Proveedor(nombre_proveedor=name,telefono_proveedor=telefono,correo_proveedor=correo, direccion_proveedor=direccion,
                                          precios_proveedor=precios,descuento_proveedor=descuento, iva_proveedor=iva, username_proveedor=username, password_proveedor=contrasenia,
                                          ventas_proveedor=0,logo_proveedor=pic_name,rango_proveedor="proveedor")
                    print(proveedor.direccion_proveedor)
                    db.session.add(proveedor)
                    db.session.commit()
                    utils.send_email_new_business(name,correo)
                    flash("Se ha creado Correctamente el personal", "info")
                    return redirect(url_for('logeo'))
            else:
                return render_template("crear_proveedor.html")
    return render_template("crear_proveedor.html")
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/logeo', methods=["POST","GET"])
def logeo():
    check_inactivity()
    if(request.method == "POST"):
        user = request.form["username"]
        contrasenia = request.form["password"]

        consulta_proveedor = db.session.query(Proveedor).filter(Proveedor.username_proveedor == user).first()
        consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == user).first()
        consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == user).first()
        productos = db.session.query(Producto).all()
        productos_empresa = db.session.query(Producto).filter(Producto.empresa == user).all()

        if(consulta_cliente is not None and consulta_cliente.verify_password(contrasenia)):
            check_inactivity()
            session["usuario"] = user
            session["rol"] = "personal"
            return render_template("sesion.html", username=user, rol=session["rol"], personal = consulta_cliente, p= productos)

        elif(consulta_admin is not None and consulta_admin.verify_password(contrasenia)):
            check_inactivity()
            session["usuario"] = user
            session["rol"] = "admin"
            return  render_template("sesion.html", username=user, rol=session["rol"],personal= consulta_admin, p=productos)

        elif (consulta_proveedor is not None and consulta_proveedor.verify_password(contrasenia)):
            check_inactivity()
            print(consulta_proveedor)

            session["usuario"] = user
            session["rol"] = "proveedor"
            print(user)

            return render_template("sesion.html", username=user, rol=session["rol"], productos_empresa=productos_empresa, personal=consulta_proveedor)

        else:
            flash("Usuario o contraseña no validos favor de verificar")
            return redirect(url_for('home'))

    else:
        print(session["rol"])
        productos = db.session.query(Producto).all()
        consulta_proveedor = db.session.query(Proveedor).filter(Proveedor.username_proveedor == session["usuario"]).first()
        consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == session["usuario"]).first()
        consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == session["usuario"]).first()
        if (consulta_admin != None):
            return render_template("sesion.html", username=session["usuario"], rol=session["rol"], personal = consulta_admin, p=productos)
        elif(consulta_cliente != None):
            return render_template("sesion.html", username=session["usuario"], rol=session["rol"],personal = consulta_cliente, p=productos)
        elif (consulta_proveedor != None):
            return render_template("sesion.html", username=session["usuario"], rol=session["rol"],personal=consulta_proveedor, p=productos)


#-----------------------------------------------------------------------------------------------------------------------

@app.route('/view-perfil/<id>/<rango>', methods=["GET","POST"])
def ver_perfil(id,rango):
    if(request.method == "POST"):
        if (rango == "admin"):
            consulta = db.session.query(Administrador).filter(Administrador.id_admin == id).all()
            if(consulta != None):
                return render_template("perfil.html", lista_datos = consulta, rol= session["rol"])
            else:
                consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == session["usuario"]).first()
                consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == session["usuario"]).first()
                if (consulta_admin != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_admin)
                elif (consulta_cliente != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_cliente)
        elif(rango == "personal"):
            consulta = db.session.query(Cliente).filter(Cliente.id_personal == id).all()
            print(consulta)
            if(consulta != None):
                return render_template("perfil.html", lista_datos=consulta, rol=session['rol'])
            else:
                consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == session["usuario"]).first()
                consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == session["usuario"]).first()
                if (consulta_admin != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_admin)
                elif (consulta_cliente != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_cliente)
        elif (rango == "proveedor"):
            consulta = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).all()
            print(consulta)
            if (consulta != None):
                return render_template("perfil.html", lista_datos=consulta, rol=session['rol'])
            else:
                consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == session["usuario"]).first()
                consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == session["usuario"]).first()
                consulta_provedor = db.session.query(Proveedor).filter(Proveedor.username_proveedor == session["usuario"]).first()
                if (consulta_admin != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_admin)
                elif (consulta_cliente != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_cliente)
                elif (consulta_provedor != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_provedor)

    else:
        if (rango == "admin"):
            consulta = db.session.query(Administrador).filter(Administrador.id_admin == id).all()
            if(consulta != None):
                return render_template("perfil.html", lista_datos = consulta, rol= session["rol"])
            else:
                consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == session["usuario"]).first()
                consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == session["usuario"]).first()
                if (consulta_admin != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_admin)
                elif (consulta_cliente != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_cliente)
        elif(rango == "personal"):
            consulta = db.session.query(Cliente).filter(Cliente.id_personal == id).all()
            print(consulta)
            if(consulta != None):
                return render_template("perfil.html", lista_datos=consulta, rol=session['rol'])
            else:
                consulta_provedor = db.session.query(Proveedor).filter(Proveedor.username_proveedor == session["usuario"]).first()
                consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == session["usuario"]).first()
                consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == session["usuario"]).first()
                if (consulta_admin != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_admin)
                elif (consulta_cliente != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_cliente)
                elif (consulta_provedor != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_provedor)

        elif (rango == "proveedor"):
            consulta = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).all()
            print(consulta)
            if (consulta != None):
                return render_template("perfil.html", lista_datos=consulta, rol=session['rol'])
            else:
                consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == session["usuario"]).first()
                consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == session["usuario"]).first()
                consulta_provedor = db.session.query(Proveedor).filter(Proveedor.username_proveedor == session["usuario"]).first()
                if (consulta_admin != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_admin)
                elif (consulta_cliente != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_cliente)
                elif (consulta_provedor != None):
                    return render_template("sesion.html", username=session["usuario"], rol=session["rol"],
                                           personal=consulta_provedor)


#-----------------------------------------------------------------------------------------------------------------------
#                 C A M B I A R   F O T O   D E   U S U A R I O    Y   D E S C A R G A   D E   F A C T U R A

@app.route("/download")
def Download_File():
    PATH = "factura.pdf"
    return send_file(PATH, as_attachment=True)


@app.route('/cambiar-foto/<id>/<rango>',methods=["POST","GET"])
def cambiar_foto(id,rango):
    if(request.method == "POST"):
        if(rango == 'admin'):
            consult = db.session.query(Administrador).filter(Administrador.id_admin == id).first()
            if(consult != None):

                utils.remove_picture_profile(consult.fotografia_admin)
                foto2 = request.files["update"]
                filename = secure_filename(foto2.filename)
                name = utils.ramdom_name(filename)
                a = utils.update_profile_picture(rango,id,name)
                print(a)
                foto2.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
                db.session.commit()
                return redirect(url_for("ver_perfil",id=id,rango=rango))


        elif(rango == "personal"):
            consulta = db.session.query(Cliente).filter(Cliente.id_personal == id).first()
            if(consulta != None):
                utils.remove_picture_profile(consulta.fotografia_personal)
                foto3 = request.files["update"]
                filename = secure_filename(foto3.filename)
                name = utils.ramdom_name(filename)
                a = utils.update_profile_picture(rango,id,name)
                foto3.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
                db.session.commit()
                return redirect(url_for("ver_perfil", id=id, rango=rango))

        elif(rango == 'proveedor'):
            consulta = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
            if (consulta != None):
                utils.remove_picture_profile(consulta.logo_proveedor)
                foto3 = request.files["update"]
                filename = secure_filename(foto3.filename)
                name = utils.ramdom_name(filename)
                a = utils.update_profile_picture(rango, id, name)
                foto3.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
                db.session.commit()
                return redirect(url_for("ver_perfil", id=id, rango=rango))

    if(rango =="admin"):
        buscar = db.session.query(Administrador).filter(Administrador.id_admin == id).first()
        return render_template("update_foto.html",datos=buscar, rango="admin")

    elif(rango == "personal"):
        buscar =  db.session.query(Cliente).filter(Cliente.id_personal == id).first()
        return render_template("update_foto.html", datos=buscar, rango="personal")

    elif (rango == "proveedor"):
        buscar = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
        return render_template("update_foto.html", datos=buscar, rango="proveedor")



#-----------------------------------------------------------------------------------------------------------------------
#                           P A R A   P O D E R   V E R   E L   P E R S O N A L

@app.route("/ver-personal",methods=["POST", "GET"])
def ver_personal():
    print(session["rol"])
    if(request.method == "POST"):
        personal = db.session.query(Cliente).all()
        for i in personal:
            print(i)
        return render_template("view_personal.html", lista_personal=personal)
    elif(request.method == "GET"):
        if(session["rol"] == 'admin'):
            personal = db.session.query(Cliente).all()
            return render_template("view_personal.html", lista_personal=personal)

#-----------------------------------------------------------------------------------------------------------------------
#                                   E D I T A R   P R O D U C T O

@app.route("/edit-product/<id>/<empresa>",methods=["POST","GET"])
def edit_product(id,empresa):
    consult = db.session.query(Producto).filter(Producto.id_producto == id).first()
    datos = db.session.query(Proveedor).filter(Proveedor.username_proveedor == empresa).first()
    consulta = db.session.query(Producto).filter(Producto.empresa == empresa).all()
    falta = utils.calcular_cuanto_falta(consult.existencias_producto,consult.stock_producto)
    if(request.method == "POST"):
        name = request.form["name"]
        precio = request.form["precio"]
        cantidad = int(request.form["cantidad"])
        print(name)
        a = utils.rellenar(cantidad,name,datos.username_proveedor)
        if(a == True):
            print(a)
            db.session.commit()
            utils.create_factura(datos.nombre_proveedor,datos.direccion_proveedor,"TecnologyStore","jinjadepython@outlook.com",name,
                                 consult.descripcion_producto,datos.precios_proveedor,datos.iva_proveedor)
            return render_template('view_product.html',producto=consulta, datos=datos)
        else:
            return render_template('edit_product.html',product=consult,cantidad=falta)

    return render_template("edit_product.html",product=consult, cantidad =falta)
#-----------------------------------------------------------------------------------------------------------------------
#                           B O R R A R   P R O D U C T O   Y   P E R S O N A L


@app.route("/delete-personal/<id>")
def delete_personal(id):
    personal = db.session.query(Cliente).filter_by(id_personal=id).delete()
    print("Personal Borrado: ",personal)
    db.session.commit()
    return redirect(url_for('ver_personal'))

@app.route("/delete-product/<id>")
def delete_product(id):
    product = db.session.query(Producto).filter_by(id_producto=id).delete()
    print("Producto Borrado:",product)
    db.session.commit()
    return redirect(url_for('aniadir_producto',user=session["usuario"]))
#-----------------------------------------------------------------------------------------------------------------------
#                                                 V E N D E R


@app.route('/vender', methods=["POST"])
def vender():
    consulta_proveedor = db.session.query(Proveedor).filter(Proveedor.username_proveedor == session["usuario"]).first()
    consulta_admin = db.session.query(Administrador).filter(Administrador.username_admin == session["usuario"]).first()
    consulta_cliente = db.session.query(Cliente).filter(Cliente.usuario_personal == session["usuario"]).first()
    productos = db.session.query(Producto).all()
    if(request.method == 'POST'):
        productos = db.session.query(Producto).all()

        product = request.form['producto']
        cantidad = int(request.form['cantidad'])
        if(cantidad == 0):
            flash("El total es cero")
            return render_template('edit_product.html', product=productos)
        else:
            precio = float(request.form['precio'])
            fecha = datetime.now()
            dia = str(fecha)
            total = precio * cantidad

            consulta = db.session.query(Producto).filter(Producto.nombre_producto == product).first()
            consult_business = db.session.query(Proveedor).filter(Proveedor.username_proveedor == consulta.empresa).first()

            if(consulta != None):
                if(consult_business != None):
                    verify = utils.verificar_existencias(consulta.id_producto, consulta.empresa)
                    if(verify == True):
                        a = utils.vender_product(cantidad, product, session["usuario"])
                        if(a == True):
                            utils.sumar_venta(product,cantidad)
                            venta = Ventas(nombre_venta=product, cantidad_venta=cantidad, fecha_venta=dia, precio_total_venta=total,cobro_venta=session['usuario'])
                            db.session.add(venta)
                            db.session.commit()
                            utils.calcular_product(consulta.id_producto, consulta.nombre_producto,consult_business.correo_proveedor,"Technology Store")

                            flash(f"El precio total es de: {total}")
                            return render_template('sesion.html', p=productos, rol=session['rol'],personal=consulta_cliente)
                        else:
                            print("Entro al False de a")
                            render_template('pagina_error.html')
                    else:
                        print("Entro al False de verify")
                        return render_template("sesion.html", p=productos, rol=session['rol'], personal=consulta_cliente)
                else:
                    print("Entro al False de consulta_bussines")
                    return render_template('pagina_error.html')
            else:
                print("Entro al False de consulta")
                return render_template('pagina_error.html')


    if(consulta_proveedor != None):
        return render_template('sesion.html', p=productos, rol=session['rol'],personal=consulta_proveedor)

    elif(consulta_admin != None):
        return render_template('sesion.html', p=productos, rol=session['rol'], personal=consulta_admin)

    elif(consulta_cliente != None):
        print("Estos son los productos: ",productos)
        return render_template('sesion.html', p=productos, rol=session['rol'], personal=consulta_cliente)



#-----------------------------------------------------------------------------------------------------------------------
#                                       A Ñ A D I R    P R O D U C T O

@app.route('/aniadir-product/<user>',methods=['GET'])
def aniadir_producto(user):
    consult = db.session.query(Producto).filter(Producto.empresa == user).all()
    consulta_usuario = db.session.query(Proveedor).filter(Proveedor.username_proveedor == user).first()
    return render_template('view_product.html', producto = consult,datos=consulta_usuario)

#-----------------------------------------------------------------------------------------------------------------------
#                                           A G R E G R A R   P R O D U C T O

@app.route('/add-product/<id>',methods=["POST","GET"])
def add_product(id):
    busqueda = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()

    if(request.method == "POST"):
        if(busqueda != None):
            name_product = request.form["name_producto"]
            descripcion = request.form["description"]
            stock = int(request.form["stock"])
            precio = float(request.form["precio"])
            cantidad = int(request.form["cantidad_pedido"])
            existencias = request.form["existencias"]
            descuento = int(busqueda.descuento_proveedor)
            operacion =  utils.precio_nuevo_producto(cantidad,precio,descuento)

            if(operacion > 0):
                utils.sumar_venta_business(busqueda.username_proveedor, cantidad, stock)
                product = Producto(nombre_producto=name_product, precio_pedido=precio,descripcion_producto=descripcion,
                                   stock_producto=stock,existencias_producto=existencias, numero_vendido=0,empresa=busqueda.username_proveedor)
                db.session.add(product)
                db.session.commit()
                utils.create_factura(busqueda.nombre_proveedor,busqueda.direccion_proveedor,"TecnologyStore",
                                      "jinjadepytho@outlook.com",name_product, descripcion,operacion,busqueda.iva_proveedor)
                return render_template('dowloand.html', user=session["usuario"])



    return render_template('add_product.html',provedor=busqueda)

#-----------------------------------------------------------------------------------------------------------------------
#                                           C E R R A R   S E S I O N

@app.route("/ver-graficas")
def ver_grafica():
     utils.grafica_ventas()
     return redirect(url_for("logeo"))

@app.route("/ver-graficas-provedor/<user>")
def graficas_provedor(user):
    utils.graficas_compras(user)
    return redirect(url_for("logeo"))

@app.route("/grafica-comparativa")
def grafica_comparativa():
    utils.grafica_comparativa()
    return redirect(url_for("logeo"))

@app.route('/close-session')
def close_session():
    session.clear()
    return redirect(url_for('home'))




#-----------------------------------------------------------------------------------------------------------------------
#                                                       M A I N

if (__name__ == '__main__'):
# Las importaciones que hacemos de utils nos sirven para cuando se esta empezando el programa, que se ocupa un administrador
# que se ocupa un producto y un usuario y con esas funciones los podemos crear al instante
    db.Base.metadata.create_all(db.engine)
    #utils.crear_admin()
    #utils.crear_usuario()
    #utils.create_product()
    app.run(debug=True,host='0.0.0.0')