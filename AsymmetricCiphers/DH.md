# Diffie–Hellman (DH) — concise notes

## Purpose
- Establish a shared secret between two parties over an insecure channel.
- Provides confidentiality foundation for symmetric encryption; does not provide authentication/confidentiality by itself.

## Math prerequisites
- Choose a large prime p and a generator g of a multiplicative subgroup modulo p.
- Operations are modular exponentiation in Zp*.

## Basic protocol (finite-field DH)
1. Alice picks secret a, computes A = g^a mod p, sends A to Bob.  
2. Bob picks secret b, computes B = g^b mod p, sends B to Alice.  
3. Shared secret S = A^b mod p = B^a mod p = g^(ab) mod p.

## Small numeric example
- p = 23, g = 5  
- Alice: a = 6 → A = 5^6 mod 23 = 8  
- Bob: b = 15 → B = 5^15 mod 23 = 19  
- Alice computes S = 19^6 mod 23 = 2  
- Bob computes S = 8^15 mod 23 = 2

## Minimal Python example
```python
p = 23
g = 5
a = 6
b = 15
A = pow(g, a, p)
B = pow(g, b, p)
S_alice = pow(B, a, p)
S_bob = pow(A, b, p)
assert S_alice == S_bob
```

## Security properties and threats
- Security relies on hardness of the discrete logarithm problem (DLP) in chosen group.
- Vulnerable to active Man-in-the-Middle (MITM) unless parties authenticate keys or messages.
- Other attacks: small-subgroup confinement, invalid-parameter attacks, side channels, precomputation for weak/moderate primes.

## Mitigations / best practices
- Use authenticated DH (e.g., sign/verify public values or use authenticated protocols like TLS).  
- Use standard, well-known groups (RFC 7919 finite-field groups or standard elliptic curves).  
- Validate public keys (check 1 < value < p−1 and subgroup membership when needed).  
- Prefer ephemeral keys for forward secrecy (DHE/ECDHE).  
- Use sufficiently large parameters: at least 2048-bit modular p, or prefer elliptic-curve DH (Curve25519, P-256, etc.) for better security/performance.

## Variants
- Ephemeral DH (DHE): new DH key pair per session → forward secrecy.  
- Static DH: long-term DH keys (no forward secrecy).  
- Elliptic Curve Diffie–Hellman (ECDH): same concept on elliptic curves — smaller keys and faster.  
- X25519 / Curve25519: recommended modern ECDH primitive.

## Implementation tips
- Use vetted cryptographic libraries; avoid implementing low-level ops yourself.  
- Ensure constant-time exponentiation implementations to reduce side channels.  
- Combine shared secret with an HKDF / KDF before use as symmetric key material.

## Summary
- DH establishes a shared secret securely against passive eavesdroppers but requires authentication to prevent active attacks.  
- Prefer modern curve-based primitives (e.g., X25519) or standardized large-group parameters and always use authenticated channels and KDFs for keys.