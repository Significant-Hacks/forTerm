import pandas as pd
import time

def predict_multiplier(hash_str, historical_data):
    """
    Predicts the multiplier for a given Haraka crash game hash, 
    incorporating historical data and a safety margin.

    Args:
        hash_str: The SHA256 hash string.
        historical_data: Pandas DataFrame containing historical hashes and multipliers.

    Returns:
        A tuple containing:
            - Predicted color ('Red' or 'Green')
            - Predicted multiplier (float)
            - Confidence level (float between 0 and 1)
    """

    start_time = time.time()

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
            char_data = historical_data[historical_data["Hash"].str.startswith(prefix)]
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

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Prediction time: {elapsed_time:.3f} seconds")

    return predicted_color, predicted_multiplier, confidence

# Load your historical data (replace with your actual file path)
historical_data = pd.read_csv("records_docs/haraka80seeds.csv", names=["Hash", "Multiplier"])

# Example usage
hash_example = "f2c51d16669a4c6bc52b75dbdd4576d50bc39f9f3fa0b0f7754fca4c7c66abe9"
predicted_color, predicted_multiplier, confidence = predict_multiplier(hash_example, historical_data)

print(f"Predicted Color: {predicted_color}")
print(f"Predicted Multiplier: {predicted_multiplier:.2f}")
print(f"Confidence Level: {confidence:.2f}")