import pandas as pd

def predict_multiplier(hash_str):
    """
    Predicts the multiplier for a given Haraka crash game hash.

    Args:
        hash_str: The SHA256 hash string.

    Returns:
        A tuple containing:
            - Predicted color ('Red' or 'Green')
            - Predicted multiplier (float)
            - Confidence level (float between 0 and 1)
    """

    # Load the historical data
    data = pd.read_csv("records_docs/haraka80seeds.csv")

    # Define color prediction rules
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
            char_data = data[data["SHA256"].str.startswith(first_char)]
            if not char_data.empty:
                predicted_multiplier = char_data["Multiplier"].mean()
            else:
                predicted_multiplier = 1.5  # Default value if no data is available

        # Consider 2-character and 3-character sequences
        if len(hash_str) >= 2:
            first_two_chars = hash_str[:2]
            two_char_data = data[data["SHA256"].str.startswith(first_two_chars)]
            if not two_char_data.empty:
                predicted_multiplier = two_char_data["Multiplier"].mean()

        if len(hash_str) >= 3:
            first_three_chars = hash_str[:3]
            three_char_data = data[data["SHA256"].str.startswith(first_three_chars)]
            if not three_char_data.empty:
                predicted_multiplier = three_char_data["Multiplier"].mean()

    # Calculate confidence level
    if predicted_color == "Red" and hash_str.startswith(("6c", "6a", "6b")):
        confidence = 0.9
    elif predicted_color == "Green" and hash_str.startswith(("5c", "5d", "5e", "5f")):
        confidence = 0.8
    else:
        confidence = 0.5

    return predicted_color, predicted_multiplier, confidence

# Example usage
hash_example = input("Enter SHA256 hash to predict multiplier: ").strip()
predicted_color, predicted_multiplier, confidence = predict_multiplier(hash_example)

print(f"Predicted Color: {predicted_color}")
print(f"Predicted Multiplier: {predicted_multiplier:.2f}")
print(f"Confidence Level: {confidence:.2f}")
