# Hybrid-Ransomware Proof-of-Concept

*Python-based demonstration of a hybrid cryptographic ransomware workflow**  
This repository contains a proof-of-concept implementation that simulates the **full lifecycle of a ransomware file-encryption attack** with client-server key recovery, illustrating how modern ransomware combines fast symmetric encryption with asymmetric key protection. :contentReference[oaicite:0]{index=0}

1. **Symmetric Encryption**  
   - Generates a random AES (Fernet) key.  
   - Encrypts one or more target files in place using AES-CBC (via `cryptography.fernet`).

2. **Asymmetric Key Wrapping**  
   - Loads the attacker’s RSA public key.  
   - Encrypts (wraps) the AES key with RSA‐OAEP (SHA-256).  
   - Stores the encrypted AES key to disk.

3. **Key Recovery Server**  
   - A multithreaded TCP server (built with `socketserver`) running on the attacker’s machine.  
   - Accepts incoming encrypted AES keys, decrypts them with the attacker’s RSA private key, and returns the raw AES key to the client.

4. **Client-Server Interaction**  
   - The client prompts the “victim” for a verification code (`wahoo`) before requesting decryption.  
   - Sends the wrapped AES key to the server and receives back the decrypted AES key.  
   - Uses the recovered AES key to decrypt all previously encrypted files.

---

## Features

- **Hybrid Cryptography** — Demonstrates AES symmetric file encryption combined with RSA key wrapping. :contentReference[oaicite:3]{index=3}  
- **Client & Server Components** — Showcase both sides of key exchange and decryption workflow. :contentReference[oaicite:4]{index=4}  
- **TCP Multithreaded Server** — Supports multiple client requests for key decryption. :contentReference[oaicite:5]{index=5}  
- **Python-Only** — Uses standard Python 3.8+ and the `cryptography` library. :contentReference[oaicite:6]{index=6}

---
## Security Note

This code is for educational purposes only. Do **not** deploy it on production systems or use it to harm real data.

## Features

- **Hybrid Cryptography**: Combines fast symmetric file encryption with secure asymmetric key protection.  
- **Client & Server**: Demonstrates both sides of the ransomware key-exchange protocol.  
- **Dependencies**:  
  - Python 3.8+  
  - [cryptography](https://pypi.org/project/cryptography/)

##Quickstart
  
  1. Generate an RSA keypair on the server: 
     ```
     openssl genkey -algorithm RSA -out private_key.pem - pkeyopt rsa_keygen_bits:4096
     openssl rsa -pubout -in private_key.pem -out public_key.pem
     ```
  2. Run the Key Recovery Server (Attacker Machine): (`python ransomware_server.py`).
     ```
     python ransomware_server.py
     ```  
     Set the server to listen on the desired port (defaut 8000)
  3. Run the Client (Victim Machine): place your target files and `public_key.key` alongside `client.py`, then run:  
     ```
     python ransomware_client.py
     ```  
  4. Follow the prompts to encrypt, send the key, and decrypt.
   - Encrypt target files.
   - Send wrapped AES key to server.
   - Retrieve original AES key.
   - Decrypt files.
---
## Workflow 
1. Encryption Phase
 - The client picks targer files.
 - Generates a random AES key.
 - Encrypts files with AES.
 - Wraps the AES Key using RSA public key.
 - Sends wrapped key to server. 
2. Decryption Phase
 - Client authenticates with server (example uses a hardcoded verification code: `wahoo`).
 - Server decrypts AES key using private RSA key.
 - Client uses recovered AES key to decrypt files.
---
**Short Walkthrough Video**
Link: https://youtu.be/aeaSkzG2dY4?si=UBVt-5Ownp4AHoeF 
