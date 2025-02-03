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

    # Load the historical data (replace with your actual data)
    data = pd.read_csv("records_docs/haraka80seeds.csv", 
                       names=["Multiplier", "SHA256"], 
                       header=None, 
                       skiprows=1, 
                       engine='python') 

    # Define color prediction rules
    if hash_str.startswith(("6c", "6a", "6b")) or any(char in hash_str[0] for char in "012345"):
        predicted_color = "Red"
    else:
        predicted_color = "Green"

    # Define multiplier prediction rules
    if predicted_color == "Red":
        predicted_multiplier = 1.5  # Adjust this based on your analysis
    else:
        predicted_multiplier = 1.5  # Default value

        # Prioritize more specific matches
        for n in range(1, 4):  # Check up to 3-character prefixes
            prefix = hash_str[:n]
            try:
                char_data = data[data["SHA256"].astype(str).str.startswith(prefix)]
            except (AttributeError, ValueError):  # If conversion fails, try numeric comparison
                try:
                    char_data = data[data["SHA256"] >= int(prefix, 16)]
                except ValueError:  # If numeric comparison also fails, handle gracefully
                    char_data = pd.DataFrame() 

            if not char_data.empty:
                predicted_multiplier = char_data["Multiplier"].mean() + 1.00  # Safety margin
                break

    # Calculate confidence level (adjust based on your analysis)
    if predicted_color == "Red" and hash_str.startswith(("6c", "6a", "6b")):
        confidence = 0.9  # High confidence for strong Red indicators
    elif predicted_color == "Green" and hash_str.startswith(("5c", "5d", "5e", "5f")):
        confidence = 0.8  # High confidence for strong Green indicators
    else:
        confidence = 0.5  # Default confidence level

    return predicted_color, predicted_multiplier, confidence

# Example usage
hash_example = input("Enter SHA256 hash to predict multiplier: ").strip()
# hash_example = "36c5f163ca5555cf2237a491e4046a67fb24fecb290f98fd9f975a22e58f03f3"
predicted_color, predicted_multiplier, confidence = predict_multiplier(hash_example)

print(f"Predicted Color: {predicted_color}")
print(f"Predicted Multiplier: {predicted_multiplier:.2f}")
print(f"Confidence Level: {confidence:.2f}")