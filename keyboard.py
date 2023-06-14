from tkinter import Tk
import time
import csv
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class UserProfile:
    def __init__(self):
        self.options = {
            "1": self.create_profile,
            "2": self.add_data,
            "3": self.test_password,
            "4": self.quit_program
        }
        self.profiles = {}
        self.current_profile = None
        self.user_data = []
        self.password_attempts = 0

    def display_menu(self):
        print("========== Keystroke Dynamics Based User Authentication System ==========")
        print("1. Create a profile")
        print("2. Add data to a profile")
        print("3. Test a profile")
        print("4. Quit")

    def get_user_input(self):
        return input("Enter your choice: ")

    def create_profile(self):
        profile_name = input("Enter profile name: ")
        self.profiles[profile_name] = {}
        print(f"Profile '{profile_name}' created.")

    def add_data(self):
        if not self.profiles:
            print("No profiles found. Please create a profile first.")
            return

        print("Existing Profiles:")
        for profile in self.profiles:
            print(f"- {profile}")

        profile_name = input("Enter the profile name to add data: ")
        if profile_name in self.profiles:
            self.current_profile = profile_name
            print(f"Enter the password 'techiscool123' for profile: {self.current_profile}")
            password_entered = False
            while not password_entered:
                try:
                    self.collect_data()
                    password_entered = True
                except ValueError:
                    print("Incorrect password. Please try again.")
            self.save_data()
            print("Data added successfully.")
        else:
            print("Profile not found. Please enter a valid profile name.")

    def collect_data(self):
        password = input("Enter the password: ")
        if password == "techiscool123":
            start_time = None

            def key_up(key_event):
                nonlocal start_time
                end_time = time.time()
                flight_time = end_time - start_time
                time_difference = abs(start_time - end_time) if start_time is not None else 0
                self.user_data.append([time_difference, flight_time, self.current_profile])
                start_time = end_time

            def key_down(key_event):
                nonlocal start_time
                start_time = time.time()
                print(f"Key pressed: {key_event.char}")

            root = Tk()
            root.title("Keystroke Dynamics Based User Authentication System")
            root.geometry("500x200")

            root.bind("<KeyPress>", key_down)
            root.bind("<KeyRelease>", key_up)
            root.mainloop()
        else:
            raise ValueError

    def save_data(self):
        filename = "keystroke_data.csv"
        header = ["Time Difference", "Flight Time", "Profiles"]

        if not os.path.isfile(filename):
            with open(filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)

        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.user_data)
        self.user_data = []

    def test_password(self):
        if self.profiles:
            print("Existing Profiles:")
            for profile in self.profiles:
                print(f"- {profile}")

            profile_name = input("Enter the profile name to test: ")
            if profile_name in self.profiles:
                self.current_profile = profile_name
                password_attempts = 0
                while password_attempts < 3:
                    password = input("Enter the password 'techiscool123': ")
                    if password == "techiscool123":
                        self.collect_data()
                        self.save_data()
                        self.analyze_typing_pattern()
                        break
                    else:
                        password_attempts += 1
                        if password_attempts >= 3:
                            print("Access denied. Too many incorrect attempts.")
                            self.quit_program()
                            return
                        print("Incorrect password. Please try again.")
            else:
                print("Profile not found. Please enter a valid profile name.")
        else:
            print("No profiles found. Please create a profile first.")

    def analyze_typing_pattern(self):
        filename = "keystroke_data.csv"
        if os.path.isfile(filename):
            data = pd.read_csv(filename)
            profile_data = data[data["Profiles"] == self.current_profile]
            X = profile_data.iloc[:, :-1]
            y = profile_data.iloc[:, -1]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestClassifier(n_estimators=100)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {accuracy * 100}%")
        else:
            print("No data available. Please add data to profiles first.")

    def quit_program(self):
        print("Exiting the program...")
        quit()


user_profile = UserProfile()

while True:
    user_profile.display_menu()
    choice = user_profile.get_user_input()

    if choice in user_profile.options:
        user_profile.options[choice]()
    else:
        print("Invalid choice. Please try again.")
