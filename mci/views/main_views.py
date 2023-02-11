from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/intro')
def intro():
    return render_template('0_intro.html')

@bp.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@bp.route('/abouttest')
def abouttest():
    return render_template('abouttest.html')