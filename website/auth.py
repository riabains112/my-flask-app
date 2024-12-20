from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth' , __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                 # Successful login
                flash('Log in successfull!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!! Please try again.', category='error')
        else:
            flash('No Account has been found with this email!! It does not exist.', category='error')
    return render_template("login.html", boolean=True)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullname', "").strip()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account with this email already exists.', category='error')
        elif len(email) < 4 or "@" not in email or "." not in email:
            flash('Invalid email address. Please enter a valid email.', category='error')
        elif not full_name or len(full_name) < 2:
            flash('Full name must be greater than 2 character long.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters long', category='error')
        else:
            new_user = User(email=email, full_name=full_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            # Automatically log in the new user
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Log out successfull.', category='info')
    return redirect(url_for('auth.login'))
