from flask import Blueprint, request, flash, render_template

from project import db
from project.blueprints.auth_blueprint import only_anonymous, login_required
from project.model.user import User

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
@only_anonymous
def register():
    if request.method == 'POST':
        # Get params
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        # Check password
        if password != password_confirm:
            flash('Password does not match', 'danger')
            return render_template('user/register.html')
        # Checks integrity
        if User.find_one({'email': email, 'enabled': True}) is None:
            # Creates user
            user = User(email=email, first_name=first_name, last_name=last_name)
            user.hash_password(password)
            user.create()
            # Persists it
            db.session.commit()
        else:
            flash('The email is not available', 'danger')
    return render_template('user/register.html')


@user_blueprint.route('/retrieve-password', methods=['GET', 'POST'])
@only_anonymous
def retrieve_password():
    pass


@user_blueprint.route('/update-password', methods=['GET', 'POST'])
@login_required
def update_password():
    pass
