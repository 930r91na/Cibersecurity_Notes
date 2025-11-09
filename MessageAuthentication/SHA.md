SHA

Secure Hash Algorithms (SHA) are a family of cryptographic hash functions that produce a fixed-size digest from an arbitrary-length message. They are used for integrity checking, signatures, and other cryptographic constructions.

Key SHA families and sizes
- SHA-1: 160-bit digest. (Deprecated — collision attacks make it unsuitable for most security uses.)
- SHA-2 family: includes SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224 and SHA-512/256. Digest sizes are the numbers in their names (e.g., SHA-256 → 256-bit digest).
  - SHA-256 and SHA-224 use 512-bit message blocks and 32-bit words.
  - SHA-384 and SHA-512 use 1024-bit message blocks and 64-bit words.
- SHA-3 (Keccak): a different sponge construction; supports the same digest sizes as SHA-2 (e.g., 224/256/384/512) but with different internal structure and parameters.

Notes on security and usage
- SHA-1: considered insecure for collision resistance; do not use for new designs.
- SHA-2 (SHA-256/SHA-512): currently secure and widely used.
- SHA-3: offers an alternative construction (sponge) and can be useful where different security properties or implementation trade-offs are desired.

What differs between SHA variants
- Digest size (output length).
- Internal word size (32-bit vs 64-bit).
- Block size (512 bits vs 1024 bits).
- Number of rounds / steps and the internal functions used in the compression function.

General structure (iterative hash / Merkle–Damgård-like / sponge)

Most SHA functions (SHA-1, SHA-2) follow an iterative compression pattern:

1. Pad the message to a length that is a multiple of the block size (includes message length encoding).
2. Parse the padded message into fixed-size blocks M_1, M_2, ..., M_n.
3. Initialize a chaining value (IV) — a fixed, algorithm-specific initial state.
4. For each block M_i, compute: IV = f(IV, M_i) where f is the compression function.
5. After the last block, output the final IV (or derive the digest from it) as the message digest.

In short: chaining value (IV) + compression function + block iteration -> final digest.

Pseudocode (high-level)

```
IV = IV0
for i in 1..n:
	IV = compress(IV, M_i)
digest = output_from(IV)
```

Compression function contract
- Inputs: chaining value (IV, fixed size), message block (M_i, fixed block size).
- Output: new chaining value (same size as IV).
- Goal: mix the message block with the IV so that small changes in input produce large unpredictable changes in output.

Character diagrams

Below are two plain-text diagrams that show the message processing flow and the IV/chaining update. They are drawn using ASCII characters and will render in any editor with a monospaced font.

Flow of message processing (ASCII)

```
Message
  |
  v
 +--------+
 | Padding|
 +--------+
  |
  v
 +---------------------------+
 | Parse into blocks M1..Mn  |
 +---------------------------+
  |
  v
 +--------------------+
 | Initialize IV (IV0)|
 +--------------------+
  |
  v
 +-------------------------------+
 | For each block Mi:            |
 |   IV = compress(IV, Mi)       |
 +-------------------------------+
  |
  v
 +--------------------+
 | Final IV / digest  |
 +--------------------+
```

State / chaining illustration (ASCII)

```
IV0 --compress(M1)--> IV1 --compress(M2)--> IV2 -- ... --compress(Mn)--> IVn
                      (after M1)            (after M2)                       (final)
```

Examples and quick facts
- SHA-1: block size 512 bits, digest 160 bits, word size 32 bits.
- SHA-256: block size 512 bits, digest 256 bits, word size 32 bits.
- SHA-512: block size 1024 bits, digest 512 bits, word size 64 bits.
- SHA-3 (Keccak): uses sponge construction with parameters bitrate r and capacity c; not based on the same compression function design.

Edge cases and notes
- Empty message: still produces a valid digest after padding and processing of the single (padded) block.
- Very long messages: processed block-by-block — memory usage is O(1) beyond the message block and IV state.
- Collision resistance degrades when an algorithm is broken; prefer SHA-2 or SHA-3 for collision resistance.

References / Further reading
- FIPS 180-4: "Secure Hash Standard" (SHA family specification)
- Keccak team: SHA-3 specification

How does f work?

The compression function f mixes the IV and the message block using a combination of operations: modular addition (mod 2^w), bitwise logical operations (AND, OR, XOR), and bit rotations/shifts. The exact sequence and constants depend on the SHA variant and are designed to provide diffusion and nonlinearity.





