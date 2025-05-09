import json
import os
import random

"""
Flight Booking System
Main features:
- User Registration
- Booking Flights
- Managing Booked Flights
- Purchase services (like meals, drinks, WiFi, etc.)
"""

# Flight class to hold flight information
class Flight:
    """
    Represents a flight with flight number, date, departure location, 
    and destination location.
    """

    def __init__(self, num, date=None, fly_to=None, fly_from=None):
        """
        Initializes a Flight object.

        Args:
        - num (str): The flight number.
        - date (str, optional): The date of the flight.
        - fly_to (str, optional): The destination location.
        - fly_from (str, optional): The departure location.
        """
        self.num = num
        self.date = date
        self.fly_to = fly_to
        self.fly_from = fly_from

    def __str__(self):
        """
        Returns a string representation of the flight.

        Returns:
        - str: A formatted string containing flight details.
        """
        return f"Flight Number: {self.num}, Date: {self.date}, From: {self.fly_from}, To: {self.fly_to}"


# User class to hold user information
class User:
    """
    Manages user information and operations such as registration, 
    login, and saving/loading user data from a file.
    """
    userList = {}  # Dictionary to store all users and their data

    def __init__(self, username, password, booked_flights=None):
        """
        Initializes a User object and adds the user to the global userList.

        Args:
        - username (str): The username of the user.
        - password (str): The password of the user.
        - booked_flights (list, optional): List of flights booked by the user.
        """
        if booked_flights is None:
            booked_flights = []  # Initialize an empty list for booked flights
        self.username = username
        self.password = password
        self.booked_flights = booked_flights
        User.userList[username] = {"password": password, "booked_flights": booked_flights}

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
        - str: A string containing the username.
        """
        return f"User: {self.username}"

    @staticmethod
    def register():
        """
        Registers a new user by taking input for username and password
        and saving the user in the userList dictionary.

        Returns:
        - User: The newly created user object, or None if the username exists.
        """
        username = input("Enter a new username: ")
        if username in User.userList:
            print("Username already exists. Please choose a different one.")
            return None
        password = input("Enter a new password: ")
        new_user = User(username, password)
        print(f"Account created successfully! Welcome, {username}!")
        return new_user

    @staticmethod
    def login():
        """
        Logs in an existing user by verifying the username and password.

        Returns:
        - User: A User object for the logged-in user, or None if login fails.
        """
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username in User.userList:
            if User.userList[username]["password"] == password:
                print(f"Welcome back, {username}!")
                return User(username, password, User.userList[username]["booked_flights"])
            else:
                print("Incorrect password. Please try again.")
                return None
        else:
            print("Username not found. Please register first.")
            return None

    @staticmethod
    def save_users_to_file():
        """
        Saves all users and their data from userList to a JSON file ('user.json').
        """
        with open("user.json", "w") as f:
            json.dump(User.userList, f, indent=4)

    @staticmethod
    def load_users_from_file():
        """
        Loads user data from the JSON file ('user.json') into the userList.
        """
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                User.userList = json.load(f)


# BookedFlight class to hold flight booking information
class BookedFlight:
    """
    Represents a booked flight, including flight details, seat selection, 
    and additional services ordered.
    """

    def __init__(self, flight, seat=None, services=None):
        """
        Initializes a BookedFlight object.

        Args:
        - flight (Flight): The Flight object being booked.
        - seat (str, optional): The selected seat.
        - services (list, optional): List of additional services ordered.
        """
        self.flight = flight
        self.seat = seat
        self.services = services if services else []

    def __str__(self):
        """
        Returns a string representation of the booked flight.

        Returns:
        - str: A formatted string describing the booked flight, seat, and services.
        """
        services_str = ", ".join(self.services) if self.services else "No services ordered"
        return f"Booked {self.flight}, Seat: {self.seat}, Services: {services_str}"


def generate_flight_number(destination):
    """
    Generates a random flight number based on the destination.

    Args:
    - destination (str): The destination location.

    Returns:
    - str: A flight number in the format 'ABC123', where 'ABC' is the first
      three letters of the destination and '123' is a random number.
    """
    prefix = destination[:3].upper()
    suffix = random.randint(100, 999)
    return f"{prefix}{suffix}"


def select_seat():
    """
    Simulates seat selection by displaying available seats and allowing the
    user to select one.

    Returns:
    - str: The seat selected by the user (e.g., '5C').
    """
    rows = 10
    cols = 6
    print("\nAvailable Seats:")
    for row in range(1, rows + 1):
        seats = [f"{row}{chr(ord('A') + col)}" for col in range(cols)]
        print(" ".join(seats))
    seat = input("Select your seat (e.g., 5C): ")
    return seat


def order_services():
    """
    Simulates ordering in-flight services by displaying a menu and allowing
    the user to select multiple services.

    Returns:
    - list: A list of selected services.
    """
    services_menu = {
        "1": "Meal",
        "2": "Drink",
        "3": "Extra Baggage",
        "4": "WiFi"
    }
    print("\nIn-flight Services Menu:")
    for key, service in services_menu.items():
        print(f"{key}) {service}")

    selected_services = []
    while True:
        choice = input("Select a service (or press Enter to finish): ")
        if choice in services_menu:
            selected_services.append(services_menu[choice])
            print(f"{services_menu[choice]} added to your order.")
        elif choice == "":
            break
        else:
            print("Invalid choice. Try again.")
    return selected_services


def main():
    """
    The main function of the Flight Booking System. It provides a menu-driven 
    interface for user registration, login, booking flights, viewing booked flights, 
    and logging out. User data is saved to a file upon exit.
    """
    User.load_users_from_file()
    current_user = None  # Tracks the logged-in user

    while True:
        os.system("clear")
        print("\n--- Menu ---")
        print("1) Register")
        print("2) Login")
        print("3) Book a Flight (Must be logged in)")
        print("4) View Booked Flights (Must be logged in)")
        print("5) Logout")
        print("x) Exit and Save")

        choice = input("Enter your choice: ").lower()

        if choice == "1":
            User.register()
            input("\nPress Enter to continue")

        elif choice == "2":
            current_user = User.login()
            input("\nPress Enter to continue")

        elif choice == "3":
            if current_user:
                fly_from = input("Enter the departure location (From): ")
                fly_to = input("Enter the destination location (To): ")
                date = input("Enter the date of travel (DD/MM/YYYY): ")

                flight_num = generate_flight_number(fly_to)
                flight = Flight(flight_num, date, fly_to, fly_from)

                seat = select_seat()
                services = order_services()

                booked_flight = BookedFlight(flight, seat, services)
                current_user.booked_flights.append(str(booked_flight))
                User.userList[current_user.username]["booked_flights"] = current_user.booked_flights

                print(f"\nFlight {flight} booked successfully!")
            else:
                print("You must log in first to book a flight.")
            input("\nPress Enter to continue")

        elif choice == "4":
            if current_user:
                print("Your booked flights:")
                for flight in current_user.booked_flights:
                    print(flight)
            else:
                print("You must log in first to view booked flights.")
            input("\nPress Enter to continue")

        elif choice == "5":
            if current_user:
                print(f"Goodbye, {current_user.username}!")
                current_user = None
            input("\nPress Enter to continue")

        elif choice == "x":
            User.save_users_to_file()
            print("User data saved. Goodbye")
            break

        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue")


if __name__ == "__main__":
    main()