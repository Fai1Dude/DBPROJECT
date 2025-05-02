from flask import Blueprint, request, session, url_for, redirect
from models import Train_Schedule, Reservation, Payment, Ticket, db,Unregistered_Passenger

passenger_bp = Blueprint('passenger', __name__, template_folder='templates')

# A function to render a base template with Bootstrap
def render_page(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{title}</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    </head>
    <body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Train Reservation System</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor"
          aria-controls="navbarColor" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarColor">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="/">Main Page</a></li>
            <li class="nav-item"><a class="nav-link" href="/auth/logout">Logout</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container my-4">
      <h1 class="mb-4">{title}</h1>
      {content}
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

@passenger_bp.route('/dashboard')
def dashboard():
    role = session.get('role')
    if role == 'passenger':
        content = """
        <p class="lead">Welcome Passenger! You can search for trains, book seats, and view your reservations.</p>
        <div class="list-group">
          <a href="/passenger/search_trains_form" class="list-group-item list-group-item-action">Search for Trains</a>
          <a href="/passenger/book_form" class="list-group-item list-group-item-action">Book a Seat</a>
          <a href="/passenger/report/reservations" class="list-group-item list-group-item-action">View My Reservations</a>
        </div>
        """
        return render_page("Passenger Dashboard", content)
    elif role == 'guest':
        content = """
        <p class="lead">Welcome Guest! You can search for trains and book seats as 'Guest1'.</p>
        <div class="list-group">
          <a href="/passenger/search_trains_form" class="list-group-item list-group-item-action">Search for Trains</a>
          <a href="/passenger/book_form" class="list-group-item list-group-item-action">Book a Seat</a>
        </div>
        """
        return render_page("Guest Dashboard", content)
    else:
        return "Unauthorized", 403

@passenger_bp.route('/search_trains_form')
def search_trains_form():
    if session.get('role') not in ['passenger', 'guest']:
        return "Unauthorized", 403
    content = """
    <form method="post" action="/passenger/search_trains" class="mb-3">
        <div class="mb-3">
          <label for="date" class="form-label">Date (YYYY-MM-DD)</label>
          <input type="text" class="form-control" name="date" id="date" placeholder="2024-12-08" required>
        </div>
        <button type="submit" class="btn btn-primary">Search</button>
    </form>
    <a href="/passenger/dashboard" class="btn btn-secondary">Back to Dashboard</a>
    """
    return render_page("Search for Trains", content)

@passenger_bp.route('/search_trains', methods=['POST'])
def search_trains():
    if session.get('role') not in ['passenger', 'guest']:
        return "Unauthorized", 403
    search_date = request.form['date'].strip()
    schedules = Train_Schedule.query.filter_by(Date=search_date).all()
    if schedules:
        rows = ""
        for s in schedules:
            rows += f"<tr><td>{s.Schedule_ID}</td><td>{s.train.EName}-{s.train.AName}</td><td>{s.Date}</td></tr>"
        content = f"""
        <p class="lead">Trains on {search_date}:</p>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Schedule ID</th>
              <th>Train</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        """
    else:
        content = f"<p class='lead'>No trains found for {search_date}.</p>"
    content += "<a href='/passenger/dashboard' class='btn btn-secondary mt-3'>Back to Dashboard</a>"
    return render_page("Search Results", content)

@passenger_bp.route('/book_form')
def book_form():
    if session.get('role') not in ['passenger', 'guest']:
        return "Unauthorized", 403
    content = """
    <form method="post" action="/passenger/book" class="mb-3">
        <div class="mb-3">
          <label for="schedule_id" class="form-label">Schedule ID</label>
          <input type="number" class="form-control" name="schedule_id" id="schedule_id" required>
        </div>
        <div class="mb-3">
          <label for="seat_number" class="form-label">Seat Number</label>
          <input type="number" class="form-control" name="seat_number" id="seat_number" required>
        </div>
        <button type="submit" class="btn btn-success">Book</button>
    </form>
    <a href="/passenger/dashboard" class="btn btn-secondary">Back to Dashboard</a>
    """
    return render_page("Book a Seat", content)

@passenger_bp.route('/book', methods=['POST'])
def book():
    if session.get('role') not in ['passenger', 'guest']:
        return "Unauthorized", 403

    schedule_id = request.form.get('schedule_id')
    seat_number = request.form.get('seat_number')
    role = session.get('role')
    if role == 'guest':
        # Create a new unregistered passenger
        guest_passenger = Unregistered_Passenger(Passenger_Name='Guest', Email='guest@example.com', Phone='')
        db.session.add(guest_passenger)
        db.session.commit()
        passenger_id = guest_passenger.Passenger_ID
    else:
        passenger_id = session.get('user_id')

    reservation = Reservation(Schedule_ID=schedule_id, Passenger_ID=passenger_id, Seat_Number=seat_number, Coach='A')
    db.session.add(reservation)
    db.session.commit()

    payment = Payment(Payment_Amount=100.00, VAT_Amount=15.00)
    db.session.add(payment)
    db.session.commit()

    ticket = Ticket(Reservation_Num=reservation.Reservation_Num, Payment_ID=payment.Payment_ID, Seat_Number=seat_number)
    db.session.add(ticket)
    db.session.commit()

    content = f"""
    <p class="lead">Booked successfully!</p>
    <p>Reservation #{reservation.Reservation_Num}, Ticket #{ticket.Booking_ID}</p>
    <a href="/passenger/dashboard" class="btn btn-secondary">Back to Dashboard</a>
    """
    return render_page("Booking Confirmation", content)

@passenger_bp.route('/report/reservations')
def passenger_reservations():
    if session.get('role') not in ['passenger', 'guest']:
        return "Unauthorized", 403
    role = session.get('role')
    passenger_id = session.get('user_id') if role == 'passenger' else 0

    my_reservations = Reservation.query.filter_by(Passenger_ID=passenger_id).all()
    if my_reservations:
        rows = ""
        for r in my_reservations:
            rows += f"<tr><td>{r.Reservation_Num}</td><td>{r.Schedule_ID}</td><td>{r.Seat_Number}</td><td>{r.Coach}</td></tr>"
        content = """
        <p class="lead">Your Reservations:</p>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Reservation #</th>
              <th>Schedule ID</th>
              <th>Seat</th>
              <th>Coach</th>
            </tr>
          </thead>
          <tbody>
        """ + rows + "</tbody></table>"
    else:
        content = "<p class='lead'>You have no reservations.</p>"

    content += "<a href='/passenger/dashboard' class='btn btn-secondary mt-3'>Back to Dashboard</a>"
    return render_page("My Reservations", content)
