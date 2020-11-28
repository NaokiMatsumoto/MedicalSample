from datetime import datetime

from flask import (
    Blueprint, abort, request, render_template,
    redirect, url_for, flash, session, jsonify
)
# from medical import db


bp = Blueprint('medical', __name__, url_prefix='')

@bp.route('/')
def home():
    return render_template(
        'home.html'
    )
