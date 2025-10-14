# Introduction
# Data Encryption Standard (DES) is a symmetric-key algorithm for the encryption of digital data.
# It operates on fixed-size blocks of data (64 bits) and uses a 56-bit key for encryption and decryption.
# DES is based on a Feistel network structure and consists of multiple rounds of permutation and substitution operations.
# It is a block cipher type

# USAGE MODES:
#   Normal Mode:    python DES-algorithm.py
#                   Shows concise summary with key generation, encrypted/decrypted results
#   
#   Debug Mode:     python DES-algorithm.py --debug
#                   Shows detailed step-by-step execution including all intermediate values
#                   Useful for learning, debugging, and understanding the algorithm flow 

# Import formatting utilities for better output display
import time
import sys
from formatting_utils import (
    format_binary_grouped,
    binary_to_hex,
    print_section_header,
    print_binary_data,
    print_step_header
)

# Global debug flag - set to True for detailed step-by-step output, False for summary only
DEBUG_MODE = False

# Block cypher example
# Message to be encrypted is processed in blocks of fixed size (64 bits for DES)
# Then 1 to 1 mapping of plaintext blocks to ciphertext blocks

# Example if block size is 3 bits then the association could be
# Plaintext   |    Ciphertext
# 000         |    101
# 001         |    010  
# 010         |    111
# 011         |    000
# 100         |    001
# 101         |    100
# 110         |    011
# 111         |    110

# And then decoder and encoder would be used to convert the blocks
# Problems: The possible mappings for n is 3 
# 2^n! = 8! = 40320 possible mappings
# For the block size of 64 bits that is used in DES this would be 2^64! possible mappings
# This is infeasible to store or compute all possible mappings

# Therefore, the Feistel cipher structure is used making the mapping from 2^64! to 2^64 
# This is done by alternating substitution and permutation operations on the data blocks

# Claude Shannon and Substitution-Permutation Ciphers
# Claude Shannon introduced the concept of confusion and diffusion in cryptography
# Substitution-Permutation Networks (SPN) are a class of symmetric key algorithms that use a series of linked mathematical operations

# Substitution: Replacing bits, characters, or blocks of data with other bits, characters, or blocks
# Provides: Confusion
# Confusion: Making the relationship between the **key** and **ciphertext** as complex as possible

# Permutation: Rearranging the bits, characters, or blocks of data
# Provides: Diffusion
# Diffusion: Spreading the influence of a single **plaintext bit** over many **ciphertext bits**. Makes patterns less discernible, no statistical analysis possible


# FEISTEL CIPHER STRUCTURE

# Number of identical rounds
# Each round a mangler function is applied, and a substitution is performed in one half of the data block
# After that a permutation interchanges the two halves of the data block
# The keys for each round are derived from the main key using a key schedule

# Feistel Cipher design principles
# Increasing block size, key size, and number of
# rounds will improve security. The subkey generation
# and round function will make analysis harder.
# However, all of them slow the cipher; therefore, there
# is a trade off between security and complexity.

# Plaintext (P) is divided into two halves (L0 and R0)
# For each round i from 1 to n:
#   Li = Ri-1
#   Ri = Li-1 XOR F(Ri-1, Ki)
# Where F is the round function and Ki is the subkey for round i
# After the final round, the two halves are concatenated to form the ciphertext (C)


# DES Challenge: 56-bit-key-encrypted phrase decrypted (brute force) in less than a day
# No good cryptanalysis found against DES
# 3DES (Triple DES) - applying DES three times with either two or three different keys

# ================================ Implementation of DES Algorithm ================================

# Code step by step to encrypt and decrypt a DES (Symmetric encryption - Kab)
# Encrypt process
# Assumption Kab is preshared by the parts
# Input:
#   P - plain text (64 bits)
#   Kab - primary key (64 bits)
# Output:
#   C - cyphered text (64 bits)


# Definition of the S-boxes
S1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
]
S2 = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
]

S3 = [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
]

S4 = [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
]

S5 = [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
]

S6 = [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
]

S7 = [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
]

S8 = [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]


# Initial Permutation (IP) table
# The initial permutation (IP) is a fixed permutation of the bits of the 64-bit plaintext block
# X = IP(P)
# Y = IP^-1(C) (Inverse of the initial permutation)

# This means the first bit of the output is the 58th bit of the input, the second bit of the output is the 50th bit of the input, and so on.
IP_table = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Inverse Initial Permutation (IP-1) table, this is the inverse of the initial permutation (IP)
IP_inverse_table = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

def apply_IP(text64):
    """Apply the initial permutation (IP) over the original 64-bit text message."""
    return [text64[i - 1] for i in IP_table]

def apply_IP_inverse(text64):
    """Apply the inverse of the initial permutation"""
    return [text64[i - 1] for i in IP_inverse_table]

# Expansion (E) table permutation
# The expansion permutation expands the 32-bit half-block to 48 bits by duplicating some bits
E_table = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

def apply_expansion(block32):
    """Expand a 32-bit block to 48 bits using the E table."""
    return [block32[i - 1] for i in E_table]

# P-Permutation table for the Feistel function
# After S-box substitution, the 32-bit output is permuted using the P table
P_table = [
    16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25
]

def apply_P_permutation(block32):
    """Apply the P permutation to a 32-bit block."""
    return [block32[i - 1] for i in P_table]


# Feistel function (F)
# The Feistel function (F) takes a 32-bit half-block and a 48-bit subkey as input and produces a 32-bit output

def feistel_function(R, K):
    """Feistel function F that takes a 32-bit half-block R and a 48-bit subkey K."""

    if DEBUG_MODE:
        print("      🔄 FEISTEL FUNCTION DETAILS")
        print_binary_data("      Input R", R, show_hex=False)
        print_binary_data("      Input K", K, show_hex=False)
    
    # Step 1: Expand R from 32 to 48 bits
    expanded_R = apply_expansion(R)
    if DEBUG_MODE:
        print("\n      📈 Expansion:")
        print_binary_data("      Expanded R", expanded_R, show_hex=False)

    # Step 2: XOR with the subkey K
    xor_result = [expanded_R[i] ^ K[i] for i in range(48)]
    if DEBUG_MODE:
        print("\n      ⊕ XOR with subkey:")
        print_binary_data("      XOR result", xor_result, show_hex=False)
    
    # Step 3: Apply the S-boxes
    if DEBUG_MODE:
        print("\n      📦 S-BOX SUBSTITUTIONS:")
    sbox_output = []
    for i in range(8):
        block = xor_result[i*6:(i+1)*6]
        
        # Ensure all values in block are 0 or 1
        if any(bit not in [0, 1] for bit in block):
            if DEBUG_MODE:
                print(f"      ERROR: Block contains non-binary values: {block}")
            return None
            
        row = (block[0] << 1) | block[5]
        col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
        
        if i == 0:
            sbox_value = S1[row][col]
        elif i == 1:
            sbox_value = S2[row][col]
        elif i == 2:
            sbox_value = S3[row][col]
        elif i == 3:
            sbox_value = S4[row][col]
        elif i == 4:
            sbox_value = S5[row][col]
        elif i == 5:
            sbox_value = S6[row][col]
        elif i == 6:
            sbox_value = S7[row][col]
        elif i == 7:
            sbox_value = S8[row][col]
        
        if DEBUG_MODE:
            print(f"      S{i+1}: {format_binary_grouped(block, 6)} → Row {row}, Col {col:2d} → {sbox_value:2d} → {format_binary_grouped([(sbox_value >> j) & 1 for j in reversed(range(4))], 4)}")
        sbox_output.extend([(sbox_value >> j) & 1 for j in reversed(range(4))])
    
    # Step 4: Apply the P permutation (CRITICAL for DES security!)
    if DEBUG_MODE:
        print("\n      🔄 P-PERMUTATION:")
        print_binary_data("      Before P", sbox_output, show_hex=False)
    
    # Apply P-permutation to the 32-bit S-box output
    p_output = apply_P_permutation(sbox_output)
    if DEBUG_MODE:
        print_binary_data("      After P", p_output, show_hex=False)
    
    return p_output


# NOTE: The S boxes and the non linear transformation are crucial for the security of DES.
# They provide the necessary confusion and diffusion properties that make DES resistant to various cryptanalytic attacks.
# S1(X1) xor S2(X2) not equal to S1(X1 xor X2) this means non linearity

def exemplify_non_linearity(Sbox, X1, X2):
    """Demonstrate the non-linearity of an S-box."""
    # Convert input lists to binary strings
    def bits_to_int(bits):
        return sum(bit << (len(bits) - 1 - i) for i, bit in enumerate(bits))
    
    def int_to_bits(value, length):
        return [(value >> (length - 1 - i)) & 1 for i in range(length)]
    
    print(f"📋 S-BOX NON-LINEARITY ANALYSIS")
    print(f"X1 = {X1} → {format_binary_grouped(X1, 6)}")
    print(f"X2 = {X2} → {format_binary_grouped(X2, 6)}")
    
    # Extract row and column for X1
    row1 = bits_to_int([X1[0], X1[5]])
    col1 = bits_to_int(X1[1:5])
    print(f"\n🔍 X1 Analysis:")
    print(f"   Row bits: [{X1[0]}, {X1[5]}] = {row1}")
    print(f"   Col bits: {X1[1:5]} = {col1}")
    
    # Calculate S(X1) and S(X2)
    S_X1 = Sbox[row1][col1]
    print(f"   S(X1) = S-box[{row1}][{col1}] = {S_X1}")
    
    # Extract row and column for X2
    row2 = bits_to_int([X2[0], X2[5]])
    col2 = bits_to_int(X2[1:5])
    print(f"\n🔍 X2 Analysis:")
    print(f"   Row bits: [{X2[0]}, {X2[5]}] = {row2}")
    print(f"   Col bits: {X2[1:5]} = {col2}")
    
    S_X2 = Sbox[row2][col2]
    print(f"   S(X2) = S-box[{row2}][{col2}] = {S_X2}")
    
    # Calculate S(X1) XOR S(X2)
    S_X1_XOR_S_X2 = S_X1 ^ S_X2
    print(f"\n⊕ S(X1) XOR S(X2):")
    print(f"   {S_X1} ⊕ {S_X2} = {S_X1_XOR_S_X2}")
    
    # Calculate X1 XOR X2
    X1_XOR_X2 = [X1[i] ^ X2[i] for i in range(6)]
    print(f"\n⊕ X1 XOR X2:")
    print(f"   {X1} ⊕ {X2} = {X1_XOR_X2} → {format_binary_grouped(X1_XOR_X2, 6)}")
    
    # Extract row and column for X1 XOR X2
    row_xor = bits_to_int([X1_XOR_X2[0], X1_XOR_X2[5]])
    col_xor = bits_to_int(X1_XOR_X2[1:5])
    print(f"\n🔍 (X1 XOR X2) Analysis:")
    print(f"   Row bits: [{X1_XOR_X2[0]}, {X1_XOR_X2[5]}] = {row_xor}")
    print(f"   Col bits: {X1_XOR_X2[1:5]} = {col_xor}")
    
    # Calculate S(X1 XOR X2)
    S_X1_XOR_X2 = Sbox[row_xor][col_xor]
    print(f"   S(X1 XOR X2) = S-box[{row_xor}][{col_xor}] = {S_X1_XOR_X2}")
    
    print(f"\n🎯 NON-LINEARITY RESULT:")
    print(f"   S(X1) ⊕ S(X2) = {S_X1_XOR_S_X2}")
    print(f"   S(X1 ⊕ X2)    = {S_X1_XOR_X2}")
    
    if S_X1_XOR_S_X2 != S_X1_XOR_X2:
        print(f"   ✅ NON-LINEAR: S(X1) ⊕ S(X2) ≠ S(X1 ⊕ X2) ({S_X1_XOR_S_X2} ≠ {S_X1_XOR_X2})")
    else:
        print(f"   ❌ LINEAR: S(X1) ⊕ S(X2) = S(X1 ⊕ X2) ({S_X1_XOR_S_X2} = {S_X1_XOR_X2})")
    
    return S_X1_XOR_S_X2, S_X1_XOR_X2

# =============================== Key Generation ===============================
# Key Generation (Kab -> Ki for i=1 to 16 (The subkeys needed for each round))

# From the primary key Kab (64 bits) generate 16 subkeys Ki (48 bits)
# Rules:
#   - Apply the PC-1  (Permuted Choice 1) table to the primary key Kab to get a 56-bit key K+ (Every 8th bit is ignored - parity bits)
#   - Split K+ into two 28-bit halves (C0 and D0)
#   - Apply rotation to each half (Ci and Di) according to the round number i
#   - Apply the PC-2 table to the concatenated halves (Ci and Di) to get the 48-bit subkey Ki
#   - Repeat the process for 16 rounds to get K1 to K16
# Input: Kab (64 bits)
# Output: List of 16 subkeys [K1, K2, ..., K16] (each 48 bits)

# Example of Kab, the 64-bit primary key
Kab = [
    1, 2 , 3, 4, 5, 6, 7, 8,
    9, 10, 11, 12, 13, 14, 15, 16,
    17, 18, 19, 20, 21, 22, 23, 24,
    25, 26, 27, 28, 29, 30, 31, 32,
    33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48,
    49, 50, 51, 52, 53, 54, 55, 56, 
    57, 58, 59, 60, 61, 62, 63, 64
]

# Remove parity bit
def removeParityBit(Kab):
    # Delete the last column will imply to remove MSB 
    KabOf56bits = []
    for i in range(64):
        # Every 8th bit is a parity bit (MSB)
        if (i+1) % 8 != 0:
            KabOf56bits.append(Kab[i])
    return KabOf56bits


# Apply PC-1 (Permuted Choice 1)
def applyPC1(Kab64bits):
    # PC-1 permutation table (selects and rearranges 56 bits from 64-bit key)
    # The table values are 1-indexed, so we subtract 1 for 0-indexed arrays
    # Note: PC-1 automatically excludes parity bits (positions 8,16,24,32,40,48,56,64)
    PC1_table = [
        57, 49, 41, 33, 25, 17,  9,  1,
        58, 50, 42, 34, 26, 18, 10,  2,
        59, 51, 43, 35, 27, 19, 11,  3,
        60, 52, 44, 36, 63, 55, 47, 39,
        31, 23, 15,  7, 62, 54, 46, 38,
        30, 22, 14,  6, 61, 53, 45, 37,
        29, 21, 13,  5, 28, 20, 12,  4
    ]
    
    # Apply PC-1 permutation to 64-bit key
    permuted_key = []
    for position in PC1_table:
        # PC-1 table is 1-indexed, convert to 0-indexed
        permuted_key.append(Kab64bits[position - 1])
    
    return permuted_key

# Divide the key between Ci and Di
def divideKey(KabOf56bits):
    # Ci = first 28 bits
    # Di = last 28 bits
    C0 = KabOf56bits[0:28]
    D0 = KabOf56bits[28:56]
    return C0, D0


def rotateLeft(bits, n):
    # Rotate the bits to the left by n positions
    return bits[n:] + bits[:n]


def applyPC2(Ci, Di):
    # PC-2 permutation table (selects 48 bits from 56-bit input)
    # The table values are 1-indexed, so we subtract 1 for 0-indexed arrays
    PC2_table = [
        14, 17, 11, 24,  1,  5,  3, 28,
        15,  6, 21, 10, 23, 19, 12,  4,
        26,  8, 16,  7, 27, 20, 13,  2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32
    ]
    
    # Concatenate Ci and Di to form 56-bit key
    combined_key = Ci + Di
    
    # Apply PC-2 permutation to get 48-bit subkey
    Ki = []
    for position in PC2_table:
        # PC-2 table is 1-indexed, convert to 0-indexed
        Ki.append(combined_key[position - 1])
    
    return Ki 


def generateSubkeys(Kab):
    # Apply PC-1 directly to 64-bit key (PC-1 automatically selects non-parity bits)
    if DEBUG_MODE:
        print_section_header("KEY GENERATION")
        print_binary_data("Original Key Kab (64 bits)", Kab)

    KabOf56bits = applyPC1(Kab)
    if DEBUG_MODE:
        print_binary_data("Key after PC-1 (56 bits)", KabOf56bits)

    # Divide the key into two halves
    C0, D0 = divideKey(KabOf56bits)

    if DEBUG_MODE:
        print_binary_data("C0 (28 bits)", C0)
        print_binary_data("D0 (28 bits)", D0)

    # List to hold the 16 subkeys
    subkeys = []

    # Number of left shifts for each round (DES rotation schedule)
    shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    # Generate 16 subkeys
    for i in range(16):
        if DEBUG_MODE:
            print_step_header(i + 1, f"Round {i + 1} Key Generation")
            # Rotate Ci and Di
            print(f"  Left shift by {shifts[i]} positions")
        C0 = rotateLeft(C0, shifts[i])

        if DEBUG_MODE:
            print_binary_data(f"C{i+1} (28 bits)", C0)

        D0 = rotateLeft(D0, shifts[i])
        if DEBUG_MODE:
            print_binary_data(f"D{i+1} (28 bits)", D0)

        # Apply PC-2 to get the subkey Ki
        Ki = applyPC2(C0, D0)
        if DEBUG_MODE:
            print_binary_data(f"Subkey K{i+1} (48 bits)", Ki)
        subkeys.append(Ki)
    
    return subkeys

def divide_text(chunk64bits):
    """Returns Li and Ri"""
    Li = chunk64bits[:32]
    Ri = chunk64bits[32:64]
    return Li, Ri

def DES_encrypt(P, subkeys):
    """Encrypts a 64-bit plaintext P using pre-generated subkeys."""
    if DEBUG_MODE:
        print_section_header("DES ENCRYPTION PROCESS")
    
    # Initial Permutation (IP)
    if DEBUG_MODE:
        print_step_header(0, "Initial Permutation (IP)")
    permuted_P = apply_IP(P)
    if DEBUG_MODE:
        print_binary_data("After IP", permuted_P)
    
    # Divide the permuted plaintext into two halves
    L, R = divide_text(permuted_P)
    
    if DEBUG_MODE:
        print_step_header(0, "Initial Split - Round 0")
        print_binary_data("L0", L)
        print_binary_data("R0", R)
    
    # Perform 16 rounds of the Feistel function
    for i in range(16):
        if DEBUG_MODE:
            print_step_header(i + 1, f"Round {i + 1}")
        # Save the current R to use as the new L
        previous_R = R
        
        # Apply the Feistel function F to R and the current subkey
        F_output = feistel_function(R, subkeys[i])
        
        if DEBUG_MODE:
            # Log xor R and F
            print(f"  F(R, K{i+1}): {F_output}")
            print(f"  L XOR F(R, K{i+1}): {[L[j] ^ F_output[j] for j in range(32)]}")
        
        # New R is L XOR F(R, Ki)
        R = [L[j] ^ F_output[j] for j in range(32)]
        if DEBUG_MODE:
            print(f"\n")
            print_binary_data("R: ", R)

        # New L is the previous R
        L = previous_R
        
        if DEBUG_MODE:
            print_step_header(i + 1, f"After Round {i + 1}")
            print_binary_data("L", L)
            print_binary_data("R", R)
    
    # IMPORTANT: In DES, after the 16th round, we combine R + L (not L + R)
    # This is because there's no swap after the final round
    combined = R + L
    
    # Apply the inverse initial permutation (IP-1) to get the ciphertext
    C = apply_IP_inverse(combined)
    
    return C

def DES_decrypt(C, subkeys):
    """Decrypts a 64-bit ciphertext C using pre-generated subkeys (in reverse order)."""

    # Initial Permutation (IP)
    permuted_C = apply_IP(C)

    # Divide the permuted ciphertext into two halves
    L, R = divide_text(permuted_C)

    # Perform 16 rounds of the Feistel function
    for i in range(16):
        # Save the current R to use as the new L
        previous_R = R

        # Apply the Feistel function F to R and the current subkey
        F_output = feistel_function(R, subkeys[i])

        # New R is L XOR F(R, Ki)
        R = [L[j] ^ F_output[j] for j in range(32)]

        # New L is the previous R
        L = previous_R

        if DEBUG_MODE:
            print_step_header(i + 1, f"After Round {i + 1}")
            print_binary_data("L", L)
            print_binary_data("R", R)

    # IMPORTANT: In DES, after the 16th round, we combine R + L (not L + R)
    # This is because there's no swap after the final round
    combined = R + L

    # Apply the inverse initial permutation (IP-1) to get the plaintext
    P = apply_IP_inverse(combined)

    return P


# Test the key generation
if __name__ == "__main__":
    # Check for command-line debug flag
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['--debug', '-d', 'debug']:
        DEBUG_MODE = True
    else:
        # Enable/Disable debug mode - set to True for detailed output, False for summary only
        DEBUG_MODE = False  # Change this to True for detailed output
    
    print_section_header("DES ALGORITHM TEST", '=')
    print(f"Debug Mode: {'ENABLED (detailed steps)' if DEBUG_MODE else 'DISABLED (summary only)'}")
    if not DEBUG_MODE:
        print("💡 Use 'python DES-algorithm.py --debug' for detailed step-by-step output")
    
    # Test data setup
    Plaintext = "0123456789ABCDEF"
    Key_hex = 0x133457799BBCDFF1

    # Convert hex string to integer
    Plaintext_int = int(Plaintext, 16)
    
    # Convert plaintext to binary list
    P = [(Plaintext_int >> i) & 1 for i in reversed(range(64))]

    # Convert hex to binary key
    K = [(Key_hex >> i) & 1 for i in reversed(range(64))]
    
    if DEBUG_MODE:
        print_section_header("INPUT DATA")
        print(f"Plaintext (HEX): {Plaintext}")
        print_binary_data("Plaintext", P)
        print(f"\nKey (HEX): {hex(Key_hex).upper().replace('0X', '0x')}")
        print_binary_data("Key", K)
    
    # Generate subkeys using the binary key K
    if not DEBUG_MODE:
        print_section_header("KEY GENERATION")
    start_time = time.time()
    subkeys = generateSubkeys(K)
    end_time = time.time()
    if not DEBUG_MODE:
        print(f"Generated {len(subkeys)} subkeys in {end_time - start_time:.6f} seconds")
    else:
        print(f"\n⏱ Key generation time: {end_time - start_time:.6f} seconds")

    # Encryption
    print_section_header("ENCRYPTION")
    if not DEBUG_MODE:
        print(f"Plaintext: {Plaintext}")
    
    ciphertext = DES_encrypt(P, subkeys)
    
    if DEBUG_MODE:
        print_section_header("ENCRYPTION RESULT")
        print_binary_data("Original Plaintext", P)
        print_binary_data("Final Ciphertext", ciphertext)
    else:
        cipher_hex = binary_to_hex(ciphertext)
        print(f"  → Encrypted: {cipher_hex}")

    # Decryption Test  
    print_section_header("DECRYPTION")
    # Create reversed subkeys for decryption
    subkeys_decrypt = subkeys[::-1]  # Reverse the subkeys for decryption
    
    if not DEBUG_MODE:
        cipher_hex = binary_to_hex(ciphertext)
        print(f"Ciphertext: {cipher_hex}")
    
    decrypted_plaintext = DES_decrypt(ciphertext, subkeys_decrypt)
    
    if DEBUG_MODE:
        print_section_header("DECRYPTION RESULT")
        print_binary_data("Decrypted Plaintext", decrypted_plaintext)
        print_binary_data("Original Plaintext", P)
    else:
        # Convert decrypted bits back to hex for display
        decrypted_bytes = bytearray()
        for i in range(0, len(decrypted_plaintext), 8):
            byte_bits = decrypted_plaintext[i:i + 8]
            byte_value = sum(bit << (7 - j) for j, bit in enumerate(byte_bits))
            decrypted_bytes.append(byte_value)
        decrypted_hex = ''.join(f'{byte:02X}' for byte in decrypted_bytes)
        print(f"  → Decrypted: {decrypted_hex}")

    # Verify that decryption worked
    print_section_header("VERIFICATION")
    if decrypted_plaintext == P:
        print("✅ SUCCESS: DES encryption and decryption completed successfully!")
        print("✅ Decrypted plaintext matches original plaintext!")
    else:
        print("❌ ERROR: DES encryption/decryption failed!")
        print("❌ Decrypted plaintext does NOT match original!")
