import json
import os
import random

"""
Flight Booking System
Main features:
- User Registration
- Booking Flights
- Managing Booked Flights
- Purchase services
"""

# Flight class to hold flight information
class Flight:
    def __init__(self, num, date=None, fly_to=None, fly_from=None):
        self.num = num
        self.date = date
        self.fly_to = fly_to
        self.fly_from = fly_from

    def __str__(self):
        return f"Flight Number: {self.num}, Date: {self.date}, From: {self.fly_from}, To: {self.fly_to}"

# User class to hold user information
class User:
    userList = {}  # A dictionary to store all users

    def __init__(self, username, password, booked_flights=None):
        # empty list for booked flights
        if booked_flights is None:
            booked_flights = []
        self.username = username
        self.password = password
        self.booked_flights = booked_flights
        User.userList[username] = {"password": password, "booked_flights": booked_flights}

    def __str__(self):
        return f"User: {self.username}"

    # Method to register a new account
    @staticmethod
    def register():
        username = input("Enter a new username: ")
        if username in User.userList:  # Check if username already exists
            print("Username already exists. Please choose a different one.")
            return None
        password = input("Enter a new password: ")
        new_user = User(username, password)
        print(f"Account created successfully! Welcome, {username}!")
        return new_user

    # Method to log in
    @staticmethod
    def login():
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username in User.userList:  # Check if username exists
            if User.userList[username]["password"] == password:
                print(f"Welcome back, {username}!")
                return User(username, password, User.userList[username]["booked_flights"])
            else:
                print("Incorrect password. Please try again.")
                return None
        else:
            print("Username not found. Please register first.")
            return None

    # Save users to a JSON file
    @staticmethod
    def save_users_to_file():
        with open("user.json", "w") as f:
            json.dump(User.userList, f, indent=4)

    # Load users from a JSON file
    @staticmethod
    def load_users_from_file():
        if os.path.exists("user.json"):
            with open("user.json", "r") as f:
                User.userList = json.load(f)

# BookedFlight class to hold flight booking information
class BookedFlight:
    def __init__(self, flight):
        self.flight = flight

    def __str__(self):
        return f"Booked {self.flight}"

def generate_flight_number(destination):
    #Generates a random flight number based on the destination.
    prefix = destination[:3].upper()  # First three letters of the destination
    suffix = random.randint(100, 999)  # Random number between 100 and 999
    return f"{prefix}{suffix}"

def manage_booked_flights(current_user):
    if not current_user.booked_flights:
        print("You have no booked flights to manage.")
        input("\nPress Enter to continue")
        return

    while True:
        print("\n--- Manage Booked Flights ---")
        for idx, flight_str in enumerate(current_user.booked_flights):
            print(f"{idx+1}) {flight_str}")
        print("0) Go back")

        try:
            choice = int(input("Select a flight number to manage, or 0 to return: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if choice == 0:
            break
        if 1 <= choice <= len(current_user.booked_flights):
            selected_idx = choice - 1
            print(f"You selected: {current_user.booked_flights[selected_idx]}")
            print("a) Remove this flight")
            print("b) Edit this flight")
            print("c) Go back")

            action = input("Choose an action: ").lower()
            if action == "a":
                removed_flight = current_user.booked_flights.pop(selected_idx)
                User.userList[current_user.username]["booked_flights"] = current_user.booked_flights
                print(f"Removed flight: {removed_flight}")
                input("\nPress Enter to continue")
                break
            elif action == "b":
                # Try to extract the flight number, date, from, and to from the string
                flight_str = current_user.booked_flights[selected_idx]
                # Basic parsing (since we stored as string)
                try:
                    parts = flight_str.replace('Flight Number: ', '').replace('Date: ', '').replace('From: ', '').replace('To: ', '').split(',')
                    num = parts[0].strip()
                    date = parts[1].strip()
                    fly_from = parts[2].strip()
                    fly_to = parts[3].strip()
                except Exception:
                    print("Could not parse flight details. Cannot edit.")
                    input("\nPress Enter to continue")
                    continue
                print("\nEnter new values (leave blank to keep current):")
                new_date = input(f"New date [{date}]: ").strip() or date
                new_fly_from = input(f"New departure location [{fly_from}]: ").strip() or fly_from
                new_fly_to = input(f"New destination [{fly_to}]: ").strip() or fly_to
                # Optionally, allow changing the flight number (usually we keep it, or regenerate if destination changes)
                if new_fly_to != fly_to:
                    new_num = generate_flight_number(new_fly_to)
                else:
                    new_num = num

                # Build new Flight string and update
                new_flight = Flight(new_num, date=new_date, fly_from=new_fly_from, fly_to=new_fly_to)
                current_user.booked_flights[selected_idx] = str(new_flight)
                User.userList[current_user.username]["booked_flights"] = current_user.booked_flights
                print("Flight updated.")
                input("\nPress Enter to continue")
                break
            elif action == "c":
                continue
            else:
                print("Invalid action.")
        else:
            print("Invalid flight number.")

def main():
    # Load existing users from file
    User.load_users_from_file()

    current_user = None  # To track the logged-in user

    while True:
        # main menu
        os.system("clear")
        print("\n--- Menu ---")
        print("1) Register")
        print("2) Login")
        print("3) Book a Flight (Must be logged in)")
        print("4) View Booked Flights (Must be logged in)")
        print("5) Logout")
        print("6) Manage Booked Flights (Must be logged in)")  # <--- new menu option
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
                
                # Generate a random flight number based on the destination
                flight_num = generate_flight_number(fly_to)
                
                # Create a new Flight object with all details
                flight = Flight(flight_num, date=date, fly_from=fly_from, fly_to=fly_to)
                # Book the flight 
                # Append the flight to the user's booked flights
                # and update the user list
                # in the userList dictionary
                current_user.booked_flights.append(str(flight))
                User.userList[current_user.username]["booked_flights"] = current_user.booked_flights
                print(f"Flight {flight} booked successfully!")
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
            else:
                print("You are not logged in.")
            input("\nPress Enter to continue")

        elif choice == "6":  # <--- handle new menu option
            if current_user:
                manage_booked_flights(current_user)
            else:
                print("You must log in first to manage booked flights.")
                input("\nPress Enter to continue")

        elif choice == "x":
            User.save_users_to_file()  # Save user data to file before exiting
            print("User data saved. Goodbye")
            break

        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue")


if __name__ == "__main__":
    main()
