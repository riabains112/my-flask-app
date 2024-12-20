from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager
from flask_login import current_user
import os

# database is initialised 
db = SQLAlchemy()
DB_NAME = "helpdesk_database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'HBGHDW'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views 
    from .auth import auth 
    from .admin import admin  

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    # Database models imported
    from .models import User, Ticket
    
    with app.app_context():
        create_database(app)
        create_admin(app)

    # Using LoginManager for user authentication 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.context_processor
    def inject_user():
        return {'user': current_user}


    return app

from werkzeug.security import generate_password_hash

def create_admin(app):
    from .models import User
 # creating a default admin user if none exists
    with app.app_context():  
        # Check if an admin user already exists
        admin_user = User.query.filter_by(role='admin').first()

        if not admin_user:
            # create admin with secure password 
            admin_user = User(email="admin@example.com", password=generate_password_hash, full_name="Admin", role="admin")
            db.session.add(admin_user)
            db.session.commit()
            print("A default admin user has been created")
        else:
            print("An Admin user already exists in the database.")
            
def create_database(app):
    if not path.exists('website/' + DB_NAME):
       with app.app_context():
           db.create_all()
       print('Created Database!')