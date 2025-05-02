# Train Reservation System (Flask + MySQL)
A lightweight demonstration web app that lets passengers search trains, book seats, and view reservations, while staff can manage bookings and run simple operational reports.
Built with Python 3 / Flask / SQLAlchemy / MySQL and styled with Bootstrap 5.

# ✨ Key features
Role-based sessions – mock login for passenger, staff, or guest via /auth/* routes.

Passenger workflow

Search schedules by date, book a seat, pay, and see your tickets.

Staff dashboard

Edit / cancel reservations, assign crew, promote wait-listed passengers, and view live reports (active trains today, stations by train).

Relational schema – 20 + inter-related tables mapped with SQLAlchemy models. 


Bootstrap templates rendered by helper render_page() for quick, responsive UI. 


Seed SQL scripts (ICS321TABLES.sql, ICS321Triggers.sql, DBDATA.sql) to create tables, triggers, and demo data.

# 🗄️ Tech stack
Layer	Library / Tool
Backend	Python 3.x, Flask, Flask-SQLAlchemy
DB	MySQL 8 / MariaDB (mysql+pymysql driver)
Front-end	HTML + Bootstrap 5
ORM models	Defined in models.py

# ⚙️ Local setup
Clone the repo

bash
Copy code
git clone https://github.com/<you>/TrainReservation.git
cd TrainReservation
Create a virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
Install dependencies

bash
Copy code
pip install flask flask-sqlalchemy pymysql
(Optionally export a requirements.txt later with pip freeze > requirements.txt.)

Configure MySQL

bash
Copy code
mysql -u root -p
CREATE DATABASE train_reservation_db;
USE train_reservation_db;
SOURCE ICS321TABLES.sql;
SOURCE ICS321Triggers.sql;
SOURCE DBDATA.sql;
Edit the DB URI

The default URI in db.py is:

python
Copy code
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1212@localhost/train_reservation_db'
Change root:1212@localhost to match your MySQL credentials/host. 


Tip: set DATABASE_URL in your shell and read it in db.py to avoid hard-coding passwords.

Run the server

bash
Copy code
python app.py
or: flask --app app run --debug
Visit http://127.0.0.1:5000/.

# 🏃‍♂️ Quick tour
URL	Description
/	Landing page with links to log in as Passenger, Staff, or continue as Guest. 

/auth/login_passenger	Creates a session with role passenger (user id = 1).
/auth/login_staff	Role staff (user id = 100).
/passenger/dashboard	Passenger menu: search trains, book seat, view reservations.
/staff/dashboard	Staff admin panel with management/report links.

All sessions are mocked for demo purposes—there is no password logic yet. Log out anytime via /auth/logout.

# 🧬 Project structure
graphql
Copy code
.
├─ app.py               # App factory & blueprint registration
├─ auth.py              # Simple login/logout routes
├─ passenger.py         # Passenger UI & actions
├─ staff.py             # Staff admin UI & actions
├─ models.py            # SQLAlchemy table mappings
├─ db.py                # DB init & URI
├─ utils.py             # Shared HTML template helper
├─ ICS321TABLES.sql     # CREATE TABLE statements
├─ ICS321Triggers.sql   # Triggers for business rules
└─ DBDATA.sql           # Sample data

# 🛠️ Extending the app
Replace the mock logins with real authentication (Flask-Login, JWT, or OAuth).

Add seat-availability checks before booking.

Implement proper error handling & input validation.

Containerise with Docker and use environment variables for secrets.

Write unit tests with pytest and a SQLite in-memory DB.

# 📜 License
This project is released for educational purposes under the KFUPM License. Feel free to fork, improve, and share!

# 🙋‍♀️ Support / questions
Open an issue on the repository or contact Faisal at FaisalAlhmedi@hotmail.com. Pull requests are welcome!
