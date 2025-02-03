import pandas as pd

# Load the initial records from the CSV file
records = pd.read_csv("records_docs/haraka80seeds.csv")

# Define a function to predict the closest multiplier based on the hash
def predict_multiplier(hash_str):
    # Define the color prediction rules
    if hash_str.startswith(("6c", "6a", "6b")) or any(char in hash_str[0] for char in "012345"):
        predicted_color = "Red"
    else:
        predicted_color = "Green"

    # Define the multiplier prediction rules
    if predicted_color == "Red":
        multiplier_prefixes = {
            "0": 1.00,
            "1": 1.00,
            "2": 1.00,
            "3": 1.00,
            "4": 1.00,
            "5": 1.00,
            "6": 1.50
        }
    else:
        multiplier_prefixes = {
            "5": 1.00,
            "6": 2.00,
            "7": 2.00,
            "8": 2.00,
            "9": 2.00,
            "a": 3.01,
            "b": 3.00,
            "c": 4.48,
            "d": 5.60,
            "e": 8.00,
            "f": 20.99
        }

    # Get the prefix of the hash string
    prefix = hash_str[0]

    # Check if the prefix is in the multiplier_prefixes dictionary
    if prefix in multiplier_prefixes:
        # Get the multiplier for the prefix
        multiplier = multiplier_prefixes[prefix]
        # Check if the next character is also in the dictionary
        if len(hash_str) > 1 and hash_str[1] in multiplier_prefixes:
            # Get the multiplier for the next character
            multiplier += multiplier_prefixes[hash_str[1]]
        # Return the predicted multiplier
        return multiplier
    else:
        # If the prefix is not in the dictionary, return a default value
        return 1.00

# Main loop
while True:
    # Get a new hash from the user
    hash_str = input("Enter SHA256 hash to predict multiplier: ").strip()

    # Check if the hash is valid by looking it up in the records DataFrame
    if hash_str in records['SHA256'].values:
        # Get the corresponding Bust value
        bust_value = records.loc[records['SHA256'] == hash_str, 'BUST'].values[0]
        # Calculate the predicted multiplier
        predicted_multiplier = predict_multiplier(hash_str)
        # Print the predicted multiplier and color
        print(f"Predicted Color: {'Red' if predicted_multiplier >= 1.50 else 'Green'}")
        print(f"Predicted Multiplier: {predicted_multiplier:.2f}, Bust Value: {bust_value}")

        # Check if the user wants to bet or not
        bet = input("Do you want to bet? (yes/no): ").lower()
        if bet == "yes":
            # Simulate a bet (e.g., by printing a message)
            print("Betting on predicted values...")
            print("Bet successful!")
        else:
            print("Not betting.")
    else:
        print("Invalid hash. Please check and try again.")