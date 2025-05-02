DROP DATABASE IF EXISTS train_reservation_db;
CREATE DATABASE train_reservation_db;
USE train_reservation_db;

CREATE TABLE Staff_Duty (
    DType VARCHAR(50) PRIMARY KEY,
    Ticketing_staff BOOLEAN,
    Train_Driver BOOLEAN,
    Booking_staff BOOLEAN
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Train (
    Train_ID INT AUTO_INCREMENT PRIMARY KEY,
    EName VARCHAR(100),
    AName VARCHAR(100),
    capacity INT DEFAULT 100
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Staff (
    Staff_ID INT AUTO_INCREMENT PRIMARY KEY,
    Train_ID INT NOT NULL,
    StaffFname VARCHAR(50),
    StaffLname VARCHAR(50),
    Staff_Email VARCHAR(100),
    Staff_phone VARCHAR(15),
    DType VARCHAR(50),
    FOREIGN KEY (Train_ID) REFERENCES Train(Train_ID),
    FOREIGN KEY (DType) REFERENCES Staff_Duty(DType)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Train_Schedule (
    Schedule_ID INT AUTO_INCREMENT PRIMARY KEY,
    Train_ID INT,
    Seq_Num INT NOT NULL,
    Arrival_Time TIME,
    Trip_Time TIME,
    Departure_Time TIME,
    Date DATE,
    Status VARCHAR(20) DEFAULT 'Scheduled',
    Available_Seats INT,
    FOREIGN KEY (Train_ID) REFERENCES Train(Train_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Route (
    Sequence_Number INT AUTO_INCREMENT PRIMARY KEY,
    Train_ID INT,
    Railway VARCHAR(100),
    FOREIGN KEY (Train_ID) REFERENCES Train(Train_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Station (
    Station_ID INT AUTO_INCREMENT PRIMARY KEY,
    City VARCHAR(100),
    Seq_Num INT NOT NULL,
    Station_Name VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE PassgHist (
    TotalRailway INT AUTO_INCREMENT PRIMARY KEY,
    Seq_Num INT NOT NULL,
    Transaction_Date DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Registered_Passenger (
    Passenger_ID INT AUTO_INCREMENT PRIMARY KEY,
    Passenger_Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    TotalRailway INT,
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (TotalRailway) REFERENCES PassgHist(TotalRailway)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Reservation (
    Reservation_Num INT AUTO_INCREMENT PRIMARY KEY,
    Schedule_ID INT,
    Passenger_ID INT NOT NULL,
    Seat_Number VARCHAR(10),
    Coach VARCHAR(50),
    Status VARCHAR(20) DEFAULT 'Pending',
    Departure_Reminder_Sent BOOLEAN DEFAULT FALSE,
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated_At DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Schedule_ID) REFERENCES Train_Schedule(Schedule_ID),
    FOREIGN KEY (Passenger_ID) REFERENCES Registered_Passenger(Passenger_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Payment (
    Payment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Reservation_Num INT,
    Payment_Amount DECIMAL(10,2),
    VAT_Amount DECIMAL(10,2),
    Status VARCHAR(20) DEFAULT 'Pending',
    Payment_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Reservation_Num) REFERENCES Reservation(Reservation_Num)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Loyalty_Miles (
    Passenger_ID INT PRIMARY KEY,
    Miles INT DEFAULT 0,
    Tier VARCHAR(20) DEFAULT 'Standard',
    Discount_Amount DECIMAL(5,2) DEFAULT 0,
    Last_Updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Passenger_ID) REFERENCES Registered_Passenger(Passenger_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Notification_Queue (
    Notification_ID INT AUTO_INCREMENT PRIMARY KEY,
    Passenger_ID INT,
    Type VARCHAR(50),
    Message TEXT,
    Status VARCHAR(20) DEFAULT 'Pending',
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    Sent_At DATETIME,
    FOREIGN KEY (Passenger_ID) REFERENCES Registered_Passenger(Passenger_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Waiting_List (
    Waiting_ID INT AUTO_INCREMENT PRIMARY KEY,
    Schedule_ID INT,
    Passenger_ID INT,
    Request_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(20) DEFAULT 'Waiting',
    FOREIGN KEY (Schedule_ID) REFERENCES Train_Schedule(Schedule_ID),
    FOREIGN KEY (Passenger_ID) REFERENCES Registered_Passenger(Passenger_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE Dependent (
    Dependent_ID INT AUTO_INCREMENT PRIMARY KEY,
    Passenger_ID INT,
    Dependent_Name VARCHAR(100),
    Relationship VARCHAR(50),
    Age INT,
    FOREIGN KEY (Passenger_ID) REFERENCES Registered_Passenger(Passenger_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE Staff_Assignment (
    Assignment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Staff_ID INT,
    Train_ID INT,
    Assignment_Date DATE,
    Status VARCHAR(20) DEFAULT 'Assigned',
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
    FOREIGN KEY (Train_ID) REFERENCES Train(Train_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE Unregistered_Passenger (
    Passenger_ID INT AUTO_INCREMENT PRIMARY KEY,
    Passenger_Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    Email VARCHAR(100),
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create users and set permissions
CREATE USER IF NOT EXISTS 'Hussain'@'localhost' IDENTIFIED BY 'hussain123';
CREATE USER IF NOT EXISTS 'Turki'@'localhost' IDENTIFIED BY 'turki123';
CREATE USER IF NOT EXISTS 'Faisel'@'localhost' IDENTIFIED BY 'faisel123';
CREATE USER IF NOT EXISTS 'Admin1'@'localhost' IDENTIFIED BY 'admin123';
CREATE USER IF NOT EXISTS 'Admin2'@'localhost' IDENTIFIED BY 'admin123';

-- Create roles
CREATE ROLE IF NOT EXISTS 'read_write_role';
CREATE ROLE IF NOT EXISTS 'admin_role';

-- Grant privileges to roles
GRANT SELECT, INSERT, UPDATE ON train_reservation_db.* TO 'read_write_role';
GRANT ALL PRIVILEGES ON train_reservation_db.* TO 'admin_role';

-- Assign roles to users
GRANT 'read_write_role' TO 'Hussain'@'localhost', 'Turki'@'localhost', 'Faisel'@'localhost';
GRANT 'admin_role' TO 'Admin1'@'localhost', 'Admin2'@'localhost';

-- Set default roles
SET DEFAULT ROLE 'read_write_role' TO 'Hussain'@'localhost', 'Turki'@'localhost', 'Faisel'@'localhost';
SET DEFAULT ROLE 'admin_role' TO 'Admin1'@'localhost', 'Admin2'@'localhost';

FLUSH PRIVILEGES;
