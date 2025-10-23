# Mathematical Foundations of Asymmetric Cryptography

## Number Theory Fundamentals

### Prime Numbers

**Definition**: A prime number is a natural number $p \in \mathbb{N}$ such that $p \geq 2$ and the only positive divisors of $p$ are $1$ and $p$ itself.

**Formal Definition**: $p$ is prime if and only if:
- $p \geq 2$
- For any $a, b \in \mathbb{N}$, if $p = a \cdot b$, then either $a = 1$ or $b = 1$

### Classification of Natural Numbers

Positive integers can be classified into three categories:

1. **Unit**: The number $1$ (neither prime nor composite)
2. **Prime Numbers**: Natural numbers with exactly two positive divisors ($1$ and itself)
3. **Composite Numbers**: Natural numbers with more than two positive divisors

**Examples**:
- Primes: $2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ...$
- Composites: $4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, ...$

### Primality Testing

**Trial Division Method**: A number $n$ can be determined to be prime by checking if it's divisible by any prime number $p$ where $p \leq \sqrt{n}$.

**Rationale**: If $n$ has a divisor $d > \sqrt{n}$, then $n/d < \sqrt{n}$, so we would have already found the smaller divisor.

**Algorithm**:
1. Check if $n \leq 1$ (not prime)
2. Check if $n = 2$ (prime)
3. Check if $n$ is even (not prime if $n > 2$)
4. Test divisibility by odd numbers from $3$ to $\sqrt{n}$

## Prime Factorization

**Fundamental Theorem of Arithmetic**: Every integer greater than $1$ can be uniquely represented as a product of prime powers.

**Mathematical Representation**: For any composite number $n$:
$$n = p_1^{a_1} \cdot p_2^{a_2} \cdot ... \cdot p_k^{a_k}$$

where $p_1 < p_2 < ... < p_k$ are distinct primes and $a_i \geq 1$ for all $i$.

**Example**: 
- $60 = 2^2 \cdot 3^1 \cdot 5^1$
- $1001 = 7^1 \cdot 11^1 \cdot 13^1$

### Cryptographic Importance
- **RSA Security**: Based on difficulty of factoring large composite numbers
- **Key Generation**: Requires finding large prime factors
- **Computational Complexity**: No known efficient classical algorithm for large numbers

## Coprime Numbers (Relatively Prime)

**Definition**: Two integers $a$ and $b$ are coprime (or relatively prime) if their greatest common divisor is $1$.

**Mathematical Notation**: $\gcd(a, b) = 1$

### Properties of Coprime Numbers

1. **Prime Pairs**: Any two distinct prime numbers are always coprime
   - Example: $\gcd(7, 11) = 1$

2. **Even Numbers**: Two even numbers are never coprime (both divisible by $2$)
   - Example: $\gcd(6, 8) = 2 \neq 1$

3. **Unity Property**: The number $1$ is coprime to every positive integer
   - $\gcd(1, n) = 1$ for any $n \in \mathbb{N}$

4. **Consecutive Integers**: Any two consecutive integers are always coprime
   - $\gcd(n, n+1) = 1$ for any $n \in \mathbb{N}$
   - **Proof**: If $d | n$ and $d | (n+1)$, then $d | ((n+1) - n) = 1$, so $d = 1$

5. **Coprime vs Prime**: Coprime numbers are not necessarily prime themselves
   - Example: $\gcd(9, 16) = 1$, but neither $9$ nor $16$ is prime

### Applications in Cryptography
- **RSA Key Generation**: $e$ and $\phi(n)$ must be coprime
- **Modular Arithmetic**: Enables multiplicative inverses
- **Key Security**: Ensures mathematical operations are reversible

## Fermat's and Euler's Theorems

### Fermat's Little Theorem

**Statement**: If $p$ is prime and $a$ is not divisible by $p$, then:
$$a^{p-1} \equiv 1 \pmod{p}$$

**Conditions**:
- $p$ is prime
- $\gcd(a, p) = 1$

**Equivalent Form**: $a^p \equiv a \pmod{p}$ for any integer $a$

#### Applications
1. **Primality Testing**: If $a^{p-1} \not\equiv 1 \pmod{p}$, then $p$ is composite
2. **Modular Exponentiation**: Reduces large exponents
3. **Multiplicative Inverse**: $a^{p-2} \equiv a^{-1} \pmod{p}$

**Finding Multiplicative Inverse using Fermat's Little Theorem**:
If $\gcd(a, p) = 1$ and $p$ is prime, then:
$$a^{-1} \equiv a^{p-2} \pmod{p}$$

**Example**: Find $3^{-1} \bmod 7$
- $3^{-1} \equiv 3^{7-2} \equiv 3^5 \equiv 243 \equiv 5 \pmod{7}$
- Verification: $3 \cdot 5 = 15 \equiv 1 \pmod{7}$ ✓

### Euler's Theorem

**Euler's Totient Function**: $\phi(n)$ counts the number of integers from $1$ to $n$ that are coprime to $n$.

**Formula for Prime Powers**:
- If $p$ is prime: $\phi(p) = p - 1$
- If $p^k$ is a prime power: $\phi(p^k) = p^k - p^{k-1} = p^{k-1}(p-1)$
- If $n = p \cdot q$ where $p, q$ are distinct primes: $\phi(n) = (p-1)(q-1)$

**Euler's Theorem**: If $\gcd(a, n) = 1$, then:
$$a^{\phi(n)} \equiv 1 \pmod{n}$$

**Relationship to Fermat**: Euler's theorem generalizes Fermat's Little Theorem (when $n$ is prime, $\phi(n) = n-1$)

#### Applications in RSA

1. **Key Generation**: Choose $e$ such that $\gcd(e, \phi(n)) = 1$
2. **Private Key**: Find $d$ such that $ed \equiv 1 \pmod{\phi(n)}$
3. **Encryption/Decryption**: 
   - Encrypt: $c \equiv m^e \pmod{n}$
   - Decrypt: $m \equiv c^d \pmod{n}$

**RSA Correctness Proof**:
$$c^d \equiv (m^e)^d \equiv m^{ed} \equiv m^{1 + k\phi(n)} \equiv m \cdot (m^{\phi(n)})^k \equiv m \cdot 1^k \equiv m \pmod{n}$$

## Advanced Topics

### Chinese Remainder Theorem (CRT)

**Application**: Speeds up RSA decryption by factor of 4

**Method**: Instead of computing $m = c^d \bmod n$, compute:
- $m_1 = c^{d_1} \bmod p$ where $d_1 = d \bmod (p-1)$
- $m_2 = c^{d_2} \bmod q$ where $d_2 = d \bmod (q-1)$
- Combine using CRT to get $m$

### Quadratic Residues

**Definition**: $a$ is a quadratic residue modulo $p$ if there exists $x$ such that $x^2 \equiv a \pmod{p}$

**Legendre Symbol**: $\left(\frac{a}{p}\right) = a^{(p-1)/2} \bmod p$

**Applications**: Used in some cryptographic protocols and primality tests

### Discrete Logarithm Problem

**Problem**: Given $g$, $p$, and $y = g^x \bmod p$, find $x$

**Cryptographic Importance**: Foundation of Diffie-Hellman key exchange and ElGamal encryption

**Relationship to RSA**: While RSA relies on factoring, DH/ElGamal rely on discrete logarithms