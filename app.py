from flask import Flask, session, request, redirect, url_for
from datetime import date
from db import init_app
from models import db, Reservation, Payment, Ticket, Train_Schedule  # Adjust imports to your actual models
from auth import auth_bp
from utils import render_page
from passenger import passenger_bp
from staff import staff_bp
from flask_sqlalchemy import SQLAlchemy
#Import your blueprints here:


app = Flask(__name__)
app.secret_key = 'some_secret_key'
init_app(app)

# Set your database URI and other configurations
with app.app_context():
    db.create_all()

# A function to render a base template with Bootstrap

@app.route('/')
def main_page():
    content = """
    <p>Welcome to the Train Reservation System!</p>
    <p><a href="/auth/login_passenger" class="btn btn-primary me-2">Login as Passenger</a>
    <a href="/auth/login_staff" class="btn btn-info me-2">Login as Staff</a>
    <a href="/auth/login_guest" class="btn btn-secondary">Continue as Guest</a></p>
    """
    return render_page("Welcome", content)

# Register your blueprints if you have them:
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(passenger_bp, url_prefix='/passenger')
app.register_blueprint(staff_bp, url_prefix='/staff')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    print("About to run the app...")
    app.run(debug=True)
