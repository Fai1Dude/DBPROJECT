-- Insert Staff Duty types
INSERT INTO Staff_Duty (DType, Ticketing_staff, Train_Driver, Booking_staff) VALUES
('Train Driver', false, true, false),
('Ticket Officer', true, false, false),
('Booking Agent', false, false, true),
('Multi-Role Agent', true, false, true);

-- Insert Trains
INSERT INTO Train (EName, AName, capacity) VALUES
('Express 101', 'Thunder Rail', 200),
('Local 202', 'City Commuter', 150),
('Rapid 303', 'Lightning Express', 180),
('Metro 404', 'Urban Connect', 120);

-- Insert Staff members
INSERT INTO Staff (Train_ID, StaffFname, StaffLname, Staff_Email, Staff_phone, DType) VALUES
(1, 'John', 'Smith', 'john.smith@rail.com', '555-0101', 'Train Driver'),
(1, 'Mary', 'Johnson', 'mary.j@rail.com', '555-0102', 'Ticket Officer'),
(2, 'Robert', 'Brown', 'robert.b@rail.com', '555-0103', 'Train Driver'),
(2, 'Sarah', 'Davis', 'sarah.d@rail.com', '555-0104', 'Booking Agent');

-- Insert Train Schedules
INSERT INTO Train_Schedule (Train_ID, Seq_Num, Arrival_Time, Trip_Time, Departure_Time, Date, Status, Available_Seats) VALUES
(1, 1, '08:00:00', '02:00:00', '10:00:00', '2024-12-14', 'Scheduled', 180),
(1, 2, '14:00:00', '02:30:00', '16:30:00', '2024-12-14', 'Scheduled', 150),
(2, 1, '09:30:00', '01:30:00', '11:00:00', '2024-12-14', 'Scheduled', 120),
(3, 1, '11:00:00', '03:00:00', '14:00:00', '2024-12-14', 'Scheduled', 160);

-- Insert Routes
INSERT INTO Route (Train_ID, Railway) VALUES
(1, 'North Line'),
(1, 'South Express'),
(2, 'City Circle'),
(3, 'Coast Route');

-- Insert Stations
INSERT INTO Station (City, Seq_Num, Station_Name) VALUES
('New York', 1, 'Central Station'),
('Boston', 2, 'South Station'),
('Philadelphia', 3, 'Market East'),
('Washington', 4, 'Union Station');

-- Insert Passenger History
INSERT INTO PassgHist (Seq_Num, Transaction_Date) VALUES
(1, '2024-12-13 09:00:00'),
(2, '2024-12-13 10:30:00'),
(3, '2024-12-13 11:45:00'),
(4, '2024-12-13 13:15:00');

-- Insert Registered Passengers
INSERT INTO Registered_Passenger (Passenger_Name, Email, Phone, TotalRailway) VALUES
('Alice Wilson', 'alice.w@email.com', '555-0201', 1),
('Bob Anderson', 'bob.a@email.com', '555-0202', 2),
('Carol Martinez', 'carol.m@email.com', '555-0203', 3),
('David Thompson', 'david.t@email.com', '555-0204', 4);

-- Insert Reservations
INSERT INTO Reservation (Schedule_ID, Passenger_ID, Seat_Number, Coach, Status) VALUES
(1, 1, 'A1', 'First Class', 'Confirmed'),
(1, 2, 'B3', 'Business', 'Confirmed'),
(2, 3, 'C4', 'Economy', 'Confirmed'),
(3, 4, 'D2', 'First Class', 'Confirmed');

-- Insert Payments
INSERT INTO Payment (Reservation_Num, Payment_Amount, VAT_Amount, Status) VALUES
(1, 150.00, 15.00, 'Completed'),
(2, 120.00, 12.00, 'Completed'),
(3, 80.00, 8.00, 'Completed'),
(4, 200.00, 20.00, 'Completed');

-- Insert Loyalty Miles
INSERT INTO Loyalty_Miles (Passenger_ID, Miles, Tier, Discount_Amount) VALUES
(1, 5000, 'Gold', 15.00),
(2, 3000, 'Silver', 10.00),
(3, 1000, 'Bronze', 5.00),
(4, 500, 'Standard', 0.00);

-- Insert Notification Queue
INSERT INTO Notification_Queue (Passenger_ID, Type, Message, Status) VALUES
(1, 'Departure Alert', 'Your train departs in 2 hours', 'Pending'),
(2, 'Booking Confirmation', 'Your booking has been confirmed', 'Sent'),
(3, 'Payment Reminder', 'Payment due for your recent booking', 'Pending'),
(4, 'Schedule Change', 'Your train schedule has been updated', 'Pending');

-- Insert Waiting List
INSERT INTO Waiting_List (Schedule_ID, Passenger_ID, Status) VALUES
(1, 3, 'Waiting'),
(2, 4, 'Waiting'),
(3, 1, 'Notified'),
(4, 2, 'Cancelled');
-- Insert Dependent data
INSERT INTO Dependent (Passenger_ID, Dependent_Name, Relationship, Age) VALUES
(1, 'Emma Wilson', 'Child', 12),
(1, 'James Wilson', 'Child', 8),
(2, 'Sophie Anderson', 'Spouse', 35),
(3, 'Lucas Martinez', 'Child', 15),
(3, 'Isabella Martinez', 'Child', 10),
(4, 'Oliver Thompson', 'Child', 6);

-- Insert Staff Assignment data
INSERT INTO Staff_Assignment (Staff_ID, Train_ID, Assignment_Date, Status) VALUES
(1, 1, '2024-12-14', 'Assigned'), -- John Smith assigned to Express 101
(2, 1, '2024-12-14', 'Assigned'), -- Mary Johnson assigned to Express 101
(3, 2, '2024-12-14', 'Assigned'), -- Robert Brown assigned to Local 202
(4, 2, '2024-12-14', 'Assigned'), -- Sarah Davis assigned to Local 202
(1, 3, '2024-12-15', 'Assigned'), -- John Smith assigned to Rapid 303 next day
(2, 4, '2024-12-15', 'Assigned'), -- Mary Johnson assigned to Metro 404 next day
(3, 1, '2024-12-15', 'Pending'), -- Robert Brown pending assignment to Express 101
(4, 3, '2024-12-15', 'Pending'); -- Sarah Davis pending assignment to Rapid 303