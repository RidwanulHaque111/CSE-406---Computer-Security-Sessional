import random
import time

time_p = 0.0
time_g = 0.0
time_a = 0.0
time_b = 0.0
time_A = 0.0
time_B = 0.0


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


def verify_equality(p, g, a, b):
    A = pow(g, a, p)
    B = pow(g, b, p)

    result1 = pow(A, b, p)
    result2 = pow(B, a, p)

    return result1 == result2


def get_p():
    global p
    return p
def get_g():
    global g
    return g
def get_a():
    global a
    return a
def get_b():
    global b
    return b
def get_A():
    global A
    return A
def get_B():
    global B
    return B


# Test the safe prime generation
k = int(input("Enter the number of bits (k): "))

time_start = time.perf_counter()
p = generate_large_prime(k)
time_stop = time.perf_counter()
time_p = time_stop - time_start


minimum = 2
maximum = p - 1

time_start = time.perf_counter()
g = find_primitive_root(p, minimum, maximum)
time_stop = time.perf_counter()
time_g = time_stop - time_start

time_start = time.perf_counter()
a = generate_large_prime(k // 2)
time_stop = time.perf_counter()
time_a = time_stop - time_start

b = generate_large_prime(k // 2)
#check if b is equal to a, if so generate new b
while (b == a):
    b = generate_large_prime(k // 2)

time_start = time.perf_counter()
A = pow(g, a, p)
time_stop = time.perf_counter()
time_A = time_stop - time_start
B = pow(g, b, p)

print("Generated safe prime number (p):", p)
print("Primitive root (g) for mod p:", g)
print("Generated prime number (a):", a)
print("Generated prime number (b):", b)
print("A = g^a (mod p):", A)
print("B = g^b (mod p):", B)

if verify_equality(p, g, a, b):
    print("Verification Successful: A^b (mod p) = B^a (mod p)")
else:
    print("Verification failed: A^b (mod p) != B^a (mod p)")

#print all the times
print("\nExecution time:")
print("p:", time_p," seconds")
print("g:", time_g," seconds")
print("a or b:", time_a," seconds")
print("A or B:", time_A," seconds")

def runHellman():
    global p
    global g
    global a
    global b
    global A
    global B

def get_p():
    global p
    return p

def get_g():
    global g
    return g


def get_a():
    global a
    return a


def get_b():
    global b
    return b


def get_A():
    global A
    return A


def get_B():
    global B
    return B


#take time for average of
def average_time(trials):
    global k
    time_p = 0.0
    time_g = 0.0
    time_a = 0.0
    time_A = 0.0
    trials = 50
    for i in range(trials):
        time_start = time.perf_counter()
        p = generate_large_prime(k)
        time_stop = time.perf_counter()
        time_p += time_stop - time_start

        time_start = time.perf_counter()
        g = find_primitive_root(p, minimum, maximum)
        time_stop = time.perf_counter()
        time_g += time_stop - time_start

        time_start = time.perf_counter()
        a = generate_large_prime(k // 2)
        time_stop = time.perf_counter()
        time_a += time_stop - time_start

        time_start = time.perf_counter()
        A = pow(g, a, p)
        time_stop = time.perf_counter()
        time_A += time_stop - time_start

    #print all the times
    print("\nAverage execution time:")
    print("p:", time_p/trials," seconds")
    print("g:", time_g/trials," seconds")
    print("a or b:", time_a/trials," seconds")
    print("A or B:", time_A/trials," seconds")

#average_time(100)
