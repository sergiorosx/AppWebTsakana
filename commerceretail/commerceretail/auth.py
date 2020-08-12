import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from commerceretail.database import db_session
from commerceretail.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'El nombre de usuario es requerido.'
        elif not password:
            error = 'La Contraseña es requerida.'
        else:
            userRegistered = User.query.filter_by(username=username).first()
            if userRegistered is not None:
                error = '{} ya se encuentra registrado.'.format(username)

        if error is None:
            newUser = User(username, generate_password_hash(password))
            db_session.add(newUser)
            db_session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Ingrese un nombre de usuario.'
        elif not check_password_hash(user.password, password):
            error = 'Ingrese una contraseña.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        #if g.user is None:
        #    return redirect(url_for('auth.login'))

        #return view(**kwargs)
        """pull user info from the database based on session id"""

        g.user = None

        if 'user_id' in session:
            try:
                try:
                    g.user = User.query.get(session['user_id'])
                    return view(**kwargs)
                except TypeError:  # session probably expired
                    pass
            except KeyError:
                pass
        else:
            return redirect(url_for('auth.login'))

    return wrapped_view