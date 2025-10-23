# Mathematical Foundations - Practical Examples

This file demonstrates the mathematical concepts from Foundation.md with concrete examples and implementations.

## Prime Number Examples and Verification

### Small Primes
```python
from foundation import isPrime, primesUpTo

# First 20 primes
primes_20 = primesUpTo(71)
print("First 20 primes:", primes_20)

# Verify primality of some numbers
test_numbers = [97, 98, 99, 100, 101]
for n in test_numbers:
    print(f"{n} is {'prime' if isPrime(n) else 'composite'}")
```

### Large Prime Testing
```python
from foundation import isPrimeByMillerRabin

# Test some larger numbers
large_candidates = [
    982451653,  # Known prime
    982451654,  # Even, so composite
    1000000007, # Known prime
    1000000009  # Known prime
]

for candidate in large_candidates:
    is_prime = isPrimeByMillerRabin(candidate, k=10)
    print(f"{candidate}: {'Prime' if is_prime else 'Composite'}")
```

## Prime Factorization Examples

### Manual Factorization
```python
def prime_factorization(n):
    """Return the prime factorization of n as a list of (prime, exponent) pairs."""
    factors = []
    d = 2
    
    while d * d <= n:
        exponent = 0
        while n % d == 0:
            n //= d
            exponent += 1
        if exponent > 0:
            factors.append((d, exponent))
        d += 1
    
    if n > 1:
        factors.append((n, 1))
    
    return factors

# Examples
numbers_to_factor = [60, 84, 100, 315, 1001]
for num in numbers_to_factor:
    factors = prime_factorization(num)
    factorization = " × ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors])
    print(f"{num} = {factorization}")
```

### Verification
```python
def verify_factorization(n, factors):
    """Verify that the factorization is correct."""
    product = 1
    for prime, exponent in factors:
        product *= prime ** exponent
    return product == n

# Verify our factorizations
for num in numbers_to_factor:
    factors = prime_factorization(num)
    is_correct = verify_factorization(num, factors)
    print(f"Factorization of {num} is {'correct' if is_correct else 'incorrect'}")
```

## GCD and Coprime Examples

### Euclidean Algorithm in Action
```python
from foundation import gcd, extendedGcd

# GCD examples
pairs = [(48, 18), (101, 13), (270, 192), (17, 19)]

for a, b in pairs:
    g = gcd(a, b)
    print(f"gcd({a}, {b}) = {g}")
    print(f"  {a} and {b} are {'coprime' if g == 1 else 'not coprime'}")
```

### Extended GCD for Finding Inverses
```python
def demonstrate_extended_gcd(a, b):
    """Show how extended GCD works step by step."""
    g, x, y = extendedGcd(a, b)
    print(f"Extended GCD({a}, {b}):")
    print(f"  gcd = {g}")
    print(f"  Coefficients: x = {x}, y = {y}")
    print(f"  Verification: {a} × {x} + {b} × {y} = {a*x + b*y} = {g}")
    return g, x, y

# Examples
demonstrate_extended_gcd(240, 46)
demonstrate_extended_gcd(17, 13)
```

## Modular Arithmetic Examples

### Fermat's Little Theorem Verification
```python
from foundation import modularExponentiation

def verify_fermat_little_theorem(a, p):
    """Verify Fermat's Little Theorem: a^(p-1) ≡ 1 (mod p)."""
    if not isPrime(p):
        return False, f"{p} is not prime"
    
    if gcd(a, p) != 1:
        return False, f"{a} and {p} are not coprime"
    
    result = modularExponentiation(a, p - 1, p)
    return result == 1, f"{a}^{p-1} ≡ {result} (mod {p})"

# Test Fermat's Little Theorem
test_cases = [
    (2, 7),   # 2^6 ≡ 1 (mod 7)
    (3, 11),  # 3^10 ≡ 1 (mod 11)  
    (5, 13),  # 5^12 ≡ 1 (mod 13)
    (7, 17),  # 7^16 ≡ 1 (mod 17)
]

for a, p in test_cases:
    is_valid, message = verify_fermat_little_theorem(a, p)
    print(f"Fermat's Little Theorem for a={a}, p={p}: {message} ✓" if is_valid else f"❌ {message}")
```

### Multiplicative Inverse Examples
```python
from foundation import modularInverse

def demonstrate_multiplicative_inverse(a, m):
    """Show multiplicative inverse calculation and verification."""
    try:
        inv = modularInverse(a, m)
        verification = (a * inv) % m
        print(f"Multiplicative inverse of {a} modulo {m}:")
        print(f"  {a}^(-1) ≡ {inv} (mod {m})")
        print(f"  Verification: {a} × {inv} ≡ {verification} (mod {m}) ✓")
        return inv
    except ValueError as e:
        print(f"❌ {e}")
        return None

# Examples
inverse_examples = [(3, 11), (7, 26), (15, 26), (5, 17)]
for a, m in inverse_examples:
    demonstrate_multiplicative_inverse(a, m)
    print()
```

## Euler's Totient Function Examples

### Computing φ(n)
```python
def euler_totient(n):
    """Compute Euler's totient function φ(n)."""
    if n == 1:
        return 1
    
    # Get prime factorization
    factors = prime_factorization(n)
    
    # Apply formula: φ(n) = n × ∏(1 - 1/p) for all prime factors p
    result = n
    for prime, _ in factors:
        result = result * (prime - 1) // prime
    
    return result

def count_coprimes(n):
    """Count integers from 1 to n that are coprime to n (brute force)."""
    count = 0
    for i in range(1, n + 1):
        if gcd(i, n) == 1:
            count += 1
    return count

# Test Euler's totient function
test_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 21]

print("n\tφ(n) (formula)\tφ(n) (count)\tMatch")
print("-" * 40)
for n in test_values:
    formula_result = euler_totient(n)
    count_result = count_coprimes(n)
    match = "✓" if formula_result == count_result else "❌"
    print(f"{n}\t{formula_result}\t\t{count_result}\t\t{match}")
```

### Euler's Theorem Verification
```python
def verify_euler_theorem(a, n):
    """Verify Euler's Theorem: a^φ(n) ≡ 1 (mod n) when gcd(a,n) = 1."""
    if gcd(a, n) != 1:
        return False, f"gcd({a}, {n}) ≠ 1"
    
    phi_n = euler_totient(n)
    result = modularExponentiation(a, phi_n, n)
    
    return result == 1, f"{a}^φ({n}) = {a}^{phi_n} ≡ {result} (mod {n})"

# Test Euler's Theorem
euler_test_cases = [
    (3, 10),  # gcd(3,10) = 1, φ(10) = 4, so 3^4 ≡ 1 (mod 10)
    (7, 12),  # gcd(7,12) = 1, φ(12) = 4, so 7^4 ≡ 1 (mod 12)
    (5, 21),  # gcd(5,21) = 1, φ(21) = 12, so 5^12 ≡ 1 (mod 21)
]

for a, n in euler_test_cases:
    is_valid, message = verify_euler_theorem(a, n)
    status = "✓" if is_valid else "❌"
    print(f"Euler's Theorem for a={a}, n={n}: {message} {status}")
```

## RSA Mathematical Foundation

### Key Generation Mathematics
```python
def rsa_key_generation_demo(p, q):
    """Demonstrate RSA key generation mathematics."""
    print(f"RSA Key Generation with p={p}, q={q}")
    print("-" * 40)
    
    # Check if p and q are prime
    if not (isPrime(p) and isPrime(q)):
        print("❌ Both p and q must be prime!")
        return
    
    # Compute n = p × q
    n = p * q
    print(f"n = p × q = {p} × {q} = {n}")
    
    # Compute φ(n) = (p-1)(q-1)
    phi_n = (p - 1) * (q - 1)
    print(f"φ(n) = (p-1)(q-1) = {p-1} × {q-1} = {phi_n}")
    
    # Choose e (commonly 65537)
    e = 65537
    if gcd(e, phi_n) != 1:
        e = 3  # Fallback for small examples
        while gcd(e, phi_n) != 1:
            e += 2
    
    print(f"Public exponent e = {e} (gcd(e, φ(n)) = {gcd(e, phi_n)})")
    
    # Compute d = e^(-1) mod φ(n)
    try:
        d = modularInverse(e, phi_n)
        print(f"Private exponent d = {d}")
        
        # Verify ed ≡ 1 (mod φ(n))
        verification = (e * d) % phi_n
        print(f"Verification: e × d ≡ {e} × {d} ≡ {verification} (mod {phi_n}) ✓")
        
        return (n, e), (n, d)
        
    except ValueError:
        print(f"❌ Cannot find modular inverse of {e} modulo {phi_n}")
        return None, None

# Small RSA example
print("Small RSA Example:")
public_key, private_key = rsa_key_generation_demo(17, 19)

if public_key and private_key:
    n, e = public_key
    n, d = private_key
    
    # Test encryption/decryption
    message = 42
    if message < n:
        print(f"\nTesting with message m = {message}")
        ciphertext = modularExponentiation(message, e, n)
        decrypted = modularExponentiation(ciphertext, d, n)
        
        print(f"Encryption: c ≡ {message}^{e} ≡ {ciphertext} (mod {n})")
        print(f"Decryption: m ≡ {ciphertext}^{d} ≡ {decrypted} (mod {n})")
        print(f"Success: {'✓' if decrypted == message else '❌'}")
```

## Running the Examples

To run these examples, save this content to a file called `examples.py` and run:

```bash
python examples.py
```

Make sure you have the `foundation.py` file with all the mathematical functions available in the same directory.

These examples demonstrate:
1. Prime number identification and testing
2. Prime factorization algorithms  
3. GCD computation and applications
4. Modular arithmetic operations
5. Verification of number theory theorems
6. Basic RSA key generation mathematics

Each example includes verification steps to ensure the mathematical operations are correct and help build intuition for the underlying concepts used in asymmetric cryptography.