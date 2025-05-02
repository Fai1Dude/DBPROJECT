from flask import Blueprint, session

from utils import render_page

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login_passenger')
def login_passenger():
    # Mock login as passenger
    session['role'] = 'passenger'
    session['user_id'] = 1
    return render_page("Login", "<p>You are logged in as passenger. <a href='/passenger/dashboard'>Go to dashboard</a></p>")

@auth_bp.route('/login_staff')
def login_staff():
    # Mock login as staff
    session['role'] = 'staff'
    session['user_id'] = 100
    return render_page("Login", "<p>You are logged in as staff. <a href='/staff/dashboard'>Go to dashboard</a></p>")

@auth_bp.route('/login_guest')
def login_guest():
    # Mock login as guest
    session['role'] = 'guest'
    session['user_id'] = 'Guest1'
    return render_page("Login", "<p>You are logged in as guest. <a href='/passenger/dashboard'>Go to dashboard</a></p>")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return render_page("Logout", "<p>You have been logged out. <a href='/'>Main Page</a></p>")
