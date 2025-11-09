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

sbox_transformation = {
    0x43, 0x7E, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x99, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
}


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
            # i is 0 <= i <= 7
            c = 0x63
            transformed_byte = byte ^ ((byte >> 4) & 0x0F) ^ ((byte >> 5) & 0x0F) ^ ((byte >> 6) & 0x0F) ^ ((byte >> 7) & 0x0F) ^ c

            sbox[i][j] = transformed_byte & 0xFF  # Ensure byte is within 0-255


b_matrix_representation[8][8] = {
    [1, 0, 0, 0, 1, 1, 1, 1],   # b0
    [1, 1, 0, 0, 0, 1, 1, 1],  # b1
    [1, 1, 1, 0, 0, 0, 1, 1],  # b2
    [1, 1, 1, 1, 0, 0, 0, 1],  # b3
    [1, 1, 1, 1, 1, 0, 0, 0],  # b4
    [0, 1, 1, 1, 1, 1, 0, 0],  # b5
    [0, 0, 1, 1, 1, 1, 1, 0],  # b6
    [0, 0, 0, 1, 1, 1, 1, 1]  # b7
}

# c is always 0x63 = 01100011, to get the non linearity
c[8] =
{
    1, # c0
    1, # c1
    0, # c2
    0, # c3
    0, # c4
    1, # c5 
    1, # c6
    0 # c7
}

def create_Inverse_Sbox(hexIrreduciblePoly):


def test_Sbox():
    hexIrreduciblePoly = 0x11B  # x^8 + x^4 + x^3 + x + 1
    sbox = create_Sbox(hexIrreduciblePoly)
    # Theoretically compare with known S-box
    # Find  value in the generated S-box for the 0x11b
    theoric_value = sbox[1][0xA]  # Row 1, Column A
    print(f"S-box value at [1][A]: {value:02X}") 
    if theoric_value == sbox:
        print("S-box generation is correct.")
    else:
        print("S-box generation is incorrect.")
    


# 2 ShiftRows Step (SR Transformation)
# Causes diffusion over multiple rounds
# The rows of the state are shifted cyclically to the left

# 1st row is not shifted
# 2nd row is shifted left by 1 byte
# 3rd row is shifted left by 2 bytes
# 4th row is shifted left by 3 bytes

def shift_rows(state):
    # Shift the second row left by 1
    state[1] = state[1][1:] + state[1][:1]
    # Shift the third row left by 2
    state[2] = state[2][2:] + state[2][:2]
    # Shift the fourth row left by 3
    state[3] = state[3][3:] + state[3][:3]
    return state


# 3 MixColumns Step (MC Transformation)
# Each column of the state is treated as a polynomial in GF(2^8)
# The columns are mixed using a linear transformation
# This step provides additional diffusion by combining the bytes in each column

# The state matrix from the previous approach is the input of the following
# 4 x 4 matrix multiplication in GF(2^8) (xor & and operations)
# The state matrix will be multiplied by another fixed matrix
# The fixed matrix is defined as follows:

forward_transformation_matrix = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

inverse_transformation_matrix = [
    [0x0E, 0x0B, 0x0D, 0x09],
    [0x09, 0x0E, 0x0B, 0x0D],
    [0x0D, 0x09, 0x0E, 0x0B],
    [0x0B, 0x0D, 0x09, 0x0E]
]

# The forward transformation matrix * the inverse transformation matrix = Identity matrix

def mix_columns(state):
    # Perform constant matrix x state matrix multiplication
    new_state = matrix_multiplication(constant_matrix, state)
    return new_state

def matrix_multiplication(matA, matB):
    # Example for s0' = (02 * s0) ⊕ (03 * s1) ⊕ (01 * s2) ⊕ (01 * s3)
    # x * f(x) mod (x^8 + x^4 + x^3 + x + 1) 


    # Other technique is based on the fact that 
    # x^8 mod m(x) = x^4 + x^3 + x + 1 = m(x) - x^8

    # Multiplication by 0x02 or 0x03 can ve implemente as follows:
    # 1 left shift is equivalent to that multiplication 

    return result

def gf_mult(a, b):
    # Galois Field (2^8) multiplication
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        high_bit_set = a & 0x80
        a <<= 1
        if high_bit_set:
            a ^= 0x1B  # x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p % 256


# 4 AddRoundKey Step (ARK Transformation)
# Each byte of the state is combined with a byte of the round key using bitwise XOR
# This step is crucial for the security of the cipher as it introduces key dependency into the state
# The round keys are derived from the original key using a key schedule algorithm

def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state
