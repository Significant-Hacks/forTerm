import pandas as pd
import hashlib

# Load the initial records from the CSV file
records = pd.read_csv("records_docs/haraka80seeds.csv")

def predict_multiplier(hash_str):
    # Define the color prediction rules
    if hash_str.startswith(("6c", "6a", "6b")) or any(char in hash_str[0] for char in "012345"):
        predicted_color = "Red"
    else:
        predicted_color = "Green"

    # Define multiplier prediction logic based on user notes
    if predicted_color == "Red":
        if hash_str[0] == '6' and hash_str[1] in ['c', 'a', 'b']:
            predicted_multiplier = 1.5  # Base value for Red
        else:
            predicted_multiplier = 1.5  # Default value
    else:
        # Green multiplier prediction based on character frequencies
        first_char = hash_str[0]
        if first_char in ['5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
            # Use historical data for specific starting character
            char_data = records[records["SHA256"].str.startswith(first_char)]
            if not char_data.empty:
                predicted_multiplier = char_data["Multiplier"].mean()
            else:
                predicted_multiplier = 1.5  # Default value if no data is available

        # Consider 2-character and 3-character sequences
        if len(hash_str) >= 2:
            first_two_chars = hash_str[:2]
            two_char_data = records[records["SHA256"].str.startswith(first_two_chars)]
            if not two_char_data.empty:
                predicted_multiplier = two_char_data["Multiplier"].mean()

        if len(hash_str) >= 3:
            first_three_chars = hash_str[:3]
            three_char_data = records[records["SHA256"].str.startswith(first_three_chars)]
            if not three_char_data.empty:
                predicted_multiplier = three_char_data["Multiplier"].mean()

    return predicted_color, predicted_multiplier

# Main loop
while True:
    hash_str = input("Enter SHA256 hash to predict multiplier: ").strip()
    try:
        calculated_hash = hashlib.sha256(hash_str.encode()).hexdigest()
        if calculated_hash == hash_str:
            predicted_color, predicted_multiplier = predict_multiplier(hash_str)
            print(f"Predicted Color: {predicted_color}")
            print(f"Predicted Multiplier: {predicted_multiplier:.2f}")
        else:
            print("Invalid hash.")
    except Exception as e:
        print(f"Error: {e}")
