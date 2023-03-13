#                               D E S C R I P C I O N   D E L   A R C H I V O

# Dentro de este archivo van a ir muchas todas las funciones que no sean para flask, por decir tenemos una que es para
# Crear el administrador, preferi dejar el main solo para las funciones que va a tener flask y cree esta carpeta para
# Poder meter mis funciones extra como la de allowed_file entre otras que se iran creando

#-----------------------------------------------------------------------------------------------------------------------
#                                       I M P O R T A C I O N E S

# Ya que tambien vamos a trabajar con funciones o variables del main tenemos que decirle que del main, de models nos vayan
# Importando lo que vayamos ocupando
from main import ALLOWED_EXTENSIONS
from models import *
import db
from os import path, remove
import uuid
from flask import render_template, flash
import smtplib
from pyinvoice.models import  ServiceProviderInfo, ClientInfo, Item
from pyinvoice.templates import SimpleInvoice
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
#-----------------------------------------------------------------------------------------------------------------------
#                                           F U N C I O N E S

def comprobacion_datos(username,correo):
    consult_user_proveedor = db.session.query(Proveedor).filter(Proveedor.username_proveedor == username).first()
    consult_user_admin = db.session.query(Administrador).filter(Administrador.username_admin == username).first()
    consult_username = db.session.query(Cliente).filter(Cliente.usuario_personal == username).first()

    consult_email_cliente = db.session.query(Cliente).filter(Cliente.correo_personal == correo).first()
    consult_email_admin = db.session.query(Administrador).filter(Administrador.correo_admin == correo).first()
    consult_email_proveedor = db.session.query(Proveedor).filter(Proveedor.correo_proveedor == correo).first()

    if (consult_username != None):
        flash("El usuario ya esta en uso")
        return render_template("crear_proveedor.html")
    else:
        if (consult_user_admin != None):
            flash("El usuario ya esta en uso")
            return render_template("crear_proveedor.html")
        else:
            if(consult_user_proveedor != None):
                flash("El usuario ya esta en uso")
                return render_template("crear_proveedor.html")
            else:
                if(consult_email_cliente != None):
                    flash("El correo ya esta en uso")
                    return render_template("crear_proveedor.html")
                else:
                    if(consult_email_admin != None):
                        flash("El correo ya esta en uso")
                        return render_template("crear_proveedor.html")
                    else:
                        if(consult_email_proveedor != None):
                            flash("El correo ya esta en uso")
                            return render_template("crear_proveedor.html")
                        else:
                            return True

# Funcion de carga de foto de perfil
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Funcion para crear un administrador
def crear_admin():
    a = Administrador(nombre_admin="Alberto David", apellidos_admin="Vazquez Montes", correo_admin="beto@gmail.com",
                        username_admin="beto",password_admin="0",fotografia_admin="alexis.gif",ventas_admin=0,rango_admin="admin")
    db.session.add(a)
    db.session.commit()
    return print("Se creo el Administrador")

def crear_usuario():
    u = Cliente(nombre_personal="Martin",apellidos_personal="De la torre Vazquez",correo_personal="martindelatorrevazquez029@outlook.com",
                usuario_personal="Vazquez1240", password_personal="0",telefono_cliente="4811232663",fotografia_personal="alexis.gif", rango_personal="personal",
                ventas_personal=0)
    db.session.add(u)
    db.session.commit()
    print("Se creo el usuario")

# verificamos si la ruta existe
def path_url_exists(path_url):
    if( path.exists(path_url)):
        return True
    else:
        return False



# Metgodo para eliminar la foto de perfil del usuario
def remove_picture_profile(profile_name):
    path_url = '/proyecto tokio/TiendaVirtual/static/imagenes' + profile_name
    if(path_url_exists(path_url)):
        remove(path_url)


def ramdom_name(name_base):
    filename = str(uuid.uuid1()) + "_" + name_base
    return filename

def update_profile_picture(rango,id, picture):
    if(rango == 'admin'):
        consult = db.session.query(Administrador).filter(Administrador.id_admin == id).first()
        if(consult != None):
            if(consult.fotografia_admin is not None):
                remove_picture_profile(consult.fotografia_admin)
                consult.fotografia_admin = picture
                return consult.fotografia_admin
            else:
                consult.fotografia_admin = picture
                return consult.fotografia_admin

    elif(rango == 'personal'):
        consult = db.session.query(Cliente).filter(Cliente.id_personal == id).first()
        if(consult != None):
            if(consult.fotografia_personal):
                remove_picture_profile(consult.fotografia_personal)
                consult.fotografia_personal = picture
                return consult.fotografia_personal
            else:
                consult.fotografia_personal = picture
                return consult.fotografia_personal

    elif (rango == 'proveedor'):
        consult = db.session.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
        if (consult != None):
            if (consult.logo_proveedor):
                remove_picture_profile(consult.logo_proveedor)
                consult.logo_proveedor = picture
                return consult.logo_proveedor
            else:
                consult.logo_proveedor = picture
                return consult.logo_proveedor
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funcion de enviar correo
def send_email(nombre,destinatario):
    message = "Hola Bienvenido {}, Es un gusto darte la bienvenida a esta empresa, que ya es tu nueva familia".format(nombre)
    subject = "Bienvenido  a Technology Store"
    message = 'Subject: {}\n\n{}'.format(subject, message)
    print(destinatario)
    server = smtplib.SMTP('smtp.outlook.com',587)
    server.starttls()
    server.login("jinjadepython@outlook.com","Futbol26")

    server.sendmail("jinjadepython@outlook.com", destinatario,message)
    server.quit()

    print("el correo se envio correcatamente")

# Funcion de mandar correos a las empresas nuevas
def send_email_new_business(name,email_business):
    subject = "Gracias por aceptar esta oferta"
    message = f"Muchas gracias por aceptar {name}, te agradecemos que formes parte de nuestro grupo de proveedores"
    message = "Subject: {}\n\n{}".format(subject,message)

    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.starttls()
    server.login("jinjadepython@outlook.com", "Futbol26")

    server.sendmail("jinjadepython@outlook.com", email_business, message)
    server.quit()
    print("El correo se ha creado correctamente")

def send_email_producto(producto,email_business,remitente):
    subject = "Necesitamos Stock"
    message = f"""Buen dia, somos {remitente}, este es correo para pedir si nos manda sustento del producto {producto}, ya que nos estamos quedando sin
suministros favor de responder este correo de recibido!
Un saludo {remitente}"""

    message = "Subject: {}\n\n{}".format(subject, message)
    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.starttls()
    server.login("jinjadepython@outlook.com", "Futbol26")

    #server.sendmail("prueba_de_flask@outlook.com",email_business,message)
    server.sendmail("jinjadepython@outlook.com", email_business, message)

    server.quit()
    print("El correo se ha enviado correctamente!")
    return True



def  calcular_product(id_produ,producto,email_business,remitente):
    buscar = db.session.query(Producto).filter(Producto.id_producto == id_produ).first()
    if(buscar != None):
        porcentaje = 10
        numero = int(buscar.stock_producto)

        operacion = porcentaje + numero / 100

        if(buscar.existencias_producto <= operacion):
            print("Se tiene que mandar el correo")
            return send_email_producto(producto,email_business,remitente)

        else:
            return True

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def create_product():
    product = Producto(nombre_producto="Teclado Gamer",precio_pedido=5400,descripcion_producto="Teclado Gamer de la marca Logitech",
                       stock_producto=560,existencias_producto=560,numero_vendido=0,empresa='logitech')

    db.session.add(product)
    db.session.commit()
    print("Se ha creado el producto")

#-----------------------------------------------------------------------------------------------------------------------

def calcular_cuanto_falta(productos_existencia, productos_faltantes):
    tengo = productos_existencia
    necesito = productos_faltantes

    falta = necesito - tengo

    return falta


def verificar_existencias(id,empresa):
    busqueda = db.session.query(Producto).filter(Producto.id_producto == id).first()
    if(busqueda.existencias_producto == 0):
        flash("No hay mas existencias")
        return False
    else:
        return True

#-----------------------------------------------------------------------------------------------------------------------
def sumar_venta(name_product,num_venta):
    busqueda = db.session.query(Producto).filter(Producto.nombre_producto == name_product).first()
    if(busqueda != None):
        suma = busqueda.numero_vendido + num_venta
        busqueda.numero_vendido = suma
        db.session.commit()
        return True
def sumar_venta_business(empresa, num_pedido,stock):
    busqueda = db.session.query(Proveedor).filter(Proveedor.username_proveedor == empresa).first()
    if(busqueda != None):
        operacion = num_pedido * stock
        suma = busqueda.ventas_proveedor + operacion
        busqueda.ventas_proveedor = suma
        db.session.commit()
        return True

#-----------------------------------------------------------------------------------------------------------------------
def vender_product(catidad_quitar,product, personal):
    consulta = db.session.query(Producto).filter(Producto.nombre_producto == product).first()
    vendio = db.session.query(Cliente).filter(Cliente.usuario_personal == personal).first()
    vendio_admin = db.session.query(Administrador).filter(Administrador.username_admin == personal).first()
    if(consulta != None):
        if(vendio != None):
            suma = vendio.ventas_personal + catidad_quitar
            resta = consulta.existencias_producto - catidad_quitar
            vendio.ventas_personal = suma
            consulta.existencias_producto = resta
            db.session.commit()
            return True
        elif(vendio_admin != None):
            suma = vendio_admin.ventas_admin + catidad_quitar
            resta = consulta.existencias_producto - catidad_quitar
            vendio_admin.ventas_admin = suma
            consulta.existencias_producto = resta
            db.session.commit()
            return True
    else:
        return False

def rellenar(cantidad_sumar, product, provedor):
    consulta_provedor = db.session.query(Proveedor).filter(Proveedor.username_proveedor == provedor).first()
    consulta = db.session.query(Producto).filter(Producto.nombre_producto == product).first()
    if(consulta != None):
        if(consulta_provedor != None):
            suma_venta = consulta_provedor.ventas_proveedor + cantidad_sumar
            suma = consulta.existencias_producto + cantidad_sumar
            if(suma > consulta.stock_producto):
                flash("La cantidad no puede ser mayor a la indicada")
                return render_template('edit_product.html', product=consulta)
            else:
                consulta_provedor.ventas_proveedor = suma_venta
                consulta.existencias_producto = suma
                db.session.commit()
                return True
        else:
            return False
    else:
        return False


#-----------------------------------------------------------------------------------------------------------------------
#                  C A L C U L A R   E L  P R E C I O    F I N A L   D E L   N U E V O   P R O D U C T O

def precio_nuevo_producto(cantidad,precio_pedido, descuento):
    global precio_final

    operacion = cantidad * precio_pedido
    coversion_porcentaje = descuento / 100
    multiplicacion = operacion * coversion_porcentaje
    precio_final = operacion - multiplicacion

    if(operacion > 0):
        flash(f"El precio final es de: {precio_final}")
        return precio_final
    else:
        precio_final = -1
        flash("Ocurrio un error, La operacion de volvo 0 o un numero menor")
        return precio_final
#-----------------------------------------------------------------------------------------------------------------------
#                                              F A C T U R A S
def create_factura(name_business, calle, nombre_cliente, email_cliente, producto, descripcion, precio_pedido, iva):
    doc = SimpleInvoice("factura.pdf")
    doc.is_paid = True



    doc.service_provider_info = ServiceProviderInfo(
        name=name_business,
        street=calle
    )

    doc.client_info = ClientInfo(name=nombre_cliente,email=email_cliente)

    doc.add_item(Item(producto, descripcion, 1, precio_pedido))

    doc.set_item_tax_rate(iva)
    print("Se ha creado el documento")
    doc.finish()
#-----------------------------------------------------------------------------------------------------------------------
#                                               G R A F I C A S

#                                                 V E N T A S
def grafica_ventas():
    conect = sqlite3.connect("./database/tienda.db")
    df = pd.read_sql_query("SELECT * from producto", conect)
    print(df)
    valores = df[["nombre_producto","numero_vendido"]]
    ax = valores.plot.bar(x="nombre_producto", y="numero_vendido", rot=0)
    plt.show()
    conect.close()


#                                                  C O M P R A S
def graficas_compras(empresa):
    conect = sqlite3.connect("./database/tienda.db")
    sql = f"SELECT * FROM producto WHERE empresa = '{empresa}'"
    df = pd.read_sql_query(sql, conect)
    valores = df[["nombre_producto","numero_vendido"]]
    ax = valores.plot.bar(x="nombre_producto", y="numero_vendido", rot=0)
    plt.show()
    conect.close()

#                                            C O M P A R A T I V A S

def grafica_comparativa():
    conect = sqlite3.connect("./database/tienda.db")
    sql_ventas = "SELECT * FROM personal"
    sql_ventas_admin = "SELECT * FROM admin"
    sql_compras = "SELECT * FROM producto"

    df_ventas = pd.read_sql_query(sql_ventas,conect)
    df_compras = pd.read_sql_query(sql_compras, conect)
    df_ventas_admin = pd.read_sql_query(sql_ventas_admin, conect)


    lista_compra = []
    for compra in df_compras["numero_vendido"]:
        lista_compra.append(compra)
    compra = sum(lista_compra)


    lista_ventas = []
    for venta in df_ventas["ventas_personal"]:
        lista_ventas.append(venta)
    venta = sum(lista_ventas)

    for venta_admin in df_ventas_admin["ventas_admin"]:
        lista_ventas.append(venta_admin)

    venta = sum(lista_ventas)
    datos = {"Venta":venta,
             "Compra":compra
             }

    df = pd.DataFrame(datos, columns=["Venta", "Compra"], index=[1])
    valores = df[["Venta", "Compra"]]
    ax = valores.plot.bar(xlabel="Grafica",ylabel=valores,rot=0)
    plt.show()
    conect.close()


