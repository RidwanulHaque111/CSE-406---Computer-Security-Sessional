from BitVector import BitVector
import random
import time
import hashlib

timer_key_gen = 0
timer_encrypt = 0
timer_decrypt = 0
def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x

def euclid_inverse(e, phi):
    d = 0
    a1 = 0
    a2 = 1
    b1 = 1
    t_phi = phi

    while e > 0:
        t1 = t_phi//e
        t2 = t_phi - t1 * e
        t_phi = e
        e = t2

        a = a2 - t1 * a1
        b = d - t1 * b1

        a2 = a1
        a1 = a
        d = b1
        b1 = b

    if (t_phi == 1):
        return d + phi


def generate_key_pair(p, q):
    global timer_key_gen
    start = time.time()
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = euclid_inverse(e, phi)
    end = time.time()
    timer_key_gen = end-start
    return (e, n), (d, n)


def encrypt(pk, text):
    global timer_encrypt
    start = time.time()
    key, n = pk
    cipher = [pow(ord(x), key, n) for x in text]
    end = time.time()
    timer_encrypt = end-start
    return cipher


def decrypt(pk, text):
    global timer_decrypt
    start = time.time()
    key, n = pk
    lis = [str(pow(x, key, n)) for x in text]
    decrypted= [chr(int(x)) for x in lis]
    end = time.time()
    timer_decrypt = end - start
    return ''.join(decrypted)

# Function to generate a digital signature
def sign(private_key, message):
    # Hash the message using a cryptographic hash function
    hashed_message = hashlib.sha256(message.encode()).digest()

    # Encrypt the hashed message using the private key
    signature = pow(int.from_bytes(hashed_message, byteorder='big'), private_key[0], private_key[1])

    return signature

# Function to verify a digital signature
def verify(public_key, message, signature):
    # Hash the message using a cryptographic hash function
    hashed_message = hashlib.sha256(message.encode()).digest()

    # Decrypt the signature using the public key
    recovered_message_digest = pow(signature, public_key[0], public_key[1])

    # Compare the recovered message digest with the newly computed message digest
    if int.from_bytes(hashed_message, byteorder='big') == recovered_message_digest:
        return True
    else:
        return False


k = int(input("Enter value of K (16, 32, 64 or 128): "))
k = int (k/2)
low = 2**(k-1)
high = 2**(k)-1

bit_size = k
p = BitVector(intVal = 0)
q = BitVector(intVal = 0)
while True:
    p = p.gen_random_bits(bit_size)
    check = p.test_for_primality()
    if check > 0.9:
        break
while True:
    q = q.gen_random_bits(bit_size)
    check = q.test_for_primality()
    if check > 0.9:
        break
x = p.intValue()
y = q.intValue()

public, private = generate_key_pair(x, y)
print("Generated Keys")
print("{'public':",public,",", "'private':",private,"}")
plain_text = input("\nInput Plain Text : ")
print(plain_text)

# Sign the message
signature = sign(private, plain_text)


encrypted_text = encrypt(public,plain_text)
print("\nCipher Text:")
for cipher in encrypted_text:
    print(cipher,end="")

decrypted_text = decrypt(private,encrypted_text)
print("\nDecrypted Text:")
print(decrypted_text)
print("\nExecution Time:")
print("Key-Generation: ",timer_key_gen, "seconds")
print("Encryption: ",timer_encrypt, "seconds")
print("Decryption: ",timer_decrypt, "seconds")


# Verify the signature
is_authentic = verify(public, decrypted_text, signature)


print("\nAuthentication : ",is_authentic)





