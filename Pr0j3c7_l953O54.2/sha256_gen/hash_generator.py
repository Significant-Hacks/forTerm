import hashlib

def generate_hash(algorithm, input_data):
    """Generate a cryptographic hash for the given input data."""
    try:
        # Create a hash object
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(input_data.encode('utf-8'))
        return hash_obj.hexdigest()
    except ValueError:
        return f"Error: {algorithm} is not a valid hashing algorithm."

def main():
    print("Available algorithms: MD5, SHA1, SHA256, SHA512")
    algorithm = input("Enter the hashing algorithm: ").strip().lower()
    data = input("Enter the data to hash: ").strip()
    
    hash_value = generate_hash(algorithm, data)
    print(f"Hash ({algorithm}): {hash_value}")

if __name__ == "__main__":
    main()
