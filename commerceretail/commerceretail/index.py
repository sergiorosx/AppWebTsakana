from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from commerceretail.auth import login_required

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index/index.html')