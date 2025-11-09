# Asymmetric encryption

The keys are defined from two primes p and q.

- n = p * q
- Typical modulus sizes include 1024, 2048 and 4096 bits (implementation-dependent).

RSA flow

- A generates a key pair: public (Ka+) and private (Ka-).
- B generates a key pair: public (Kb+) and private (Kb-).

- A and B may publish or send their public keys to a trusted third party (TTP).
- The TTP can distribute certificates or key data (Ca, Cb) as needed.

- To send M to B, A computes the ciphertext C = E(Kb+, M).
- B recovers M by computing M = D(Kb-, C).

RSA key setup

1. Choose two distinct large primes p and q (keep them secret).
2. Compute n = p * q. The modulus n is used in both public and private keys.
3. Compute Euler's totient: phi(n) = (p - 1) * (q - 1).
4. Select an encryption exponent e with 1 < e < phi(n) and gcd(e, phi(n)) = 1.
5. Compute d as the modular inverse of e modulo phi(n): e * d ≡ 1 (mod phi(n)).
6. Public key: K+ = {e, n}. Private key: K- = {d, n}.

Example key setup (small numbers for illustration)

Imagine p = 17 and q = 11.

- n = p * q = 17 * 11 = 187
- phi(n) = (p - 1) * (q - 1) = 16 * 10 = 160

Select e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1.
For example, e = 7 is valid.

Compute d so that e * d ≡ 1 (mod 160). One solution is d = 23 because 7 * 23 = 161 ≡ 1 (mod 160).

So:

- Public key K+ = {e, n} = {7, 187}
- Private key K- = {d, n} = {23, 187}

If M = 88, then (textbook RSA):

Enc: C = M^e mod n

Dec: M = C^d mod n

(End of note)





