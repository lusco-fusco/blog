import functools

from flask import Blueprint, request, render_template, session, url_for, flash
from werkzeug.utils import redirect

from project.model.user import User

auth_blueprint = Blueprint('auth', __name__)


# --------------------------------
# Decorators for user control
# --------------------------------
def only_anonymous(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in') is None:
            return fn(*args, **kwargs)
        return redirect(url_for('home.all_articles'))
    return inner


def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('home.all_articles', next=request.path))
    return inner


def admin_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('is_admin'):
            return fn(*args, **kwargs)
        return redirect(url_for('home.all_articles'))
    return inner

# --------------------------------
# Auth blueprints
# --------------------------------
@auth_blueprint.route('/login', methods=['GET', 'POST'])
@only_anonymous
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('email') and request.form.get('password'):
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.find_one({'email': email, 'enabled': True})
        if user.verify_password(password):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['user_name'] = user.first_name
            session.permanent = True    # TODO: Use cookie to store session.
            # session.set_cookie('user_id', user.id)
            session['is_admin'] = user.is_admin()
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('home.all_articles'))
        else:
            flash('Incorrect email or password.', 'danger')
    return render_template('auth/login.html', next_url=next_url)


@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home.all_articles'))
