from flask import Blueprint, render_template, request, session, flash, url_for
from werkzeug.utils import redirect

from project import db
from project.blueprints.auth_blueprint import login_required
from project.model.user import User

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/profile', methods=['GET'])
@login_required
def details():
    return render_template('profile/details.html', current_user=User.find_one({'id': session.get('user_id')}))


@profile_blueprint.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def update_details():
    current_user = User.find_one({'id': session.get('user_id')})
    if request.method == 'POST':
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        if email == current_user.email or User.is_email_available(email):
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            current_user.update()
            session['user_name'] = first_name
            db.session.commit()
            return redirect(url_for('profile.details'))
        else:
            flash('Email is not available', 'error')
    return render_template('profile/edit.html', current_user=current_user)


@profile_blueprint.route('/profile/password', methods=['GET', 'POST'])
@login_required
def update_password():
    if request.method == 'POST':
        if request.form.get("password") == request.form.get("password_confirm"):
            current_user = User.find_one({'id': session.get('user_id')})
            current_user.hash_password(request.form.get("password"))
            current_user.update()
            db.session.commit()
            flash('Password updated', 'error')
            return redirect(url_for('profile.details'))
        else:
            flash('Password does not match', 'error')
            return redirect(url_for('profile.update_password'))
    return render_template('profile/edit_password.html')


@profile_blueprint.route('/profile', methods=['POST'])
@login_required
def delete():
    current_user = User.find_one({'id': session.get('user_id')})
    current_user.soft_delete()
    session.clear()
    db.session.commit()
    flash('Yout account has been delete', 'info')
    return redirect(url_for('home.list_publish_articles'))
