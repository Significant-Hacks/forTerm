import pandas as pd

# Load historical records from CSV
records = pd.read_csv("records_docs/haraka80seeds.csv", skipinitialspace=True)

# Ensure the SHA256 column is treated as strings
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

    return predicted_color, predicted_multiplier

# Function to log user feedback
def log_feedback(hash_str, predicted_color, predicted_multiplier, correct_multiplier):
    with open("prediction_feedback.txt", "a") as f:
        f.write(f"{hash_str}, {predicted_color}, {predicted_multiplier:.2f}, {correct_multiplier:.2f}\n")

# Function to calculate accuracy
def calculate_accuracy():
    try:
        feedback_data = pd.read_csv("prediction_feedback.txt", header=None, names=["Hash", "Predicted Color", "Predicted Multiplier", "Correct Multiplier"])
        correct_predictions = (feedback_data["Predicted Color"] == feedback_data["Predicted Color"]) & (feedback_data["Predicted Multiplier"].astype(float) == feedback_data["Correct Multiplier"].astype(float))
        accuracy = correct_predictions.mean() * 100
        print(f"Accuracy of predictions: {accuracy:.2f}%")
    except Exception as e:
        print(f"Error calculating accuracy: {e}")

# Main loop
while True:
    hash_str = input("Enter SHA256 hash to predict multiplier: ").strip()
    predicted_color, predicted_multiplier = predict_multiplier(hash_str)
    print(f"Predicted Color: {predicted_color}")
    print(f"Predicted Multiplier: {predicted_multiplier:.2f}")

    # Ask for user feedback
    correct_multiplier = float(input("Enter the correct multiplier (if known, else enter 0): "))
    log_feedback(hash_str, predicted_color, predicted_multiplier, correct_multiplier)

    # Optionally calculate accuracy after each entry
    calculate_accuracy()