import pandas as pd
from tkinter import *
import time

# Function to handle key release events
def key_up(key_event):
    global entered_password, user_data, start_time
    
    # Get the current time stamp
    time_stamp = time.time()
    
    # Add key up time to the last entered key in the password
    entered_password[-1].append(time_stamp)
    
    # Calculate the time difference between key down and key up events
    time_diff = time_stamp - entered_password[-1][1]
    entered_password[-1].append(time_diff)
    
    # If there is more than one key entered, calculate the flight time
    if len(entered_password) > 1:
        flight_time = time_stamp - entered_password[-2][1]
        entered_password[-2].append(flight_time)
        print("Flight Time:", flight_time)
    
    # Print the key up event details
    print("Key Up:", key_event.char)
    print("Time Difference:", time_diff)
    
    # Authenticate the entered password and save user data
    authenticate()
    save_user_data()

# Function to handle key press events
def key_down(key_event):
    global entered_password, start_time
    
    # Get the current time stamp
    time_stamp = time.time()
    
    # If it's the first key entered, set the start time
    if not entered_password:
        start_time = time_stamp
    
    # Add the key and key down time to the entered password
    entered_password.append([key_event.char, time_stamp])
    print("Key Down:", key_event.char)

# Function to authenticate the entered password
def authenticate():
    global entered_password, model, user_data
    
    password = "techiscool123"
    
    # If the entered password length is greater than or equal to the password length
    if len(entered_password) >= len(password):
        # Get the entered characters
        entered_chars = [entry[0] for entry in entered_password]
        
        # Check if the entered password matches the correct password
        if "".join(entered_chars[-len(password):]) == password:
            print("Authentication successful!")
            
            # Extract features from the entered password and authenticate the user using the trained model
            user_input = [entry[2] for entry in entered_password[:-1]]
            authenticate_user(user_input)
        else:
            print("Authentication failed!")
        
        # Clear the entered password
        entered_password = []

# Function to authenticate the user using a trained model
def authenticate_user(user_input):
    label = model.predict([user_input])[0]
    if label == "correct_user":
        print("User authentication successful!")
    else:
        print("User authentication failed!")

# Function to save the user data
def save_user_data():
    global user_data, entered_password, start_time
    
    # If there is more than one key entered, calculate the key down time, key up time, time difference, and flight time
    if len(entered_password) > 1:
        key_down_time = entered_password[-2][1] - start_time
        key_up_time = entered_password[-2][2] - start_time
        time_diff = entered_password[-2][3]
        flight_time = entered_password[-2][4]
        
        # Create a new DataFrame with the calculated values
        new_data = pd.DataFrame({"key_down_time": [key_down_time], "key_up_time": [key_up_time], "time_difference": [time_diff], "flight_time": [flight_time]})
        
        # Concatenate the new data with the existing user_data
        user_data = pd.concat([user_data, new_data], ignore_index=True)
        print(user_data)
        
        # Save the updated user data to a CSV file
        user_data.to_csv("user_data.csv", index=False)  # Change the file name as per your requirement

# Create an empty DataFrame to store user data
user_data = pd.DataFrame(columns=["key_down_time", "key_up_time", "time_difference", "flight_time"])

# Create the Tkinter root window and frame
root = Tk()
frame = Frame(root, width=100, height=100)

# Bind key press and key release events to the frame
frame.bind("<KeyPress>", key_down)
frame.bind("<KeyRelease>", key_up)

# Pack and focus on the frame
frame.pack()
frame.focus_set()

# Initialize variables
entered_password = []
start_time = 0.0

# Start the Tkinter event loop
root.mainloop()
