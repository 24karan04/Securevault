from cryptography.fernet import Fernet

# Generate key once and save it
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt(text):
    return cipher.decrypt(text.encode()).decode()