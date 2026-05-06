import base64
import os
import sys
from getpass import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

def banner():
    print("\033[33m")
    print(r"""
     ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗  ██████╗ ██████╗ ██████╗ ███████╗
    ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝
    ██║     ██║██████╔╝███████║█████╗  ██████╔╝██║     ██║   ██║██████╔╝█████╗
    ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗██╔══╝
    ╚██████╗██║██║     ██║  ██║███████╗██║  ██║╚██████╗╚██████╔╝██║  ██║███████╗
     ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

        ─────── CYPHER TOOLKIT ───────""")
    print("\033[0m")

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_text():
    password = getpass("Enter password: ")
    text = input("Enter text to encrypt: ").encode()

    salt = os.urandom(16)
    key = generate_key(password, salt)
    cipher = Fernet(key)

    encrypted = cipher.encrypt(text)

    result = base64.urlsafe_b64encode(salt + encrypted).decode()
    print ("\nEncrypted text:\n", result)


# Decrypt text

def decrypt_text():
    password = getpass("Enter password: ")
    encrypted_input = input("Enter encrypted text here: ")

    data = base64.urlsafe_b64decode(encrypted_input.encode())
    salt = data[:16]
    encrypted = data[16:]

    key = generate_key(password, salt)
    cipher = Fernet(key)

    try:
        decrypted = cipher.decrypt(encrypted)
        print("\nDecrypted text:\n", decrypted.decode())
    except:
        print("❌ Incorrect password or corrupted data")


# Encrypt file

def encrypt_file():
    password = getpass("Enter password: ")
    filename = input("Enter file path: ")

    if not os.path.exists(filename):
        print("❌ File not found")
        return

    with open(filename, "rb") as f:
        data = f.read()

    salt = os.urandom(16)
    key = generate_key(password, salt)
    cipher = Fernet(key)

    encrypted = cipher.encrypt(data)

    with open(filename + ".enc", "wb") as f:
        f.write(salt + encrypted)

    print(f"✅ Encrypted file saved as {filename}.enc")


# Decrypt file

def decrypt_file():
    password = getpass("Enter password: ")
    filename = input("Enter encrypted file path: ")

    if not os.path.exists(filename):
        print("❌ File not found")
        return

    with open(filename, "rb") as f:
        data = f.read()

    salt = data[:16]
    encrypted = data[16:]

    key = generate_key(password, salt)
    cipher = Fernet(key)

    try:
        decrypted = cipher.decrypt(encrypted)

        output_file = filename.replace(".enc", ".dec")
        with open(output_file, "wb") as f:
            f.write(decrypted)

        print(f"✅ Decrypted file saved as {output_file}")
    except:
        print("❌ Incorrect password or corrupted file")


# CLI Menu

def main():
    while True:
        print("\n==== Encryption Tool ====")
        print("1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Encrypt File")
        print("4. Decrypt File")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            encrypt_text()
        elif choice == "2":
            decrypt_text()
        elif choice == "3":
            encrypt_file()
        elif choice == "4":
            decrypt_file()
        elif choice == "5":
            print("Goodbye 👋")
            sys.exit()
        else:
            print(" Invalid option")

if __name__ == "__main__":
    banner()
    main()