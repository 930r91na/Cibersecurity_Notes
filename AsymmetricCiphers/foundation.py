

def primesUpTo(n):
    """Return a list of all prime numbers up to n (inclusive) using Sieve of Eratosthenes."""
    if n < 2:
        return []
    
    # Initialize boolean array "prime[0..n]" and set all entries as true
    prime = [True for _ in range(n + 1)]
    prime[0] = prime[1] = False  # 0 and 1 are not prime
    
    p = 2
    while p * p <= n:
        # If prime[p] is not changed, then it is a prime
        if prime[p]:
            # Update all multiples of p
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    
    # Collect all prime numbers
    primes = []
    for i in range(2, n + 1):
        if prime[i]:
            primes.append(i)
    
    return primes

def isPrime(num):
    primes = primesUpTo(int(num**0.5) + 1)
    for prime in primes:
        if num % prime == 0 and num != prime:
            return False
    
    return True


def isPrimeByMillerRabin(n, k=5):
    """Use Miller-Rabin primality test to check if n is prime.
    
    Args:
        n (int): Number to test for primality

        k (int): Number of iterations for accuracy (default: 5)
    """
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    # Write n-1 as d*2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Witness loop
    import random
    for _ in range(k):
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

def gcd(a, b):
    """Calculate Greatest Common Divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a


def prime_factorization(n):
    """Return the prime factorization of n as a list of tuples (prime, exponent)."""
    factors = []
    primes = primesUpTo(int(n**0.5) + 1)
    for prime in primes:
        if prime * prime > n:
            break
        count = 0
        while n % prime == 0:
            n //= prime
            count += 1
        if count > 0:
            factors.append((prime, count))
    if n > 1:
        factors.append((n, 1))
    return factors

def gcdByPrimeFactorization(a, b):
    """Calculate GCD of a and b using their prime factorizations."""
    factors_a = dict(prime_factorization(a))
    factors_b = dict(prime_factorization(b))

    # if k = gcd(a,b), then for each prime p in k, k contains p^min(e1,e2)
    
    common_factors = set(factors_a.keys()) & set(factors_b.keys())
    gcd_value = 1
    for prime in common_factors:
        gcd_value *= prime ** min(factors_a[prime], factors_b[prime])
    
    return gcd_value

if __name__ == "__main__":
    # Test the functions
    print("Testing primality and GCD functions")
    test_numbers = [29, 15, 97, 100, 561]
    for number in test_numbers:
        print(f"{number} is prime: {isPrime(number)} (Miller-Rabin: {isPrimeByMillerRabin(number)})")
    print("\nTesting GCD function")
    print(f"GCD of 48 and 18: {gcd(48, 18)}")
    print(f"GCD of 101 and 10: {gcd(101, 10)}")
    print("\nTesting prime factorization")
    for number in test_numbers:
        print(f"Prime factorization of {number}: {prime_factorization(number)}")

