from sqlalchemy import Column, String, Integer, Float, Boolean
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import db


class Producto(db.Base):

    __tablename__ = "producto"

    __table_args__ = {'sqlite_autoincrement': True}

    id_producto = Column(Integer, primary_key=True)
    nombre_producto = Column(String(200), nullable=False)
    precio_pedido = Column(Float, nullable=False)
    descripcion_producto = Column(String,nullable=False)
    stock_producto = Column(Integer, nullable=False)
    existencias_producto = Column(Integer,nullable=False)
    numero_vendido = Column(Integer, nullable=False)
    empresa = Column(String(200), nullable=False)

    def __init__(self, nombre_producto, precio_pedido, descripcion_producto, stock_producto, existencias_producto, numero_vendido, empresa):
        self.nombre_producto = nombre_producto
        self.precio_pedido = precio_pedido
        self.descripcion_producto = descripcion_producto
        self.stock_producto = stock_producto
        self.existencias_producto = existencias_producto
        self.numero_vendido = numero_vendido
        self.empresa = empresa


    def __str__(self):
            return '''
            Producto: {}
            Precio: {}
            Descripcion:{}
            Stock: {}
            En existencia: {}
            Se ha vendido: {}
            Empresa: {}'''.format(self.nombre_producto, self.precio_pedido, self.descripcion_producto, self.stock_producto, self.existencias_producto, self.numero_vendido, self.empresa)




class Administrador(db.Base):

    # Lo que pasara al momento de crear la base de datos obvio no tendremos ningun administrador, entonces lo que haremos es que en el main donde empieza a
    # correr el programa crearemos un objeto de la clase administrador para que se pueda utilizar

    __tablename__ = 'admin'

    __table_args__ = {'sqlite_autoincrement': True}

    id_admin = Column(Integer, primary_key=True)
    nombre_admin = Column(String(200), nullable=False)
    apellidos_admin = Column(String(200), nullable=False)
    correo_admin = Column(String(200), nullable=False)
    username_admin = Column(String(20), nullable=False)
    password_admin = Column(String(100), nullable=False)
    fotografia_admin = Column(String, nullable=False)
    ventas_admin = Column(Integer, nullable=False)
    rango_admin = Column(String, nullable=False)

    def __init__(self, nombre_admin, apellidos_admin, correo_admin, username_admin, password_admin, fotografia_admin,ventas_admin, rango_admin):
        self.nombre_admin = nombre_admin
        self.apellidos_admin = apellidos_admin
        self.correo_admin = correo_admin
        self.username_admin = username_admin
        self.password_admin = self.__create_password(password_admin)
        self.fotografia_admin = fotografia_admin
        self.ventas_admin = ventas_admin
        self.rango_admin = rango_admin


    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_admin, password)

    def __str__(self):
        return '''
            Nombre: {}
            Apellidos: {}
            Correo: {}
            Usuario: {}
            Contraseña: {}
            Fotografia: {}
            Ventas: {}
            Rango: {}'''.format(self.nombre_admin, self.apellidos_admin, self.correo_admin, self.username_admin,self.password_admin,
                                self.fotografia_admin,self.ventas_admin, self.rango_admin)

class Cliente(db.Base):

    __tablename__ = 'personal'

    __table_args__ = {'sqlite_autoincrement': True}

    id_personal = Column(Integer, primary_key=True)
    nombre_personal = Column(String(200), nullable=False)
    apellidos_personal = Column(String(200), nullable=False)
    correo_personal = Column(String(200), nullable=False)
    usuario_personal = Column(String(200), nullable=False)
    password_personal = Column(String(200), nullable=False)
    telefono_cliente = Column(String(200), nullable=False)
    fotografia_personal = Column(String, nullable=False)
    rango_personal = Column(String, nullable=False)
    ventas_personal = Column(Integer, nullable=False)


    def __init__(self, nombre_personal, apellidos_personal, correo_personal, usuario_personal, password_personal, telefono_cliente, fotografia_personal, rango_personal, ventas_personal):
        self.nombre_personal = nombre_personal
        self.apellidos_personal = apellidos_personal
        self.correo_personal = correo_personal
        self.usuario_personal = usuario_personal
        self.password_personal = self.__create_password(password_personal)
        self.telefono_cliente = telefono_cliente
        self.fotografia_personal = fotografia_personal
        self.rango_personal = rango_personal
        self.ventas_personal = ventas_personal

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_personal, password)

    def __str__(self):
        return '''
        Nombre: {}
        Apellidos: {}
        Correo: {}
        Usuario: {}
        Contraseña: {}
        Telefono: {}
        Fotografia: {}
        Rango: {}
        Ventas: {}'''.format(self.nombre_personal, self.apellidos_personal, self.correo_personal, self.usuario_personal, self.password_personal,
                            self.telefono_cliente,self.fotografia_personal,self.rango_personal, self.ventas_personal)

class Proveedor(db.Base):

    __tablename__ = "proveedor"

    __table_args__ = {'sqlite_autoincrement': True}

    id_proveedor = Column(Integer, primary_key=True)
    nombre_proveedor = Column(String(200), nullable=False)
    telefono_proveedor = Column(String(100), nullable=False)
    correo_proveedor = Column(String, nullable=False)
    direccion_proveedor = Column(String(500), nullable=False)
    precios_proveedor = Column(String(900), nullable=False)
    descuento_proveedor = Column(String(100), nullable=False)
    iva_proveedor = Column(Float, nullable=False)
    username_proveedor = Column(String(200), nullable=False)
    password_proveedor = Column(String(200), nullable=False)
    ventas_proveedor = Column(Integer, nullable=False)
    logo_proveedor = Column(String(200))
    rango_proveedor = Column(String(200))

    def __init__(self, nombre_proveedor, telefono_proveedor, correo_proveedor, direccion_proveedor, precios_proveedor, descuento_proveedor, iva_proveedor, username_proveedor, password_proveedor,ventas_proveedor, logo_proveedor, rango_proveedor):
        self.nombre_proveedor = nombre_proveedor
        self.telefono_proveedor = telefono_proveedor
        self.correo_proveedor = correo_proveedor
        self.direccion_proveedor = direccion_proveedor
        self.precios_proveedor = precios_proveedor
        self.descuento_proveedor = descuento_proveedor
        self.iva_proveedor = iva_proveedor
        self.username_proveedor = username_proveedor
        self.password_proveedor = self.__create_password(password_proveedor)
        self.ventas_proveedor = ventas_proveedor
        self.logo_proveedor = logo_proveedor
        self.rango_proveedor = rango_proveedor

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_proveedor, password)

    def __str__(self):
        return """
        Empresa: {}
        Telefono: {}
        Correo: {}
        Direccion: {}
        Precios: {}
        Descuento: {}
        IVA: {}
        Usuario: {}
        Contraseña: {}
        Ventas: {}
        Logo: {}
        Rango: {}""".format(self.nombre_proveedor, self.telefono_proveedor, self.correo_proveedor, self.direccion_proveedor, self.precios_proveedor, self.descuento_proveedor,
                           self.iva_proveedor, self.username_proveedor, self.password_proveedor, self.ventas_proveedor, self.logo_proveedor, self.rango_proveedor)

class Ventas(db.Base):

    __tablename__ = "ventas"
    __table_args__ = {'sqlite_autoincrement': True}

    id_venta = Column(Integer, primary_key=True)
    nombre_venta = Column(String(200),nullable=False)
    cantidad_venta = Column(Integer, nullable=False)
    fecha_venta = Column(String(200), nullable=False)
    precio_total_venta = Column(Float, nullable=False)
    cobro_venta = Column(String(200), nullable=False)

    def __init__(self, nombre_venta, cantidad_venta, fecha_venta, precio_total_venta, cobro_venta):
        self.nombre_venta = nombre_venta
        self.cantidad_venta = cantidad_venta
        self.fecha_venta = fecha_venta
        self.precio_total_venta = precio_total_venta
        self.cobro_venta = cobro_venta

    def __str__(self):
        return """
        ID: {}
        Venta: {}
        Cantidad: {}
        Fecha: {}
        Total: {}
        Atendio: {}""".format(self.id_venta,self.nombre_venta,self.cantidad_venta, self.fecha_venta, self.precio_total_venta,
                              self.cobro_venta)