import socket
import random
import hashlib
from f3_1705111_myAES import *

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 11111)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print("Waiting for BOB to connect...")

# Accept a connection from BOB
client_socket, client_address = server_socket.accept()
print("BOB connected.\n")

### Hellman Block
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

        # Check if (p-1)/2 is also prime
        q = (p - 1) // 2
        if is_prime(q):
            return p


def find_primitive_root(p, minimum, maximum):
    while True:
        g = random.randint(minimum, maximum)
        if pow(g, (p - 1) // 2, p) != 1 and pow(g, p - 1, p) == 1:
            return g

# Test the safe prime generation
k = 32

p = generate_large_prime(k)

minimum = 2
maximum = p - 1


g = find_primitive_root(p, minimum, maximum)

a = generate_large_prime(k // 2)
b = generate_large_prime(k // 2)
#check if b is equal to a, if so generate new b
while (b == a):
    b = generate_large_prime(k // 2)

A = pow(g, a, p)
### End of Hellman


#send p,g,A to BOB
client_socket.send(str(p).encode())
client_socket.send(str(g).encode())
client_socket.send(str(A).encode())
print("Successfully Sent p = ", str(p))
print("Successfully Sent g = ", str(g))
print("Successfully Sent A = ", str(A))
print("Ready for Transmission!\n")

#receive B from BOB
B = int(client_socket.recv(1024).decode())
shared_secret_key = pow(B, a, p)
shared_secret_key = str(shared_secret_key)
shared_secret_key = shared_secret_key.encode('utf-8')
shared_secret_key = hashlib.sha256(shared_secret_key).digest()


aes = AES(shared_secret_key)
key = shared_secret_key
plaintext = input("Enter Plain text:")
ciphertext = ""

# check if the plaintext has more than 16 bytes. if yes, divide it into blocks of 16 bytes and encrypt each block separately. if no, pad the plaintext with zeros to make it 16 bytes.
if len(plaintext) >= 16:
    # print("The plaintext has more than 16 bytes. It will be divided into blocks of 16 bytes and encrypted separately.")
    plaintext_blocks = []
    for i in range(0, len(plaintext), 16):
        plaintext_blocks.append(plaintext[i:i + 16])
    # add zeros to the last block if it has less than 16 bytes
    if len(plaintext_blocks[-1]) < 16:
        while len(plaintext_blocks[-1]) < 16:
            plaintext_blocks[-1] += " "

    ciphertext_blocks = []
    for i in range(len(plaintext_blocks)):
        plaintext_blocks[i] = plaintext_blocks[i].encode('utf-8')

        aes = AES(key)
        ciphertext_blocks.append(aes.encrypt(plaintext_blocks[i]))
    ciphertext = b''.join(ciphertext_blocks)

else:
    # print("The plaintext has less than 16 bytes. It will be padded with zeros to make it 16 bytes.")
    while len(plaintext) < 16:
        plaintext += " "

    plaintext = plaintext.encode('utf-8')
    aes = AES(key)
    ciphertext = aes.encrypt(plaintext)

print("Sent Ciphertext : ",end="")
print(ciphertext.decode('latin-1'))

client_socket.send(ciphertext)
client_socket.close()
server_socket.close()


