from datetime import date
from utils import render_page
from flask import session, Blueprint, request
from models import Train_Schedule, Train, Station

staff_bp = Blueprint('staff', __name__, template_folder='templates')

@staff_bp.route('/dashboard')
def staff_dashboard():
    if session.get('role') == 'staff':
        content = """
        <p class="lead">Welcome Staff Member! Manage your admin functions:</p>
        <div class="list-group">
          <a href="/staff/edit_reservation_form" class="list-group-item list-group-item-action">Edit a Reservation</a>
          <a href="/staff/cancel_reservation_form" class="list-group-item list-group-item-action">Cancel a Reservation</a>
          <a href="/staff/assign_staff_form" class="list-group-item list-group-item-action">Assign Staff to Train</a>
          <a href="/staff/promote_waitlisted_form" class="list-group-item list-group-item-action">Promote Waitlisted Passenger</a>
          <a href="/staff/report/active_trains" class="list-group-item list-group-item-action">View Active Trains</a>
          <a href="/staff/report/stations_by_train" class="list-group-item list-group-item-action">View Stations by Train</a>
        </div>
        """
        return render_page("Staff Dashboard", content)
    else:
        return "Unauthorized", 403

@staff_bp.route('/edit_reservation_form')
def edit_reservation_form():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    content = """
    <h2>Edit a Reservation</h2>
    <form method="post" action="/staff/edit_reservation" class="mb-3">
      <div class="mb-3">
        <label for="reservation_id" class="form-label">Reservation ID</label>
        <input type="number" class="form-control" name="reservation_id" id="reservation_id" required>
      </div>
      <div class="mb-3">
        <label for="new_seat" class="form-label">New Seat</label>
        <input type="number" class="form-control" name="new_seat" id="new_seat" required>
      </div>
      <button type="submit" class="btn btn-primary">Update</button>
    </form>
    <a href="/staff/dashboard" class="btn btn-secondary">Back to Dashboard</a>
    """
    return render_page("Edit a Reservation", content)

@staff_bp.route('/edit_reservation', methods=['POST'])
def edit_reservation():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    reservation_id = request.form['reservation_id']
    new_seat = request.form['new_seat']
    # Mock editing, in real scenario, do db operation
    content = f"Reservation #{reservation_id} updated to seat {new_seat}.<br><a href='/staff/dashboard' class='btn btn-secondary mt-3'>Back to Dashboard</a>"
    return render_page("Edit Confirmation", content)

@staff_bp.route('/cancel_reservation_form')
def cancel_reservation_form():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    content = """
    <h2>Cancel a Reservation</h2>
    <form method="post" action="/staff/cancel_reservation" class="mb-3">
      <div class="mb-3">
        <label for="reservation_id" class="form-label">Reservation ID</label>
        <input type="number" class="form-control" name="reservation_id" id="reservation_id" required>
      </div>
      <button type="submit" class="btn btn-danger">Cancel</button>
    </form>
    <a href="/staff/dashboard" class="btn btn-secondary">Back to Dashboard</a>
    """
    return render_page("Cancel a Reservation", content)

@staff_bp.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    reservation_id = request.form['reservation_id']
    # Mock cancellation
    content = f"Reservation #{reservation_id} cancelled.<br><a href='/staff/dashboard' class='btn btn-secondary mt-3'>Back to Dashboard</a>"
    return render_page("Cancellation Confirmation", content)

@staff_bp.route('/assign_staff_form')
def assign_staff_form():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    content = """
    <h2>Assign Staff to Train</h2>
    <form method="post" action="/staff/assign_staff" class="mb-3">
      <div class="mb-3">
        <label for="staff_id" class="form-label">Staff ID</label>
        <input type="number" class="form-control" name="staff_id" id="staff_id" required>
      </div>
      <div class="mb-3">
        <label for="schedule_id" class="form-label">Schedule ID</label>
        <input type="number" class="form-control" name="schedule_id" id="schedule_id" required>
      </div>
      <button type="submit" class="btn btn-primary">Assign</button>
    </form>
    <a href="/staff/dashboard" class="btn btn-secondary">Back to Dashboard</a>
    """
    return render_page("Assign Staff", content)

@staff_bp.route('/assign_staff', methods=['POST'])
def assign_staff():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    staff_id = request.form['staff_id']
    schedule_id = request.form['schedule_id']
    # Mock assign
    content = f"Assigned staff {staff_id} to schedule {schedule_id}.<br><a href='/staff/dashboard' class='btn btn-secondary mt-3'>Back to Dashboard</a>"
    return render_page("Assignment Confirmation", content)

@staff_bp.route('/promote_waitlisted_form')
def promote_waitlisted_form():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    content = """
    <h2>Promote Waitlisted Passenger</h2>
    <p>For demonstration, just click promote:</p>
    <form method="post" action="/staff/promote_waitlisted">
      <button type="submit" class="btn btn-success">Promote</button>
    </form>
    <a href="/staff/dashboard" class="btn btn-secondary mt-3">Back to Dashboard</a>
    """
    return render_page("Promote Waitlisted Passenger", content)

@staff_bp.route('/promote_waitlisted', methods=['POST'])
def promote_waitlisted():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    # Mock promotion
    content = "Promoted a waitlisted passenger.<br><a href='/staff/dashboard' class='btn btn-secondary mt-3'>Back to Dashboard</a>"
    return render_page("Promotion Confirmation", content)


@staff_bp.route('/report/active_trains')
def active_trains():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    today = date.today()
    active_schedules = Train_Schedule.query.filter(Train_Schedule.Date == today).all()

    rows = ""
    for schedule in active_schedules:
        rows += f"<tr><td>{schedule.Schedule_ID}</td><td>{schedule.train.EName}-{schedule.train.AName}</td><td>{schedule.Date}</td></tr>"

    content = f"""
    <p class="lead">Trains active on {today}:</p>
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
    <a href="/staff/dashboard" class="btn btn-secondary mt-3">Back to Dashboard</a>
    """
    return render_page("Active Trains", content)


@staff_bp.route('/report/stations_by_train')
def stations_by_train():
    if session.get('role') != 'staff':
        return "Unauthorized", 403
    trains = Train.query.all()

    content = "<p class='lead'>Stations by Train:</p>"
    for train in trains:
        content += f"<h4>{train.EName}-{train.AName}</h4>"
        stations = Station.query.filter(Station.Seq_Num.in_([route.Sequence_Number for route in train.routes])).all()
        if stations:
            content += "<ul>"
            for station in stations:
                content += f"<li>{station.Station_Name} - {station.City}</li>"
            content += "</ul>"
        else:
            content += "<p>No stations found for this train.</p>"

    content += "<a href='/staff/dashboard' class='btn btn-secondary mt-3'>Back to Dashboard</a>"
    return render_page("Stations by Train", content)
