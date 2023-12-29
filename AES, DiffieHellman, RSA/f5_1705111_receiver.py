import socket
import random
import hashlib
from f3_1705111_myAES import *

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to ALICE
server_address = ('localhost', 11111)
client_socket.connect(server_address)
print("Connected to ALICE.\n")

p = client_socket.recv(1024).decode()
g = client_socket.recv(1024).decode()
A = client_socket.recv(1024).decode()

print("Successfully Received p = ",p)
print("Successfully Received g = ",g)
print("Successfully Received A = ",A)
print("Ready for Transmission!\n")

def is_prime(n, t=20):
    # Perform Robin-Miller primality test
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform the test t times
    for _ in range(t):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_large_prime(k):
    while True:
        # Generate a random prime number (p)
        p = random.getrandbits(k)
        p |= (1 << (k - 1)) | 1

        # Check if p is prime using Robin-Miller test
        if not is_prime(p):
            continue

        # Check if (cp-1)/2 is also prime
        q = (p - 1) // 2
        if is_prime(q):
            return p

# Generate b and send B to Server
k = 32
b = generate_large_prime(k // 2)
B = pow(int(g), b, int(p))

client_socket.send(str(B).encode())
shared_secret_key = pow(int(A), b, int(p))
shared_secret_key = str(shared_secret_key)
shared_secret_key = shared_secret_key.encode('utf-8')
shared_secret_key = hashlib.sha256(shared_secret_key).digest()

ciphertext = client_socket.recv(1024)
aes = AES(shared_secret_key)

print("Decrypted Text : ",end="")
for i in range(0,len(ciphertext),16):
    plaintext = aes.decrypt(ciphertext[i:i+16])
    print(plaintext.decode('latin-1').rstrip(' '),end="")

# Close the socket
client_socket.close()





