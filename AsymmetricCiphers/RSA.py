"""RSA — concise notes and an educational demo

This file contains a short, corrected explanation of RSA (asymmetric public-key
encryption) together with a small, self-contained example using small primes
for educational purposes.

Important corrections and notes:
- Correct n for p=17 and q=11 is n = 17 * 11 = 187 (not 197).
- Euler's totient phi(n) = (p-1)*(q-1) = 16 * 10 = 160.
- Choose e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1 (e is coprime to phi).
- Compute d as the modular inverse of e modulo phi(n): e * d ≡ 1 (mod phi(n)).

Practical notes (summary):
- Real RSA uses large primes (2048, 3072, 4096 bits) and secure padding
  (e.g. OAEP) before encryption. Do not use textbook RSA in production.
- For correctness proofs you can use Euler's theorem or Carmichael's lambda
  function (λ(n)) instead of phi(n) in some analyses.

Example (small educational values):
- p = 17, q = 11
- n = p * q = 187
- phi(n) = (p - 1) * (q - 1) = 160
- choose e = 7 (gcd(7, 160) = 1)
- compute d such that 7 * d ≡ 1 (mod 160) → d = 23, because 7*23 = 161 ≡ 1 (mod 160)

Public key  PU = (e, n) = (7, 187)
Private key PR = (d, n) = (23, 187)

If M = 88 (message as an integer < n):
- Encryption:  C = M^e mod n = pow(88, 7, 187) = 11
- Decryption:  M = C^d mod n = pow(11, 23, 187) = 88

The demonstration code below shows the calculations programmatically and
contains small helper functions (extended gcd and modular inverse) used for
educational key generation.
"""

from typing import Tuple


def egcd(a: int, b: int) -> Tuple[int, int, int]:
	"""Extended Euclidean Algorithm.

	Returns a tuple (g, x, y) such that a*x + b*y = g = gcd(a, b).
	"""
	if b == 0:
		return (a, 1, 0)
	g, x1, y1 = egcd(b, a % b)
	return (g, y1, x1 - (a // b) * y1)


def modinv(a: int, m: int) -> int:
	"""Modular inverse: find x such that (a * x) % m == 1.

	Raises ValueError if the inverse does not exist.
	"""
	g, x, _ = egcd(a, m)
	if g != 1:
		raise ValueError(f"modular inverse does not exist for {a} modulo {m}")
	return x % m


def generate_example_keys(p: int, q: int, e: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
	"""Generate a small RSA keypair (public, private) for demonstration.

	Returns (public_key, private_key) where each is a tuple (exponent, n).
	This is for educational purposes only and uses small primes.
	"""
	if p == q:
		raise ValueError("p and q must be distinct primes")
	n = p * q
	phi = (p - 1) * (q - 1)
	if e <= 1 or e >= phi:
		raise ValueError("e must satisfy 1 < e < phi(n)")
	# Verify e is coprime to phi
	g, _, _ = egcd(e, phi)
	if g != 1:
		raise ValueError("e must be coprime to phi(n)")
	d = modinv(e, phi)
	return (e, n), (d, n)


def encrypt(public_key: Tuple[int, int], message: int) -> int:
	e, n = public_key
	if not (0 <= message < n):
		raise ValueError("message must be an integer in range 0 <= M < n")
	return pow(message, e, n)


def decrypt(private_key: Tuple[int, int], ciphertext: int) -> int:
	d, n = private_key
	return pow(ciphertext, d, n)


def demo() -> None:
	# Small example matching the notes above
	p, q = 17, 11
	e = 7
	public, private = generate_example_keys(p, q, e)
	n = public[1]
	phi = (p - 1) * (q - 1)

	print("RSA educational demo (small numbers)")
	print(f"p={p}, q={q}")
	print(f"n = p*q = {n}")
	print(f"phi(n) = (p-1)*(q-1) = {phi}")
	print(f"public key (e, n) = {public}")
	print(f"private key (d, n) = {private}")

	M = 88
	C = encrypt(public, M)
	M2 = decrypt(private, C)
	print(f"Original message M = {M}")
	print(f"Encrypted ciphertext C = M^e mod n = {C}")
	print(f"Decrypted message = C^d mod n = {M2}")


if __name__ == "__main__":
	demo()





