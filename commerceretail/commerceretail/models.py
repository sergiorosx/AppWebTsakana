from sqlalchemy import Column, Integer, BigInteger, Float, String, LargeBinary, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from commerceretail.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String, unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

# Id (PK), cédula (UK), nombre, dirección, teléfono, foto
class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    cedula = Column(String(20), unique=True)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(BigInteger, nullable=False)
    foto = Column(LargeBinary, nullable=False)

    def __init__(self, cedula, nombre, direccion, telefono, foto):
        self.cedula = cedula
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.foto = foto

    def __repr__(self):
        return '<Client %r>' % (self.nombre)

# Id, Descripcion(UK)
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(20), unique=True)

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return '<Category %r>' % (self.descripcion)

# Id, código del producto (UK), categoría (FK), nombre, precio, cantidad en bodega, estado -activo, inactivo-
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    codigo = Column(String, unique=True)
    categoria_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    categoria = relationship('Category', backref='categories', lazy=True)
    nombre = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    cantidad_en_bodega = Column(Integer, nullable=False)
    estado = Column(Boolean, nullable=False)

    def __init__(self, codigo, categoria_id, nombre, precio, cantidad_en_bodega, estado):
        self.codigo = codigo
        self.categoria_id = categoria_id
        self.nombre = nombre
        self.precio = precio
        self.cantidad_en_bodega = cantidad_en_bodega
        self.estado = estado

    def __repr__(self):
        return '<Product %r>' % (self.codigo)

# id, Descripcion(UK)
class PaymentMethod(Base):
    __tablename__ = 'paymentmethod'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(20), unique=True)

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return '<PaymentMethod %r>' % (self.descripcion)

# id factura, código de la factura, cliente que realiza la compra (FK), fecha de compra, 
# método de pago, valor total-> valor calculado
class BillHeader(Base):
    __tablename__ = 'billheader'
    id = Column(Integer, primary_key=True)
    codigo = Column(String, unique=True)
    cliente_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    cliente = relationship('Client', backref='clients', lazy=True)
    fecha_compra = Column(DateTime, nullable=False)
    metodo_pago_id = Column(Integer, ForeignKey('paymentmethod.id'), nullable=False)
    metodo_pago = relationship('PaymentMethod', backref='paymentmethods', lazy=True)

    def __init__(self, codigo, cliente_id, fecha_compra, metodo_pago_id):
        self.codigo = codigo
        self.cliente_id = cliente_id
        self.fecha_compra = fecha_compra
        self.metodo_pago_id = metodo_pago_id

    def __repr__(self):
        return '<BillHeader %r>' % (self.codigo)

# id detalle, id factura, producto, precio, cantidad de producto
class BillDetail(Base):
    __tablename__ = 'billdetail'
    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey('billheader.id'), nullable=False)
    factura = relationship('BillHeader', backref='billheaders', lazy=True)
    producto_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    producto = relationship('Product', backref='products', lazy=True)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)

    def __init__(self, factura_id, producto_id, precio, cantidad):
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.precio = precio
        self.cantidad = cantidad

    def __repr__(self):
        return '<BillDetail %r %r>' % (self.id, self.factura_id)