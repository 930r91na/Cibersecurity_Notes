# Cryptography Class Notes & Implementations LIS4062

A comprehensive collection of cryptographic algorithms, mathematical foundations, and educational implementations for learning cybersecurity principles.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Symmetric Ciphers](#symmetric-ciphers)
- [Asymmetric Ciphers](#asymmetric-ciphers)

##  Overview

This repository serves as a complete educational resource for understanding cryptographic algorithms from the ground up. It includes:

- **Theoretical foundations** with mathematical explanations
- **Practical implementations** in Python with detailed comments
- **Working examples** demonstrating encryption and decryption
- **Debugging tools** for step-by-step algorithm visualization
- **Cryptanalysis techniques** for understanding cipher weaknesses
  

##  Repository Structure

```
.
├── SymmetricCiphers/
│   ├── Introduction.md              # Overview of symmetric cryptography
│   ├── Substitution-ciphers.py      # Caesar, Vigenère, Playfair, etc.
│   ├── Transposition-ciphers.py     # Rail Fence, Row Transposition
│   ├── DES-algorithm.py             # Data Encryption Standard
│   ├── 3DES-algorithm.py            # Triple DES
│   ├── AES-algorithm.py             # Advanced Encryption Standard (WIP)
│   ├── KE-DES-algorithm.py          # Key-Enhanced DES variant
│   ├── Stream-cipher.py             # RC4 and stream cipher concepts
│   ├── Block-Cipher-modes.py        # ECB, CBC, CFB, OFB, CTR modes
│   ├── Product-Ciphers.py           # Combined substitution-transposition
│   ├── Euclidean_GF_algorithm.py    # Mathematical foundations
│   ├── formatting_utils.py          # Display and formatting utilities
│   └── everything.py                # Unified CLI interface
│
├── AsymmetricCiphers/
│   ├── Introduction.md              # Public key cryptography overview
│   ├── Foundation.md                # Mathematical foundations
│   ├── foundation.py                # Number theory implementations
│   └── examples.py                  # Practical examples
│
└── .gitignore
```

##  Symmetric Ciphers

### Classical Ciphers

#### Substitution Ciphers
- **Caesar Cipher**: Simple shift cipher
- **Monoalphabetic**: Single substitution alphabet
- **Playfair Cipher**: Digraph substitution using 5×5 matrix
- **Vigenère Cipher**: Polyalphabetic cipher using keyword

#### Transposition Ciphers
- **Rail Fence**: Zigzag pattern transposition
- **Row Transposition**: Columnar transposition with keyword

### Modern Block Ciphers

#### DES (Data Encryption Standard)
```bash
# Encrypt with DES
python DES-algorithm.py

# Enable debug mode to see all 16 rounds
python DES-algorithm.py --debug
```

**Features:**
- 64-bit blocks, 56-bit effective key
- 16 rounds of Feistel network
- Complete implementation with all permutations and S-boxes
- Step-by-step visualization available

#### 3DES (Triple DES)
- Applies DES three times
- Supports 2-key and 3-key modes
- 112-bit or 168-bit effective key strength

#### AES (Advanced Encryption Standard)
- Rijndael algorithm implementation (in progress)
- 128, 192, or 256-bit keys
- Substitution-Permutation Network structure

### Stream Ciphers
- RC4 algorithm concepts
- Key scheduling algorithm (KSA)
- Pseudo-random generation algorithm (PRGA)

##  Asymmetric Ciphers

### Mathematical Foundations

The `Foundation.md` file covers essential number theory:

#### Prime Numbers
- Primality testing (trial division, Miller-Rabin)
- Prime factorization
- Fundamental theorem of arithmetic

#### Number Theory
- Greatest Common Divisor (Euclidean algorithm)
- Coprime numbers and properties
- Modular arithmetic

#### Key Theorems
- **Fermat's Little Theorem**: `a^(p-1) ≡ 1 (mod p)`
- **Euler's Theorem**: `a^φ(n) ≡ 1 (mod n)`
- 
#### Galois Fields
- Finite field arithmetic (GF(2^8))
- Polynomial operations
- Multiplicative inverses


##  References

Some of the notes and comments are from the class material LIS4062 Information Security
- FIPS 46-3: Data Encryption Standard (DES)
- FIPS 197: Advanced Encryption Standard (AES)
- RFC 2104: HMAC: Keyed-Hashing for Message Authentication
- "Applied Cryptography" by Bruce Schneier
- "Cryptography and Network Security" by William Stallings
