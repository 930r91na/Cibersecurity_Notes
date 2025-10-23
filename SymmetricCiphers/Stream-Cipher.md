# Stream Ciphers — Introduction

A stream cipher encrypts plaintext one symbol (commonly one byte or one bit) at a time by combining it with a pseudorandom keystream. Stream ciphers are designed for high throughput, low latency, and low memory usage, making them suitable for streaming data, network protocols, and embedded devices.

Key points
- Works on a continuous stream of data (byte- or bit-wise).
- Keystream is generated from a secret key (and often an IV/nonce).
- Encryption = plaintext XOR keystream; decryption uses the same keystream.
- Security depends entirely on keystream unpredictability and correct key/IV management.

Common design goals
- Long period and good statistical properties of keystream.
- Resistance to known-plaintext, chosen-plaintext, and state-recovery attacks.
- Fast software/hardware implementation and low memory.

Examples
- One-time pad (information-theoretic secure when key = message and used once).
- RC4 (Ron's Code / Rivest Cipher 4) — historically popular but now deprecated due to biases.
- Salsa20 / ChaCha20 — modern, secure, and widely recommended stream ciphers.

## "Ron's Code" (RC4) — brief overview

RC4 (designed by Ron Rivest) is a byte-oriented stream cipher with two main parts:
1. Key-Scheduling Algorithm (KSA) — initializes a 256-byte state array S using the key.
2. Pseudo-Random Generation Algorithm (PRGA) — produces keystream bytes by permuting S and outputting bytes derived from S.

Why it's notable
- Simple and fast; used historically in TLS, WEP, and other protocols.
- Serious weaknesses: initial keystream bytes are biased, and RC4 is vulnerable to practical plaintext recovery attacks in many real-world uses.
- Recommendation: do not use RC4 in new designs — replace with ChaCha20, AES-GCM, or other modern ciphers.


Ci = Mi XOR StreamKeyi

### Example 
HI = Mi = Pi
          ASCII
M1 - H:   48hex     0100 1000
M2 - I:   49hex     0100 1001

Key Scheduling K1, K2
K1: 1010 1000
K1: 0101 0010

M1 xor K1 = E0hex
M2 xor K2 = 1Bhex



