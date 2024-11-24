import mysql.connector

# Database connection
connection = mysql.connector.connect(
    host="sql12.freesqldatabase.com	",
    user="sql12747166",  # Replace with your MySQL username
    password="hLGUfs7Dgy",  # Replace with your MySQL password
    database="sql12747166"
)

cursor = connection.cursor()

# Introductory screen
def show_intro():
    print("\n" + "=" * 50)
    print(" " * 10 + "FLIGHT MANAGEMENT SYSTEM")
    print("=" * 50)
    print("\nSakthivel Azhakiamanavalan")
    print("Class: XII, Sec: C")
    print("School: D.A.V BHEL School, Ranipet")
    print("\n")

# User signup
def signup():
    print("\n=== Signup ===")
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    connection.commit()
    print("Signup successful! You can now log in.")

# User login
def login():
    print("\n=== Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        print("Login successful!")
        return True, user
    else:
        print("Invalid credentials. Please try again.")
        return False, None

# Administrator login
def admin_login():
    print("\n=== Administrator Login ===")
    admin_user = input("Enter admin username: ")
    admin_pass = input("Enter admin password: ")
    
    if admin_user == "admin" and admin_pass == "sakthi":
        print("Administrator login successful!")
        return True
    else:
        print("Invalid administrator credentials.")
        return False

# User menu
def user_menu():
    while True:
        print("\n--- User Menu ---")
        print("1. Book Ticket")
        print("2. View Bookings")
        print("3. View Flights")
        print("4. Logout")
        
        choice = int(input("Enter your choice: "))
        if choice == 1:
            book_ticket()
        elif choice == 2:
            view_bookings()
        elif choice == 3:
            view_flights()
        elif choice == 4:
            print("Logging out...")
            break
        else:
            print("Invalid choice! Please try again.")

# Administrator menu
def admin_menu():
    while True:
        print("\n=== Administrator Menu ===")
        print("1. Add Flight")
        print("2. View Flights")
        print("3. Update Flight")
        print("4. Delete Flight")
        print("5. View Booked Details")  # New option added
        print("6. Show Users")
        print("7. Add User")
        print("8. Edit User")
        print("9. Delete User")
        print("10. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_flight()
        elif choice == "2":
            view_flights()
        elif choice == "3":
            update_flight()
        elif choice == "4":
            delete_flight()
        elif choice == "5":
            view_booked_details()
        elif choice == "6":
            show_users()
        elif choice == "7":
            add_user()
        elif choice == "8":
            edit_user()
        elif choice == "9":  # New option handling
            delete_user()
        elif choice == "10":
            print("Exiting Administrator Menu...")
            break
        else:
            print("Invalid choice! Please try again.")


# Master Booking Details

def view_booked_details():
    print("\n=== View Booked Details ===")
    
    query = """
    SELECT 
        b.booking_id, 
        b.flight_id, 
        b.customer_name, 
        b.seats_booked,
        u.user_id,
        u.username,
        f.name AS flight_name,
        f.source,
        f.destination,
        f.price * b.seats_booked AS amount_paid
    FROM 
        bookings b
    LEFT JOIN 
        users u ON b.user_id = u.user_id
    LEFT JOIN 
        flights f ON b.flight_id = f.flight_id
    """
    
    cursor.execute(query)
    bookings = cursor.fetchall()

    if bookings:
        print(f"{'Booking ID':<12} {'Flight ID':<10} {'Customer Name':<20} {'Seats Booked':<12} {'User ID':<10} {'Username':<20} {'Flight Name':<25} {'Amount Paid':<12}")
        print("-" * 100)
        
        for booking in bookings:
            # Ensure all data is present, if not replace with a default value
            booking_id = booking[0] if booking[0] is not None else 'N/A'
            flight_id = booking[1] if booking[1] is not None else 'N/A'
            customer_name = booking[2] if booking[2] is not None else 'N/A'
            seats_booked = booking[3] if booking[3] is not None else 0
            user_id = booking[4] if booking[4] is not None else 'N/A'
            username = booking[5] if booking[5] is not None else 'N/A'
            flight_name = booking[6] if booking[6] is not None else 'N/A'
            source = booking[7] if booking[7] is not None else 'N/A'
            destination = booking[8] if booking[8] is not None else 'N/A'
            amount_paid = booking[9] if booking[9] is not None else 0.0
            
            # Format the amount paid to two decimal places, if it exists
            print(f"{booking_id:<12} {flight_id:<10} {customer_name:<20} {seats_booked:<12} {user_id:<10} {username:<20} {flight_name:<25} {amount_paid:<12.2f}")
    else:
        print("No bookings found.")





# Add a flight
def add_flight():
    print("\n=== Add Flight ===")
    name = input("Enter flight name: ")
    source = input("Enter source: ")
    destination = input("Enter destination: ")
    departure = input("Enter departure time: ")
    arrival = input("Enter arrival time: ")
    seats = int(input("Enter available seats: "))
    price = float(input("Enter ticket price: "))
    
    query = """
        INSERT INTO flights (name, source, destination, departure, arrival, seats, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, source, destination, departure, arrival, seats, price))
    connection.commit()
    print("Flight added successfully!")

# View flights
def view_flights():
    print("\n=== View Flights ===")
    query = "SELECT * FROM flights"
    cursor.execute(query)
    flights = cursor.fetchall()

    if flights:
        # Header
        print(f"{'Flight ID':<10} {'Name':<15} {'Source':<15} {'Destination':<15} {'Departure':<10} {'Arrival':<10} {'Seats':<10} {'Price':<10}")
        print("-" * 85)
        # Rows
        for flight in flights:
            # Convert timedelta to string
            departure = str(flight[4])
            arrival = str(flight[5])
            print(f"{flight[0]:<10} {flight[1]:<15} {flight[2]:<15} {flight[3]:<15} {departure:<10} {arrival:<10} {flight[6]:<10} {flight[7]:<10.2f}")
    else:
        print("No flights available.")


# Update flight
def update_flight():
    print("\n=== Update Flight ===")
    flight_id = int(input("Enter flight ID to update: "))
    seats = int(input("Enter new available seats: "))
    
    query = "UPDATE flights SET seats = %s WHERE flight_id = %s"
    cursor.execute(query, (seats, flight_id))
    connection.commit()
    print("Flight updated successfully!")

# Delete flight
def delete_flight():
    print("\n=== Delete Flight ===")
    flight_id = int(input("Enter flight ID to delete: "))
    
    query = "DELETE FROM flights WHERE flight_id = %s"
    cursor.execute(query, (flight_id,))
    connection.commit()
    print("Flight deleted successfully!")

# Book ticket
def book_ticket():
    print("\n=== Book Ticket ===")
    view_flights()
    flight_id = int(input("Enter flight ID to book: "))
    name = input("Enter your name: ")
    seats = int(input("Enter number of seats to book: "))
    
    query = "SELECT seats FROM flights WHERE flight_id = %s"
    cursor.execute(query, (flight_id,))
    available_seats = cursor.fetchone()
    
    if available_seats and available_seats[0] >= seats:
        # Update seats
        new_seats = available_seats[0] - seats
        update_query = "UPDATE flights SET seats = %s WHERE flight_id = %s"
        cursor.execute(update_query, (new_seats, flight_id))
        
        # Add booking
        booking_query = """
            INSERT INTO bookings (flight_id, customer_name, seats_booked)
            VALUES (%s, %s, %s)
        """
        cursor.execute(booking_query, (flight_id, name, seats))
        connection.commit()
        print("Booking successful!")
    else:
        print("Not enough seats available.")

# View bookings
def view_bookings():
    print("\n=== View Bookings ===")
    query = "SELECT * FROM bookings"
    cursor.execute(query)
    bookings = cursor.fetchall()

    if bookings:
        # Header
        print(f"{'Booking ID':<12} {'Flight ID':<10} {'Customer Name':<20} {'Seats Booked':<15}")
        print("-" * 60)
        # Rows
        for booking in bookings:
            print(f"{booking[0]:<12} {booking[1]:<10} {booking[2]:<20} {booking[3]:<15}")
    else:
        print("No bookings available.")


# Show users
def show_users():
    print("\n=== Show Users ===")
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    
    if users:
        for user in users:
            print(f"User ID: {user[0]}, Username: {user[1]}")
    else:
        print("No users found.")

# Edit user
def edit_user():
    print("\n=== Edit User ===")
    user_id = int(input("Enter user ID to edit: "))
    new_username = input("Enter new username: ")
    
    query = "UPDATE users SET username = %s WHERE user_id = %s"
    cursor.execute(query, (new_username, user_id))
    connection.commit()
    print("User updated successfully!")

# Delete user
def delete_user():
    print("\n=== Delete User ===")
    user_id = int(input("Enter user ID to delete: "))
    
    query = "DELETE FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    connection.commit()
    print("User deleted successfully!")

# Main function
def main():
    show_intro()
    while True:
        print("\n--- Welcome to Sakz Flights ---")
        print("1. Login")
        print("2. Signup")
        print("3. Administrator Login")
        print("4. Exit")
        
        choice = int(input("Enter your choice: "))
        if choice == 1:
            logged_in, user = login()
            if logged_in:
                user_menu()
        elif choice == 2:
            signup()
        elif choice == 3:
            if admin_login():
                admin_menu()
        elif choice == 4:
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Close connection at the end
try:
    main()
finally:
    cursor.close()
    connection.close()
