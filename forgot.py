import json
from cryptography.fernet import Fernet

# Load encryption key
KEY_FILE = "key.key"
DATA_FILE = "data.json.enc"

def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def decrypt_data():
    key = load_key()
    cipher = Fernet(key)
    
    try:
        with open(DATA_FILE, "rb") as file:
            encrypted_data = file.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data)
    except Exception as e:
        print("Error decrypting data: Wrong Key", e)
        return {}

# Read and print the decrypted passwords
decrypted_data = decrypt_data()
if decrypted_data:
    print(json.dumps(decrypted_data, indent=4))
else:
    print("No stored passwords found.")
