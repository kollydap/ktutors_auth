from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate an RSA private key (2048 bits is a common key size)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Serialize the private key to PEM format (for JWT signing)
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Save the private key to a file
def save_private_key():
    # todo try to check if theres already a private key, if not, generate one
    with open("private_key.pem", "wb") as key_file:
        key_file.write(private_key_pem)

def return_private_key():
    with open("private_key.pem", "rb") as key_file:
        private_key = key_file.read()
        return private_key
