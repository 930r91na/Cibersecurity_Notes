# AES (Advanced Encryption Standard) Rijndael (Vincent Rijmen and Joan Daemen Belgium)
# AES is a symmetric block cipher
# Algebraic fundamentals:
#     1. Finite Field GF(2^8) 
#     2. Galois Field GF(2^8)
#     3. Prime numbers
#     4. Euclidian algorithm
#     5. Prime 

from Euclidean_GF_algorithm import extended_euclidean

# AES - symmetric block cipher 
# Block size: 128 bits (16 bytes) - the size of the plain text
# Kab + P  (AES) = C

# Input:
#   P - plain text (128 bits)
#  | 1N0 | 1N4 | 1N8 | 1N12|
#  | 1N1 | 1N5 | 1N9 | 1N13|
#  | 1N2 | 1N6 | 1N10| 1N14|
#  | 1N3 | 1N7 | 1N11| 1N15|
# In each column there are 4 bytes (32 bits)
# Process data as a block of 4 columns and 4 rows (4x4 matrix), 

# Kab - primary key (128 - 10 rounds, 192 - 12 rounds, 256 - 14 rounds)
# Iterative rather than feistel cipher
# 128 bits example
# k0 | k4 | k8 | k12|
# k1 | k5 | k9 | k13|
# k2 | k6 | k10| k14|
# k3 | k7 | k11| k15|

# Key is expanded to an array of words
# (44/54/60) words are generated
# Key sscheduling 


# 4 words will be used in each round 
# Each round undergoes to (9/11/13) rounds of processing
# 1. SubBytes - non-linear byte substitution using a substitution table (S-box)
# 2. ShiftRows - transposition step where each row of the state is shifted cyclic
# 3. MixColumns - mixing operation which operates on the columns of the state, combining the four bytes in each column
# 4. AddRoundKey - each byte of the state is combined with a byte of the round key using bitwise XOR

# The final round does not include the MixColumns step4


# AES-128
# 1 ARK with k0
# 9 rounds of (SB, SR, MC, ARK with k1 to k9)
# Final round of (SB, SR, ARK with k10)

# 1 SubBytes Step (SB Transformation)
# Each byte in the state is replaced with its corresponding byte from the S-box
# The S-box is designed to be resistant to known cryptanalytic attacks, it is created with a irreducible polynomial m(x)= x^8 + x^4 + x^3 + x + 1 = {0x11B0}
# It is constructed by combining the multiplicative inverse in GF(2^8) with an affine transformation
# This non linearity layer is crucial to fight cryptanalytic attacks

sbox_transformation = [
    43, 7E, 77, 7B, F2, 6B, 6F, C5, 30, 01, 67, 2B, FE, D7, AB, 76,
    CA, 82, C9, 7D, FA, 59, 47, F0, AD, D4, A2, AF, 9C, A4, 72, C0,
    B7, FD, 93, 26, 36, 3F, F7, CC, 34, A5, E5, F1, 71, D8, 31, 15,
    04, C7, 23, C3, 18, 96, 05, 9A, 07, 12, 80, E2, EB, 27, B2, 75,
    09, 83, 2C, 1A , 1B, 6E, 5A, A0, 52, 3B, D6, B3, 29, E3, 2F, 84,
    53, D1, 00, ED, 20, FC, B1, 5B, 6A, CB, BE, 39, 4A, 4C, 58, CF,
    D0, EF, AA, FB, 43, 4D, 33, 85, 45, F9, 02, 7F, 50, 3C, 9F, A8,
    51, A3, 40, 8F, 92, 99, 38, F5, BC, B6, DA, 21, 10, FF, F3, D2,
    CD, 0C, 13, EC, 5F, 97, 44, 17, C4, A7, 7E, 3D, 64, 5D, 19, 73,
    60, 81, 4F, DC, 22, 2A, 90, 88, 46, EE, B8, 14, DE, 5E, 0B, DB, 
    E0, 32, 3A, 0A, 49, 06, 24, 5C, C2, D3, AC, 62, 91, 95, E4, 79,
    E7, C8, 37, 6D, 8D, D5, 4E, A9, 6C, 56, F4, EA, 65, 7A, AE, 08,
    BA, 78, 25, 2E, 1C, A6, B4, C6, E8, DD, 74, 1F, 4B, BD, 8B, 8A,
    70, 3E, B5, 66, 48, 03, F6, 0E, 61, 35, 57, B9, 86, C1, 1D, 9E,
    E1, F8, 98, 11, 69, D9, 8E, 94, 9B, 1E, 87, E9, CE, 55, 28, DF,
    8C, A1, 89, 0D, BF, E6, 42, 68, 41, 99, 2D, 0F, B0, 54, BB, 16

]


# {1A} is row 1 column A -> Sbox transformation [1][A] = 7B
def create_Sbox(hexIrreduciblePoly):
    sbox = [] # 16x16 matrix indexed from 0 to F 
    # 1. Initialize S-box with byte values in ascending order by row 
    for i in range(16):
        row = []
        for j in range(16):
            byte = (i << 4) | j
            row.append(byte)
        sbox.append(row)

    # 2. Map each nonzero byte in the sbox to its multiplicative inverse in GF(2^8)
    for i in range(16):
        for j in range(16):
            byte = sbox[i][j]
            if byte != 0:
                inverse = extended_euclidean(byte, hexIrreduciblePoly)
                sbox[i][j] = inverse

    # 3. Apply GF(2) affine transformation to each byte in the sbox
    for i in range(16):
        for j in range(16):
            byte = sbox[i][j]
            # Affine transformation: b' = b ⊕ (b_{i+4} mod 8) ⊕ (b_{i+5} mod 8) ⊕ (b_{i+6} mod 8) ⊕ (b_{i+7} mod 8) ⊕ c
            # b' is the transformed byte, b is the original byte, and c is a constant (0x63)
            # The mod is 8 because we are dealing with bytes (8 bits) defined by prev step 2^8
            c = 0x63
            transformed_byte = byte ^ ((byte >> 4) & 0x0F) ^ ((byte >> 5) & 0x0F) ^ ((byte >> 6) & 0x0F) ^ ((byte >> 7) & 0x0F) ^ c

            sbox[i][j] = transformed_byte & 0xFF  # Ensure byte is within 0-255


def define_Sbox():
    sbox = [] # 16x16 matrix indexed from 0 to F 
    # Contains all 256 possible (permutation) byte values (0x00 to 0xFF)
    # {1A} is row 1 column A
    for i in range(16):
        row = []
        for j in range(16):
            byte = (i << 4) | j
            # Apply S-box transformation (substitution)
            transformed_byte = sbox_transformation(byte)
            row.append(transformed_byte)
        sbox.append(row)
    return sbox

# 2 ShiftRows Step (SR Transformation)
# Causes diffusion over multiple rounds
# The rows of the state are shifted cyclically to the left




# 3 MixColumns Step (MC Transformation)
# Each column of the state is treated as a polynomial in GF(2^8)
# The columns are mixed using a linear transformation
# This step provides additional diffusion by combining the bytes in each column




# 4 AddRoundKey Step (ARK Transformation)
# Each byte of the state is combined with a byte of the round key using bitwise XOR
# This step is crucial for the security of the cipher as it introduces key dependency into the state
# The round keys are derived from the original key using a key schedule algorithm


