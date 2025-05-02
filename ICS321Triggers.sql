-- Now we can create the departure reminder trigger
DELIMITER //
CREATE TRIGGER BeforeDeparture
BEFORE UPDATE ON Train_Schedule
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(HOUR, CURRENT_TIMESTAMP, 
        CONCAT(NEW.Date, ' ', NEW.Departure_Time)) = 3 THEN
        
        INSERT INTO Notification_Queue (
            Passenger_ID,
            Type,
            Message,
            Status
        )
        SELECT 
            r.Passenger_ID,
            'Departure Reminder',
            CONCAT('Your train ', t.EName, ' departs in 3 hours'),
            'Pending'
        FROM Reservation r
        JOIN Train_Schedule ts ON r.Schedule_ID = ts.Schedule_ID
        JOIN Train t ON ts.Train_ID = t.Train_ID
        WHERE ts.Schedule_ID = NEW.Schedule_ID;
    END IF;
END //
DELIMITER ;

-- Add trigger for payment reminder
DELIMITER //
CREATE TRIGGER PaymentReminder
AFTER INSERT ON Reservation
FOR EACH ROW
BEGIN
    -- Create payment reminder notification if payment not received within 24 hours
    INSERT INTO Notification_Queue (
        Passenger_ID,
        Type,
        Message,
        Status
    )
    SELECT 
        NEW.Passenger_ID,
        'Payment Reminder',
        CONCAT('Please complete payment for your reservation #', NEW.Reservation_Num),
        'Pending'
    WHERE NOT EXISTS (
        SELECT 1 FROM Payment 
        WHERE Reservation_Num = NEW.Reservation_Num 
        AND Status = 'Completed'
    );
END //
DELIMITER ;

-- Add trigger for waitlist promotion
DELIMITER //
CREATE TRIGGER WaitlistPromotion
AFTER UPDATE ON Train_Schedule
FOR EACH ROW
BEGIN
    IF NEW.Available_Seats > 0 THEN
        -- Get the next waitlisted passenger (prioritizing loyalty members)
        SET @next_passenger = (
            SELECT wl.Passenger_ID
            FROM Waiting_List wl
            LEFT JOIN Loyalty_Miles lm ON wl.Passenger_ID = lm.Passenger_ID
            WHERE wl.Schedule_ID = NEW.Schedule_ID
            AND wl.Status = 'Waiting'
            ORDER BY lm.Miles DESC, wl.Request_Date ASC
            LIMIT 1
        );
        
        IF @next_passenger IS NOT NULL THEN
            -- Update waiting list status
            UPDATE Waiting_List 
            SET Status = 'Promoted'
            WHERE Passenger_ID = @next_passenger
            AND Schedule_ID = NEW.Schedule_ID;
            
            -- Add notification
            INSERT INTO Notification_Queue (
                Passenger_ID,
                Type,
                Message,
                Status
            ) VALUES (
                @next_passenger,
                'Waitlist Promotion',
                'A seat is now available for your waitlisted journey. Please complete your booking within 24 hours.',
                'Pending'
            );
        END IF;
    END IF;
END //
DELIMITER ;