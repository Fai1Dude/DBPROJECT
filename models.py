from datetime import datetime, date, time
from db import db

class Staff_Duty(db.Model):
    __tablename__ = 'Staff_Duty'
    DType = db.Column(db.String(50), primary_key=True)
    Ticketing_staff = db.Column(db.Boolean)
    Train_Driver = db.Column(db.Boolean)
    Booking_staff = db.Column(db.Boolean)

class Train(db.Model):
    __tablename__ = 'Train'
    Train_ID = db.Column(db.Integer, primary_key=True)
    EName = db.Column(db.String(100))
    AName = db.Column(db.String(100))

class Staff(db.Model):
    __tablename__ = 'Staff'
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Train_ID = db.Column(db.Integer, db.ForeignKey('Train.Train_ID'))
    StaffFname = db.Column(db.String(50))
    StaffLname = db.Column(db.String(50))
    Staff_Email = db.Column(db.String(100))
    Staff_phone = db.Column(db.String(15))
    DType = db.Column(db.String(50), db.ForeignKey('Staff_Duty.DType'))

    train = db.relationship("Train", backref="staff")
    duty = db.relationship("Staff_Duty", backref="staff")

class Train_Schedule(db.Model):
    __tablename__ = 'Train_Schedule'
    Schedule_ID = db.Column(db.Integer, primary_key=True)
    Train_ID = db.Column(db.Integer, db.ForeignKey('Train.Train_ID'))
    Seq_Num = db.Column(db.Integer)
    Arrival_Time = db.Column(db.Time)
    Trip_Time = db.Column(db.Time)
    Departure_Time = db.Column(db.Time)
    Date = db.Column(db.Date)

    train = db.relationship("Train", backref="schedules")

class Route(db.Model):
    __tablename__ = 'Route'
    Sequence_Number = db.Column(db.Integer, primary_key=True)
    Train_ID = db.Column(db.Integer, db.ForeignKey('Train.Train_ID'))
    Railway = db.Column(db.String(100))

    train = db.relationship("Train", backref="routes")

class Station(db.Model):
    __tablename__ = 'Station'
    Station_ID = db.Column(db.Integer, primary_key=True)
    City = db.Column(db.String(100))
    Seq_Num = db.Column(db.Integer)
    Station_Name = db.Column(db.String(100))

class PassgHist(db.Model):
    __tablename__ = 'PassgHist'
    TotalRailway = db.Column(db.Integer, primary_key=True)
    Seq_Num = db.Column(db.Integer)

class Reservation(db.Model):
    __tablename__ = 'Reservation'
    Reservation_Num = db.Column(db.Integer, primary_key=True)
    Schedule_ID = db.Column(db.Integer, db.ForeignKey('Train_Schedule.Schedule_ID'))
    Passenger_ID = db.Column(db.Integer)
    Seat_Number = db.Column(db.Integer)
    Coach = db.Column(db.String(50))

    schedule = db.relationship("Train_Schedule", backref="reservations")


class Registered_Passenger(db.Model):
    __tablename__ = 'Registered_Passenger'
    Passenger_ID = db.Column(db.Integer, primary_key=True)
    Passenger_Name = db.Column(db.String(100))
    TotalRailway = db.Column(db.Integer, db.ForeignKey('PassgHist.TotalRailway'))
    Phone = db.Column(db.String(15))

    history = db.relationship("PassgHist", backref="passengers")


class Unregistered_Passenger(db.Model):
    __tablename__ = 'Unregistered_Passenger'
    Passenger_ID = db.Column(db.Integer, primary_key=True)
    Passenger_Name = db.Column(db.String(100))
    Phone = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    Created_At = db.Column(db.DateTime, default=datetime.utcnow)

class Identification_Document(db.Model):
    __tablename__ = 'Identification_Document'
    IdentifyingGovDocs = db.Column(db.String(100), primary_key=True)
    Passenger_ID = db.Column(db.Integer, db.ForeignKey('Registered_Passenger.Passenger_ID'))

class Dependent(db.Model):
    __tablename__ = 'Dependent'
    Dependent_ID = db.Column(db.Integer, primary_key=True)
    Passenger_ID = db.Column(db.Integer, db.ForeignKey('Registered_Passenger.Passenger_ID'))
    Dependent_Name = db.Column(db.String(100))
    Relation = db.Column(db.String(50))

class Discounted(db.Model):
    __tablename__ = 'Discounted'
    Dependent_DEF = db.Column(db.Integer, primary_key=True)
    Discount_Amount = db.Column(db.Numeric(10,2))
    Booking_ID = db.Column(db.Integer) # Not linked due to original schema constraints

class Loyalty_Miles(db.Model):
    __tablename__ = 'Loyalty_Miles'
    Passenger_ID = db.Column(db.Integer, db.ForeignKey('Registered_Passenger.Passenger_ID'), primary_key=True)
    Discount_Amount = db.Column(db.Numeric(10,2))
    Classtype = db.Column(db.String(50))

class Payment(db.Model):
    __tablename__ = 'Payment'
    Payment_ID = db.Column(db.Integer, primary_key=True)
    Payment_Amount = db.Column(db.Numeric(10,2))
    VAT_Amount = db.Column(db.Numeric(10,2))

class Ticket(db.Model):
    __tablename__ = 'Ticket'
    Booking_ID = db.Column(db.Integer, primary_key=True)
    Reservation_Num = db.Column(db.Integer, db.ForeignKey('Reservation.Reservation_Num'))
    Payment_ID = db.Column(db.Integer, db.ForeignKey('Payment.Payment_ID'))
    Seat_Number = db.Column(db.Integer)

    reservation = db.relationship("Reservation", backref="tickets")
    payment = db.relationship("Payment", backref="tickets")

class Waiting_List(db.Model):
    __tablename__ = 'Waiting_List'
    Waiting_ID = db.Column(db.Integer, primary_key=True)
    Reservation_Num = db.Column(db.Integer, db.ForeignKey('Reservation.Reservation_Num'))
    Booking_ID = db.Column(db.Integer, db.ForeignKey('Ticket.Booking_ID'))
    Payment_ID = db.Column(db.Integer, db.ForeignKey('Payment.Payment_ID'))
    Reservation_Date = db.Column(db.Date)
    Cancellation_Charge = db.Column(db.Numeric(10,2))
