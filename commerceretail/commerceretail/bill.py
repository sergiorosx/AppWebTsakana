from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, abort
)
from werkzeug.exceptions import abort
from sqlalchemy import func
import datetime
from commerceretail.database import db_session
from commerceretail.auth import login_required
from commerceretail.models import BillHeader
from commerceretail.models import BillDetail
from commerceretail.models import PaymentMethod
from commerceretail.models import Client
from commerceretail.models import Product

bp = Blueprint('bill', __name__, url_prefix='/bill')


@bp.route('/')
@login_required
def index():
    bills = db_session.query(BillHeader, func.sum(BillDetail.precio * BillDetail.cantidad).label('valortotal')).outerjoin(BillDetail, BillHeader.id == BillDetail.factura_id).outerjoin(Client, BillHeader.cliente_id == Client.id).group_by(BillHeader.id).all()
    return render_template('bill/index.html', bills = bills)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    clients = Client.query.all()
    paymentmethods = PaymentMethod.query.all()

    if request.method == 'POST':
        codigo = request.form['codigo']
        cliente_id = request.form['cliente_id']
        array_fecha_compra = request.form['fecha_compra'].split('-')
        fecha_compra = datetime.datetime(int(array_fecha_compra[0]), 
                                         int(array_fecha_compra[1]), 
                                         int(array_fecha_compra[2]))
        metodo_pago_id = request.form['metodo_pago_id']

        error = None
        
        if not codigo:
            error = 'Debe ingresar el código de la factura.'
        elif not cliente_id:
            error = 'Debe seleccionar un cliente.'
        elif not fecha_compra:
            error = 'Debe ingresar la fecha de compra.'
        elif not metodo_pago_id:
            error = 'Debe seleccionar un metodo de pago.'
        
        # client validation
        billRegistered = BillHeader.query.filter_by(codigo=codigo).first()
        if billRegistered is not None:
            error = 'La Factura {} ya se encuentra registrada.'.format(codigo)

        if error is not None:
            flash(error)
        else:
            newBill = BillHeader(codigo, cliente_id, fecha_compra, metodo_pago_id)
            db_session.add(newBill)
            db_session.commit()
            return redirect(url_for('bill.index'))

    return render_template('bill/create.html', paymentmethods = paymentmethods, clients = clients)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    bill = BillHeader.query.filter_by(id=id).first()
    clients = Client.query.all()
    paymentmethods = PaymentMethod.query.all()

    if request.method == 'POST':
        codigo = request.form['codigo']
        cliente_id = request.form['cliente_id']
        array_fecha_compra = request.form['fecha_compra'].split('-')
        fecha_compra = datetime.datetime(int(array_fecha_compra[0]), 
                                         int(array_fecha_compra[1]), 
                                         int(array_fecha_compra[2]))
        metodo_pago_id = request.form['metodo_pago_id']

        error = None
        
        if not codigo:
            error = 'Debe ingresar el código de la factura.'
        elif not cliente_id:
            error = 'Debe seleccionar un cliente.'
        elif not fecha_compra:
            error = 'Debe ingresar la fecha de compra.'
        elif not metodo_pago_id:
            error = 'Debe seleccionar un metodo de pago.'
        
        if error is not None:
            flash(error)
        else:
            bill.codigo = codigo
            bill.cliente_id = cliente_id
            bill.fecha_compra = fecha_compra
            bill.metodo_pago_id = metodo_pago_id
            db_session.commit()
            return redirect(url_for('bill.index'))
    return render_template('bill/update.html', bill=bill, clients = clients, paymentmethods = paymentmethods)


@bp.route('/<int:id>/detail', methods=('POST','GET'))
@login_required
def detail(id):
    bill = BillHeader.query.filter_by(id=id).first()
    billdetails = BillDetail.query.filter_by(factura_id=id).all()
    return render_template('bill/detail.html', bill=bill, billdetails=billdetails)


@bp.route('/<int:id>/addproduct', methods=('POST','GET'))
@login_required
def addproduct(id):
    products = Product.query.all()

    if request.method == 'POST':
        producto_id = request.form['producto_id']
        cantidad = request.form['cantidad']

        error = None

        if not producto_id:
            error = 'Debe seleccionar un producto'
        elif not cantidad:
            error = 'Debe ingresar una cantidad'
        elif int(cantidad) < 0:
            error = 'Debe ingresar un valor mayor a cero'
        
        product = Product.query.filter_by(id=producto_id).first()

        if product.cantidad_en_bodega < int(cantidad):
            error = 'La cantidad requerida del producto no se encuentra en bodega'

        if error is not None:
            flash(error)
        else:
            billdetail = BillDetail(id, producto_id, product.precio, cantidad)
            db_session.add(billdetail)
            product.cantidad_en_bodega = product.cantidad_en_bodega - int(cantidad)
            db_session.commit()
            return redirect(url_for('bill.detail', id=id))
    
    return render_template('bill/addproduct.html', products=products, bill_id=id)


@bp.route('/<int:id>/delete', methods=('POST','GET'))
@login_required
def delete(id):
    billdetails = BillDetail.query.filter_by(factura_id=id)

    for billdetail in billdetails:
        product = Product.query.filter_by(id=billdetail.producto_id).first()
        product.cantidad_en_bodega = product.cantidad_en_bodega + billdetail.cantidad
        db_session.commit()
    
    bill = BillHeader.query.filter_by(id=id).first()
    BillDetail.query.filter_by(factura_id=id).delete()
    db_session.delete(bill)
    db_session.commit()

    bills = BillHeader.query.all()
    return render_template('bill/index.html', bills=bills)


@bp.route('/<int:id>/deletedetail', methods=('POST','GET'))
@login_required
def deletedetail(id):

    billdetail = BillDetail.query.filter_by(id=id).first()
    
    product = Product.query.filter_by(id=billdetail.producto_id).first()
    product.cantidad_en_bodega = product.cantidad_en_bodega + billdetail.cantidad
    
    bill = BillHeader.query.filter_by(id=billdetail.factura_id).first()
    
    db_session.delete(billdetail)
    db_session.commit()

    billdetails = BillDetail.query.filter_by(factura_id=bill.id).all()
    return render_template('bill/detail.html', bill=bill, billdetails=billdetails)

# REST API
@bp.route('/<string:bill_cod>/gettotalvalue', methods=('POST','GET'))
def gettotalvalue(bill_cod):
    bills = db_session.query(BillHeader, func.sum(BillDetail.precio * BillDetail.cantidad).label('valortotal')).outerjoin(BillDetail, BillHeader.id == BillDetail.factura_id).outerjoin(Client, BillHeader.cliente_id == Client.id).filter(BillHeader.codigo == bill_cod).group_by(BillHeader.id).first()
    
    if bills is None:
        abort(404)
    
    return jsonify({'valortotal': bills.valortotal})