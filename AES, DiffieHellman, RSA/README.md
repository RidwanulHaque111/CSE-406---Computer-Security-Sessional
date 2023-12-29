# Cryptosystem Implementation (AES, RSA, Diffie-Hellman)
This repository contains the implementation of a cryptosystem that utilizes a symmetric key for encryption and decryption. The symmetric key is securely shared using the Diffie-Hellman key exchange method. The system includes independent implementations of AES, Diffie-Hellman and RSA, along with a demonstration of the entire cryptosystem using TCP Socket Programming. I have extended AES implementation to support 192 and 256 bit keys.

## Overview of the Cryptosystem
*** AES Implementation ***
- Encryption and decryption using a user-provided 128, 192, 256-bit key (ASCII string).
- Key scheduling algorithm implemented as described here.
- Handle text blocks larger than 128 bits by dividing them into chunks.
- Support encryption and decryption of other file types (image, pdf, etc.) besides text files.
- Time-related performance reported in the code.

*** Diffie-Hellman Implementation *** 
- Generate a large prime p (at least k bits long, with k as a parameter).
- Find a primitive root g for mod p within the specified range [min, max].
- Generate private keys a and b (both at least k/2 bits long).
- Compute public keys A = g^a (mod p) and B = g^b (mod p).
- Compute shared keys Ab (mod p) and Ba (mod p) and verify their equality.
- Time-related performance reported in the code.

*** Cryptosystem Implementation using Sockets *** 
- Demonstrate Sender (ALICE) and Receiver (BOB) using TCP Socket Programming.
- ALICE sends p, g, and ga (mod p) to BOB. BOB responds with gb (mod p).
- Both compute the shared secret key, store it, and signal readiness for transmission.
- ALICE sends AES-encrypted ciphertext (CT) to BOB via sockets, who decrypts using the shared secret key.

*** RSA Implementation ***
- RSA for key exchange.
- RSA for authentication.

