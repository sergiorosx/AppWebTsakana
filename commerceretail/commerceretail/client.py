import io
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file
)
from sqlalchemy import func, desc
from werkzeug.exceptions import abort
from commerceretail.auth import login_required
from commerceretail.database import db_session
from commerceretail.models import Client
from commerceretail.models import BillHeader
from commerceretail.models import BillDetail

bp = Blueprint('client', __name__, url_prefix='/client')

@bp.route('/')
@login_required
def index():
    clients = db_session.query(Client, func.count(BillDetail.id).label('compras')).outerjoin(BillHeader, Client.id == BillHeader.cliente_id).outerjoin(BillDetail, BillHeader.id == BillDetail.factura_id).group_by(BillHeader.id).order_by(desc(func.count(BillDetail.id))).all()
    print(clients)
    return render_template('client/index.html', clients = clients)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        foto = request.files['foto'].read()
        size = len(foto)
        error = None

        if not cedula:
            error = 'Debe ingresar la cédula.'
        elif not nombre:
            error = 'Debe ingresar el nombre.'
        elif not direccion:
            error = 'Debe ingresar la dirección.'
        elif not telefono:
            error = 'Debe ingresar el teléfono.'
        elif size <= 0:
            error = 'Debe seleccionar una foto.'
            
        # client validation
        clientRegistered = Client.query.filter_by(cedula=cedula).first()
        if clientRegistered is not None:
            error = 'El cliente {} ya se encuentra registrado.'.format(cedula)

        if error is not None:
            flash(error)
        else:
            newClient = Client(cedula, nombre, direccion, telefono, foto)
            db_session.add(newClient)
            db_session.commit()
            return redirect(url_for('client.index'))

    return render_template('client/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    client = Client.query.filter_by(id=id).first()

    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        foto = request.files['foto'].read()
        size = len(foto)
        error = None

        if not cedula:
            error = 'Debe ingresar la cédula.'
        elif not nombre:
            error = 'Debe ingresar el nombre.'
        elif not direccion:
            error = 'Debe ingresar la dirección.'
        elif not telefono:
            error = 'Debe ingresar el teléfono.'
        
        if error is not None:
            flash(error)
        else:
            client.cedula = cedula
            client.nombre = nombre
            client.direccion = direccion
            client.telefono = telefono
            if size > 0:
                client.foto = foto
            db_session.commit()
            return redirect(url_for('client.index'))
    return render_template('client/update.html', client=client)

@bp.route('/<int:id>/showimg', methods=['GET'])
def showimg(id):
    client = Client.query.filter_by(id=id).first()
    return send_file(
                io.BytesIO(client.foto),
                attachment_filename='foto.jpeg',
                mimetype='image/jpg'
               )

@bp.route('/<int:id>/delete', methods=('POST','GET'))
@login_required
def delete(id):
    client = Client.query.filter_by(id=id).first()
    db_session.delete(client)
    db_session.commit()
    return redirect(url_for('client.index'))