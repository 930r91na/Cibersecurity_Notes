# Key based enhancement of DES algorithm
# Differences between DES and and KE-DES
# Use of odd/even bit transformation of every key bit in the DES algorithm.
# Replacing the right-side expansion of the original DES by using Key-Distribution (K-D) function
#   The Key-Distribution (K-D) is 8-bits from Permutation Choice-1 (PC-1) key outcome. The next 32-bits outcomes from the right-side of data, there is also 8-bits outcome from Permutation Choice-2 (PC-2) in each round. The key and data created randomly, in this case, provide adequate security and the KEDES model is considered more efficient for text encryption.

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

# =============================== Key Generation ===============================
# KE-DES model needs 64-bits as the input
# Methodology:
# 1. KE-DES model needs 64-bits as the input key (same as DES)
# 2. In every Even bit position, 1 and 0 will be replaced by Odd bit position in the 56-bits block.
# 3. Divide the key into two halves (Ci and Di) of 28-bits each (same as DES)
# 4. Left shift both Ci and Di (same as DES)
# 5. Apply PC-2 to get the 48-bit subkey (same as DES)
# 6. Repeat steps 4 and 5 for 16 rounds to get 16 subkeys with the previous partial subkey as input (same as DES), 

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


PC1_table = [
        57, 49, 41, 33, 25, 17,  9,  1,
        58, 50, 42, 34, 26, 18, 10,  2,
        59, 51, 43, 35, 27, 19, 11,  3,
        60, 52, 44, 36, 63, 55, 47, 39,
        31, 23, 15,  7, 62, 54, 46, 38,
        30, 22, 14,  6, 61, 53, 45, 37,
        29, 21, 13,  5, 28, 20, 12,  4
]

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

def oddEvenBitTransformation(Kab):
    """
    KE-DES Enhancement: Apply odd-even bit transformation
    Every odd bit position will be moved to the first positions and every even bit position will be moved to the last positions.
    This according to the PC1 
    """
    for i in range(len(Kab)):
        odd = 1
        even = 29
        Kab_temp = Kab.copy()
        # EVEN
        if PC1_table[i] % 2 == 0 and i < len(Kab) - 1:
            Kab[even] = Kab_temp[i]
            even += 1
        # ODD
        else:
            Kab[odd] = Kab_temp[i]
            odd += 1


def generateSubkeys(Kab):
    # Apply PC-1 directly to 64-bit key (PC-1 automatically selects non-parity bits)
    if DEBUG_MODE:
        print_section_header("KEY GENERATION")
    KabOf56bits = applyPC1(Kab)
    if DEBUG_MODE:
        print_binary_data("Key after PC-1 (56 bits)", KabOf56bits)

    # Difference from DES: Apply odd-even bit transformation
    oddEvenBitTransformation(KabOf56bits)
    if DEBUG_MODE:
        print_binary_data("Key after Odd-Even Transformation (56 bits)", KabOf56bits)

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


# =============================== DES Algorithm Encryption and Decryption ===============================

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


# KE-DES Key-Distribution (K-D) function
# - 8 bits from PC-1 (constant for all rounds) - these are parity bit positions
# - 32 bits from the right side of data (R)
# - 8 bits from PC-2 (changes each round) - these come from the subkey
# Total: 48 bits output

# The 8 constant bits from PC-1 (parity bit positions from original 64-bit key)
PC1_constant_positions = [8, 16, 24, 32, 40, 48, 56, 64]

PC2_subkey_positions = [9, 18, 27, 36, 15, 22, 29, 4]  # First 8 bits of PC-2

def apply_KD(R, subkey_K, permutedChoice1):
    """
    Apply the K-D transformation to create 48-bit input for Feistel function.
    
    Args:
        R: 32-bit right half of data
        subkey_K: 48-bit subkey for current round  
        permutedChoice1: 56-bit key after PC-1 permutation
    
    Returns:
        48-bit result combining PC-1 constant bits, R data, and PC-2 subkey bits
    """

    # Get 8 constant bits from original key (parity bit positions)
    pc1_bits = [permutedChoice1[pos - 1] for pos in PC1_constant_positions]
    
    # Get 8 bits from PC-2 subkey for the positions defined in PC2_subkey_positions
    pc2_bits = [subkey_K[pos - 1] for pos in PC2_subkey_positions]

    # Combine: 8 PC-1 bits + 32 R bits + 8 PC-2 bits = 48 bits
    kd_result = pc1_bits + R + pc2_bits
    
    return kd_result

# KE-DES Feistel function that uses K-D instead of expansion
def feistel_function_KD(R, K, pc1):
    """KE-DES Feistel function that uses K-D transformation instead of expansion."""
    
    if DEBUG_MODE:
        print(" KE-DES FEISTEL FUNCTION DETAILS")
        print_binary_data("      Input R", R, show_hex=False)
        print_binary_data("      Input K", K, show_hex=False)
    
    # Step 1: Apply K-D transformation instead of expansion
    kd_result = apply_KD(R, K, pc1)
    if DEBUG_MODE:
        print("\n K-D Transformation:")
        print_binary_data("      K-D result", kd_result, show_hex=False)

    # Step 2: XOR with the subkey K
    xor_result = [kd_result[i] ^ K[i] for i in range(48)]
    if DEBUG_MODE:
        print("\n      ⊕ XOR with subkey:")
        print_binary_data("      XOR result", xor_result, show_hex=False)
    
    # Step 3: Apply the S-boxes
    if DEBUG_MODE:
        print("\n S-BOX SUBSTITUTIONS:")
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
        print("\n  P-PERMUTATION:")
        print_binary_data("      Before P", sbox_output, show_hex=False)
    
    # Apply P-permutation to the 32-bit S-box output
    p_output = apply_P_permutation(sbox_output)
    if DEBUG_MODE:
        print_binary_data(" After P", p_output, show_hex=False)
    
    return p_output

def divide_text(chunk64bits):
    """Returns Li and Ri"""
    Li = chunk64bits[:32]
    Ri = chunk64bits[32:64]
    return Li, Ri

# =============================== DES Encryption  ===============================
# Ke-DES encryption process
# Methodology:
# 1. Initial Permutation (IP) (same as DES)
# 2. Divide the permuted text into two halves (L0 and R0) (same as DES)
# 3. Apply K-D operion to R
# 4. Apply XOR between Ki and K-D(R)
# 5. Apply the s-boxes substitution (same as DES)
# 6. Apply the P-permutation (same as DES)
# 7. New Ri = L(i-1) XOR P-output (same as DES)
# 8. New Li = R(i-1) (same as DES)
# 9. Repeat steps 3 to 8 for 16 rounds (same as DES)
# 10. Finally, apply the inverse initial permutation (IP-1) to get the ciphertext (same as DES)

def KE_DES_encrypt(P, subkeys, Kab):
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
        # In KE-DES, the K-D function is used inside the Feistel function instead of expansion
        F_output = feistel_function_KD(R, subkeys[i], Kab)
        
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


# =============================== DES Decryption  ===============================
# Ke-DES decryption process
# Methodology:
# 1. Initial Permutation (IP) (same as DES)
# 2. Divide the permuted text into two halves (L0 and R0) (same as DES)
# 3. Apply K-D operion to R
# 4. Apply XOR between Ki and K-D(R)
# 5. Apply the s-boxes substitution (same as DES)
# 6. Apply the P-permutation (same as DES)
# 7. New Ri = L(i-1) XOR P-output (same as DES)
# 8. New Li = R(i-1) (same as DES)
# 9. Repeat steps 3 to 8 for 16 rounds with subkeys in reverse order (same as DES)
# 10. Finally, apply the inverse initial permutation (IP-1) to get the plaintext (same as DES)
def KE_DES_decrypt(C, subkeys, Kab):
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
        F_output = feistel_function_KD(R, subkeys[i], Kab)

        # New R is L XOR F(R, Ki)
        R = [L[j] ^ F_output[j] for j in range(32)]

        # New L is the previous R
        L = previous_R

        if DEBUG_MODE:
            print_step_header(i + 1, f"After Round {i + 1}")
            print_binary_data("L", L)
            print_binary_data("R", R)

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
    
    print_section_header("KE-DES ALGORITHM TEST", '=')
    print(f"Debug Mode: {'ENABLED (detailed steps)' if DEBUG_MODE else 'DISABLED (summary only)'}")
    if not DEBUG_MODE:
        print("💡 Use 'python KE-DES-algorithm.py --debug' for detailed step-by-step output")
    
    plaintext = "The Cipher Block Chaining (CBC) mode encrypts a preprocessed block of a message instead of an original message block, where the preprocessed block is formed through exclusive-ORing the original message block with a cipher data block produced from encrypting the previous message block. In the case of the first preprocessed block, a data block called initialization vector is used for exclusive Ring operation with the first message block. In other words, CBC encryption is a process of chaining successive cipher and message blocks together until the last message block is encrypted."
    plaintext = plaintext[:16]  # Use first 16 characters for testing (2 blocks) 
    expected_ciphertext_hex = 0xCB56922039AE9D6B40B0F68B26228259EE3366A2EC8C19E116DA8A4A34BA26FDE7CE6C3194F128E9C1FF5769282676EDAA4F814A9C7768C54D94B689D2491A81409A17F3F431C6FE6366C9AB3AD12AF6620A4542AD0B85C9F36697C8A0434DD8FD7A251B9127FC4E276083692B0C8B9A0BA60B240795AD8CEF00D08F5B07D5CC3BB03A1444B5DD
    expected_ciphertext_hex += 0x033323B0B250E1691F464C99734F45A8FE2226339E4E431828EA7C21FE07F6DE4C8C76E395E4556AC02A9CB2B8F3AD3183780B3AE5E64B0A0A06587A22BBDEE7ED7D21FDB6455479367EB0AC33B9B03991A9B969808E9F11779226AC25D776935EA6403FB30F8CF79D11A02BAC7EDD9EDD07E83E382B567D5E6A332FDB995EF98176EE52AB96660B5511AF9B9931A9610D69951520ACEB89A9D448A264235DAB83C43ABAF03FE5C0CDF4C25F309839B8B6F6F331D9630D2AD3E2AD146B106874F51D0D22B010D0F6A1C90A1E08E78B65F9D4E2C329975807CAB5832D12203C3641A4962DE8C05E6EB1ED429AD115E723063B2DC27E6B8C26DE51876FBC0C6CB07FD2E2C0AF71BE69A32092C6B1C0124
    expected_ciphertext_hex += 0xEA88ECBED998D496FD9DC5A0D0659AB575A85593B220FB32B94A366D2A458C17487AE3EA801D0743D57FDDA
    expected_ciphertext_hex += 0x9B8677A27F76FFD376282D910E532C1A83858C598A571553B80B205295CB544A59499E02B7C525EA8CBAE01FEDF5C
    expected_ciphertext_hex += 0xDE9139A6A43A502F6FF93D980C566452879D5EB6EED21F51CB65A30976B052DF84908FA55A4C591B2EE77BBB42
    expected_ciphertext_hex += 0xB985B46C303DA24BB11346F6594D9F2FB71A1D4BA369A7A7A30E676F5D8183190A97B7F7531B2835E09535B36386
    expected_ciphertext_hex += 0x03823DA509

    key_hex = 0x133457799BBCDFF1

    # Convert key to binary (64 bits)
    K = [(key_hex >> i) & 1 for i in reversed(range(64))]

    # Generate subkeys once for all blocks
    if not DEBUG_MODE:
        print_section_header("KEY GENERATION")
    start_time = time.time()
    subkeys = generateSubkeys(K)
    end_time = time.time()
    if not DEBUG_MODE:
        print(f"Generated {len(subkeys)} subkeys in {end_time - start_time:.6f} seconds")
    else:
        print(f"Total subkey generation time: {end_time - start_time:.6f} seconds")
        print(f"Generated {len(subkeys)} subkeys for reuse across all blocks")

    # Convert plaintext to bytes and then process in 64-bit (8-byte) blocks
    print_section_header("ENCRYPTION")
    plaintext_bytes = plaintext.encode('utf-8')
    
    cipher_calculated = []
    block_count = 0
    
    # Process in 8-byte (64-bit) blocks
    for i in range(0, len(plaintext_bytes), 8):
        block_count += 1
        # Get 8 bytes (pad with zeros if necessary)
        byte_block = plaintext_bytes[i:i + 8]
        
        # Pad with zeros if the block is less than 8 bytes
        while len(byte_block) < 8:
            byte_block += b'\x00'
        
        # Convert bytes to 64-bit binary representation
        block_bits = []
        for byte in byte_block:
            # Convert each byte to 8 bits
            byte_bits = [(byte >> j) & 1 for j in reversed(range(8))]
            block_bits.extend(byte_bits)
        
        if not DEBUG_MODE:
            print(f"Block {block_count}: '{plaintext[i:i+8] if i < len(plaintext) else 'padding'}'")
        else:
            print_step_header(block_count, f"Block {block_count} Encryption")
            print(f"  Text: '{plaintext[i:i+8] if i < len(plaintext) else 'padding'}'")
            print_binary_data("Plaintext Block", block_bits)
        
        cipher_block = KE_DES_encrypt(block_bits, subkeys, K)
        cipher_calculated.extend(cipher_block)
        
        if DEBUG_MODE:
            print_binary_data(f"Cipher Block {block_count}", cipher_block)
        else:
            # Show concise summary
            cipher_hex = binary_to_hex(cipher_block)
            print(f"  → Encrypted: {cipher_hex}")

    if not DEBUG_MODE:
        # Show final cipher summary
        total_cipher_hex = binary_to_hex(cipher_calculated)
        print(f"Total Ciphertext: {total_cipher_hex}")
    else:
        print_section_header("FINAL CIPHERTEXT")
    

    # Decryption Test
    print_section_header("DECRYPTION")
    # Create reversed subkeys for decryption
    subkeys_decrypt = subkeys[::-1]  # Reverse the subkeys for decryption
    
    decrypted_calculated = []
    block_count = 0
    for i in range(0, len(cipher_calculated), 64):
        block_count += 1
        cipher_block = cipher_calculated[i:i + 64]
        
        if not DEBUG_MODE:
            cipher_hex = binary_to_hex(cipher_block)
            print(f"Block {block_count}: {cipher_hex}")
        else:
            print_step_header(block_count, f"Block {block_count} Decryption")
            print_binary_data("Cipher Block", cipher_block)
        
        decrypted_block = KE_DES_decrypt(cipher_block, subkeys_decrypt, K)
        decrypted_calculated.extend(decrypted_block)
        
        if DEBUG_MODE:
            print_binary_data(f"Decrypted Block {block_count}", decrypted_block)
        else:
            # Convert decrypted block back to text for summary
            decrypted_bytes = bytearray()
            for j in range(0, len(decrypted_block), 8):
                byte_bits = decrypted_block[j:j + 8]
                byte_value = sum(bit << (7 - k) for k, bit in enumerate(byte_bits))
                decrypted_bytes.append(byte_value)
            block_text = decrypted_bytes.decode('utf-8', errors='ignore')
            print(f"  → Decrypted: '{block_text}'")

    print_section_header("FINAL DECRYPTED PLAINTEXT")
    # Convert decrypted bits back to bytes
    decrypted_bytes = bytearray()
    for i in range(0, len(decrypted_calculated), 8):
        byte_bits = decrypted_calculated[i:i + 8]
        byte_value = sum(bit << (7 - j) for j, bit in enumerate(byte_bits))
        decrypted_bytes.append(byte_value)

    print(f"Decrypted text: '{decrypted_bytes.decode('utf-8', errors='ignore')}'")