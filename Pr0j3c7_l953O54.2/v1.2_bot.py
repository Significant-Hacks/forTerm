import pandas as pd
from sha256_gen.hash_generator import generate_hash

# Load historical records from CSV
records = pd.read_csv("records_docs/haraka80seeds.csv", skipinitialspace=True)
records["SHA256"] = records["SHA256"].astype(str)

def predict_multiplier(hash_str):
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

        # Additional logic for multipliers greater than 10
        if predicted_multiplier > 10:
            if predicted_multiplier >= 15:
                predicted_multiplier = predicted_multiplier * 1.1  # Adjust based on trends

    return predicted_color, predicted_multiplier

# Function to log user feedback
def log_feedback(hash_str, predicted_color, predicted_multiplier, correct_multiplier, accuracy):
    with open("v1.2/v1.2_bot_prediction_feedback.txt", "a") as f:
        f.write(f"{hash_str}, {predicted_color}, {predicted_multiplier:.2f}, {correct_multiplier:.2f}, Accuracy: {accuracy:.2f}%\n")

# Function to calculate accuracy
def calculate_accuracy(predicted_multiplier, correct_multiplier):
    if correct_multiplier > 0:
        return (predicted_multiplier / correct_multiplier) * 100
    return 0.0

# Main loop
last_hash = input("Enter the last known SHA256 hash: ").strip()
while True:
    # Generate the next hash based on the last known hash
    next_hash = generate_hash("sha256", last_hash)
    print(f"Generated Next Hash: {next_hash}")

    predicted_color, predicted_multiplier = predict_multiplier(next_hash)
    print(f"Predicted Color: {predicted_color}")
    print(f"Predicted Multiplier: {predicted_multiplier:.2f}")

    # Ask for user feedback
    correct_multiplier = float(input("Enter the correct multiplier (if known, else enter 0): "))
    # empty space for next round
    print("\n")
    accuracy = calculate_accuracy(predicted_multiplier, correct_multiplier)
    log_feedback(next_hash, predicted_color, predicted_multiplier, correct_multiplier, accuracy)

    # Update last_hash for the next iteration
    last_hash = next_hash
