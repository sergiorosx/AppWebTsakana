from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from commerceretail.auth import login_required
from commerceretail.database import db_session
from commerceretail.models import Product
from commerceretail.models import Category

bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route('/')
@login_required
def index():
    products = Product.query.filter_by(estado=True).all()
    return render_template('product/index.html', products = products)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    categories = Category.query.all()

    if request.method == 'POST':
        
        codigo = request.form['codigo']
        categoria_id = request.form['categoria_id']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad_en_bodega = request.form['cantidad_en_bodega']
        if request.form['estado'] == "True":
            estado = True
        else:
            estado = False

        error = None
        
        if not codigo:
            error = 'Debe ingresar el código del producto.'
        elif not categoria_id:
            error = 'Debe seleccionar la categoría del producto.'
        elif not nombre:
            error = 'Debe ingresar el nombre.'
        elif not precio:
            error = 'Debe ingresar el precio.'
        elif not cantidad_en_bodega:
            error = 'Debe seleccionar la cantidad disponible en bodega.'
        elif not estado:
            error = 'Debe seleccionar un estado.'
        
        # client validation
        productRegistered = Product.query.filter_by(codigo=codigo).first()
        if productRegistered is not None:
            error = 'El producto {} ya se encuentra registrado.'.format(codigo)

        if error is not None:
            flash(error)
        else:
            newProduct = Product(codigo, categoria_id, nombre, precio, cantidad_en_bodega, estado)
            db_session.add(newProduct)
            db_session.commit()
            return redirect(url_for('product.index'))

    return render_template('product/create.html', categories = categories)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    product = Product.query.filter_by(id=id).first()
    categories = Category.query.all()

    if request.method == 'POST':
        codigo = request.form['codigo']
        categoria_id = request.form['categoria_id']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad_en_bodega = request.form['cantidad_en_bodega']
        if request.form['estado'] == "True":
            estado = True
        else:
            estado = False
        
        error = None

        if not codigo:
            error = 'Debe ingresar el código del producto.'
        elif not categoria_id:
            error = 'Debe seleccionar la categoría del producto.'
        elif not nombre:
            error = 'Debe ingresar el nombre.'
        elif not precio:
            error = 'Debe ingresar el precio.'
        elif not cantidad_en_bodega:
            error = 'Debe seleccionar la cantidad disponible en bodega.'
        elif not estado:
            error = 'Debe seleccionar un estado.'
        
        if error is not None:
            flash(error)
        else:
            product.codigo = codigo
            product.categoria_id = categoria_id
            product.nombre = nombre
            product.precio = precio
            product.cantidad_en_bodega = cantidad_en_bodega
            db_session.commit()
            return redirect(url_for('product.index'))
    return render_template('product/update.html', product=product, categories = Category.query.all())


@bp.route('/<int:id>/delete', methods=('POST','GET'))
@login_required
def delete(id):
    product = Product.query.filter_by(id=id).first()
    product.estado = False
    db_session.commit()
    return redirect(url_for('product.index'))