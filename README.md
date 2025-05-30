# Hybrid-Ransomware Proof-of-Concept

A Python-based proof-of-concept that demonstrates the hybrid cryptography workflow used by modern ransomware. This project simulates the full lifecycle of a file-encryption attack and key-recovery process:

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
## Security Note

This code is for educational purposes only. Do **not** deploy it on production systems or use it to harm real data.

## Features

- **Hybrid Cryptography**: Combines fast symmetric file encryption with secure asymmetric key protection.  
- **Client & Server**: Demonstrates both sides of the ransomware key-exchange protocol.  
- **Dependencies**:  
  - Python 3.8+  
  - [cryptography](https://pypi.org/project/cryptography/)  
- 🚀 **Quickstart**  
  1. Generate an RSA keypair (`openssl genpkey …`) on the server.  
  2. Copy the public key to the client machine.  
  3. Run `python ransomware_server.py` on Kali (port 8000).  
  4. Also on Kali, place your target files and `public_key.key` alongside `client.py`, then run:  
     ```bash
     python ransomware_client.py
     ```  
  5. Follow the prompts to encrypt, send the key, and decrypt.

---

