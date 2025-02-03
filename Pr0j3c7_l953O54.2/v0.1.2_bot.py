import pandas as pd
from sha256_gen.hash_generator import generate_hash
from prettytable import PrettyTable
from datetime import datetime
import hashlib

# Load historical records from CSV
records = pd.read_csv("records_docs/haraka80seeds.csv", skipinitialspace=True)
records["SHA256"] = records["SHA256"].astype(str)

def predict_multiplier_v1_0(hash_str):
    predicted_color = "Green"
    predicted_multiplier = 1.00

    # Define color prediction rules
    if hash_str.startswith(("6c", "6a", "6b")) or any(char in hash_str[0] for char in "012345"):
        predicted_color = "Red"

    # Define multiplier prediction logic based on user notes
    if predicted_color == "Red":
        if hash_str[0] == '6' and hash_str[1] in ['c', 'a', 'b']:
            predicted_multiplier = 1.5  # Base value for Red
    else:
        first_char = hash_str[0]
        if first_char == 'c':
            predicted_multiplier = 4.00  # Default for 'c'
        elif first_char == 'a':
            predicted_multiplier = 2.00  # Default for 'a'
        elif first_char == 'b':
            predicted_multiplier = 3.00  # Default for 'b'
        elif first_char == 'd':
            predicted_multiplier = 5.00  # Default for 'd'
        elif first_char == 'e':
            predicted_multiplier = 10.00  # Default for 'e'
        elif first_char == 'f':
            predicted_multiplier = 20.00  # Default for 'f'

        # Check historical data for more accurate predictions
        char_data = records[records["SHA256"].str.startswith(first_char)]
        if not char_data.empty:
            predicted_multiplier = char_data["BUST"].mean()

    return predicted_color, predicted_multiplier

def predict_multiplier_v1_1(hash_str):
    predicted_color = "Green"
    predicted_multiplier = 1.50

    # Define color prediction rules
    if hash_str.startswith(("6c", "6a", "6b")) or any(char in hash_str[0] for char in "012345"):
        predicted_color = "Red"

    # Define multiplier prediction logic based on user notes
    if predicted_color == "Red":
        if hash_str[0] == '6' and hash_str[1] in ['c', 'a', 'b']:
            predicted_multiplier = 1.5  # Base value for Red
    else:
        first_char = hash_str[0]
        if first_char == 'c':
            predicted_multiplier = 4.00  # Default for 'c'
        elif first_char == 'a':
            predicted_multiplier = 2.00  # Default for 'a'
        elif first_char == 'b':
            predicted_multiplier = 3.00  # Default for 'b'
        elif first_char == 'd':
            predicted_multiplier = 5.00  # Default for 'd'
        elif first_char == 'e':
            predicted_multiplier = 10.00  # Default for 'e'
        elif first_char == 'f':
            predicted_multiplier = 20.00  # Default for 'f'

        # Check historical data for more accurate predictions
        char_data = records[records["SHA256"].str.startswith(first_char)]
        if not char_data.empty:
            predicted_multiplier = char_data["BUST"].mean()

    return predicted_color, predicted_multiplier

def predict_multiplier_v1_2(hash_str):
    predicted_color = "Green"
    predicted_multiplier = 1.00

    if hash_str.startswith(("6c", "6a", "6b")) or any(char in hash_str[0] for char in "012345"):
        predicted_color = "Red"

    # Define multiplier prediction logic based on user notes
    if predicted_color == "Red":
        if hash_str[0] == '6' and hash_str[1] in ['c', 'a', 'b']:
            predicted_multiplier = 1.5  # Base value for Red
    else:
        first_char = hash_str[0]
        if first_char == 'c':
            predicted_multiplier = 4.00  # Default for 'c'
        elif first_char == 'a':
            predicted_multiplier = 2.00  # Default for 'a'
        elif first_char == 'b':
            predicted_multiplier = 3.00  # Default for 'b'
        elif first_char == 'd':
            predicted_multiplier = 5.00  # Default for 'd'
        elif first_char == 'e':
            predicted_multiplier = 10.00  # Default for 'e'
        elif first_char == 'f':
            predicted_multiplier = 20.00  # Default for 'f'

        # Check historical data for more accurate predictions
        char_data = records[records["SHA256"].str.startswith(first_char)]
        if not char_data.empty:
            predicted_multiplier = char_data["BUST"].mean()

        # Additional logic for multipliers greater than 10
        if predicted_multiplier > 10:
            if predicted_multiplier >= 15:
                predicted_multiplier = predicted_multiplier * 1.1  # Adjust based on trends

    return predicted_color, predicted_multiplier

# Function to log user feedback
def log_feedback(hash_str, predicted_color, predicted_multiplier, correct_multiplier):
    with open("v0.1.2/v0.1.2_bot_prediction_feedback.txt", "a") as f:
        f.write(f"{hash_str}, {predicted_color}, {predicted_multiplier:.2f}, {correct_multiplier:.2f}\n")

# Function to display the table
def display_table(current_hash, versions, color_codes, predicted_multipliers, average_multiplier):
    table = PrettyTable()
    table.title = current_hash
    table.field_names = ["Versions", "Color Codes", "Predicted Multipliers", "Average Multiplier"]

    for version, color, multiplier in zip(versions, color_codes, predicted_multipliers):
        table.add_row([version, color, multiplier, ""])  # Empty for Average Multiplier

    # Set the Average Multiplier for the last row
    table.add_row(["Average", "", "", average_multiplier])  # Add average multiplier row

    print(table)

# Main loop
print("\n")
last_hash = input("Enter the last known SHA256 hash: ").strip()
versions = ["v1.0", "v1.1", "v1.2"]
color_codes = []
predicted_multipliers = []

while True:
    next_hash = generate_hash("sha256", last_hash)
    print(f"Generated Next Hash: {next_hash}")

    # Get predictions from all versions
    color_v1_0, multiplier_v1_0 = predict_multiplier_v1_0(next_hash)
    color_v1_1, multiplier_v1_1 = predict_multiplier_v1_1(next_hash)
    color_v1_2, multiplier_v1_2 = predict_multiplier_v1_2(next_hash)

    # Store results
    color_codes = [color_v1_0, color_v1_1, color_v1_2]
    predicted_multipliers = [multiplier_v1_0, multiplier_v1_1, multiplier_v1_2]

    # Calculate average multiplier
    average_multiplier = sum(predicted_multipliers) / len(predicted_multipliers)

    # Display results
    display_table(next_hash, versions, color_codes, predicted_multipliers, average_multiplier)

    # Ask for user feedback
    correct_multiplier = float(input("Enter the correct multiplier (if known, else enter 0): "))
    print("\n")
    log_feedback(next_hash, color_v1_2, multiplier_v1_2, correct_multiplier)

    # Update last_hash for the next iteration
    last_hash = next_hash
