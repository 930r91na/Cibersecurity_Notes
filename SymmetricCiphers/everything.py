import os
import sys

# ==============================================================================
# SECTION 1: UTILITY FUNCTIONS (from formatting_utils.py)
# ==============================================================================


def format_binary_grouped(binary_list, group_size=4):
    """
    Format binary list in groups of bits with spaces between groups.
    """
    if not binary_list:
        return ""
    binary_str = "".join(str(bit) for bit in binary_list)
    grouped = [
        binary_str[i : i + group_size] for i in range(0, len(binary_str), group_size)
    ]
    return " ".join(grouped)


def binary_to_hex(binary_list):
    """
    Convert binary list to hexadecimal string.
    """
    if not binary_list:
        return ""
    padded = binary_list[:]
    while len(padded) % 4 != 0:
        padded.insert(0, 0)
    binary_str = "".join(str(bit) for bit in padded)
    hex_value = hex(int(binary_str, 2))[2:].upper().zfill(len(padded) // 4)
    return hex_value


def hex_string_to_binary_list(hex_str, bit_length=64):
    """
    Convert hexadecimal string to binary list of a specific length.
    """
    if hex_str.startswith(("0x", "0X")):
        hex_str = hex_str[2:]

    try:
        int_value = int(hex_str, 16)
        binary_str = bin(int_value)[2:].zfill(bit_length)
        return [int(bit) for bit in binary_str]
    except (ValueError, TypeError):
        return None


def print_section_header(title, char="="):
    """
    Print a formatted section header with decorative characters.
    """
    width = 70
    padding = (width - len(title) - 2) // 2
    if padding < 0:
        padding = 0
    print(f"\n{char * padding} {title} {char * padding}")


def print_binary_data(label, binary_list, show_hex=True):
    """
    Print binary data in formatted groups with optional hex representation.
    """
    formatted_binary = format_binary_grouped(binary_list)
    if show_hex and binary_list:
        hex_value = binary_to_hex(binary_list)
        print(f"{label:20} ({len(binary_list):2d} bits): {formatted_binary}")
        print(f"{' ' * 20}              HEX: {hex_value}")
    else:
        print(f"{label:20} ({len(binary_list):2d} bits): {formatted_binary}")


def print_step_header(step_num, title, sub_title=""):
    """
    Print a formatted step header for algorithm phases.
    """
    if sub_title:
        print(f"\n--- Step {step_num}: {title} ({sub_title}) ---")
    else:
        print(f"\n--- Step {step_num}: {title} ---")


def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


# ==============================================================================
# SECTION 2: MATHEMATICAL FOUNDATIONS (from Euclidean_GF_algorithm.py)
# ==============================================================================


def gcd(a, b):
    """Euclidean GCD algorithm."""
    print("--- Euclidean GCD Algorithm Steps ---")
    while b:
        print(f"GCD({a}, {b}) = GCD({b}, {a} mod {b}) = GCD({b}, {a % b})")
        a, b = b, a % b
    print("-----------------------------------")
    return a


def polynomial_mod(fx, gx):
    """Polynomial division (modulo) over GF(2)."""
    deg_fx = fx.bit_length() - 1
    deg_gx = gx.bit_length() - 1

    while deg_fx >= deg_gx:
        shift = deg_fx - deg_gx
        shifted_gx = gx << shift
        fx ^= shifted_gx
        deg_fx = fx.bit_length() - 1
    return fx


def poly_gcd(fx, gx):
    """GCD for polynomials over GF(2)."""
    print("--- Polynomial GCD Steps (binary representation) ---")
    while gx:
        remainder = polynomial_mod(fx, gx)
        print(f"GCD({bin(fx)}, {bin(gx)}) = GCD({bin(gx)}, {bin(remainder)})")
        fx, gx = gx, remainder
    print("-------------------------------------------------")
    return fx


def extended_euclidean(m, b):
    """Extended Euclidean Algorithm to find the multiplicative inverse of b mod m."""
    a1, a2, a3 = 1, 0, m
    b1, b2, b3 = 0, 1, b

    print("--- Extended Euclidean Algorithm Steps ---")
    print(f" Q  |  A1  |  A2  |  A3  |  B1  |  B2  |  B3 ")
    print("----|------|------|------|------|------|------")

    while b3 != 0:
        q = a3 // b3 if b3 != 0 else 0
        print(f"{q:<3} | {a1:<4} | {a2:<4} | {a3:<4} | {b1:<4} | {b2:<4} | {b3:<4}")
        if b3 == 1:
            print("----------------------------------------")
            return b2 % m

        t1, t2, t3 = a1 - q * b1, a2 - q * b2, a3 - q * b3
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3

    print(f"{' ':>3} | {a1:>4} | {a2:>4} | {a3:>4} | {b1:>4} | {b2:>4} | {b3:>4}")
    print("----------------------------------------")
    raise ValueError(f"No multiplicative inverse for {b} mod {m} exists.")


# ==============================================================================
# SECTION 3: CLASSICAL CIPHERS
# ==============================================================================

# --- Subsection 3.1: Substitution Ciphers ---


def caesar_cipher(mode):
    """Handler for Caesar cipher encryption and decryption."""
    try:
        text = input(f"Enter the {'plaintext' if mode == 'e' else 'ciphertext'}: ")
        shift = int(input("Enter the shift value (e.g., 3): "))
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if mode == "d":
            print("\n[INFO] Decrypting: Applying negative shift.")
            shift = -shift

        result = ""
        print_step_header(1, "Processing each character")
        for char in text:
            if char.upper() in alphabet:
                original_index = alphabet.index(char.upper())
                shifted_index = (original_index + shift) % 26
                new_char = alphabet[shifted_index]
                if not char.isupper():
                    new_char = new_char.lower()
                print(
                    f"  '{char}' (index {original_index}) + shift {shift} -> '{new_char}' (index {shifted_index})"
                )
                result += new_char
            else:
                print(f"  '{char}' is not in the alphabet, skipping.")
                result += char

        print_section_header("Result")
        print(f"{'Ciphertext' if mode != 'd' else 'Plaintext'}: {result}")
    except ValueError:
        print("\n[Error] Invalid shift value. Please enter an integer.")


def monoalphabetic_substitution(mode):
    """Handler for monoalphabetic substitution cipher."""
    try:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = input(f"Enter the 26-letter key (no repeated characters):\n> ").upper()
        if len(key) != 26 or len(set(key)) != 26:
            print("\n[Error] Invalid key. Key must be 26 unique alphabetic characters.")
            return

        text = input(f"Enter the {'plaintext' if mode == 'e' else 'ciphertext'}: ")
        result = ""

        if mode == "d":
            print_step_header(1, "Creating decryption map")
            decryption_key_map = {key[i]: alphabet[i] for i in range(26)}
            for k, v in decryption_key_map.items():
                print(f"  Cipher '{k}' -> Plain '{v}'")
            print_step_header(2, "Processing each character")
            for char in text:
                if char.upper() in decryption_key_map:
                    dec_char = decryption_key_map[char.upper()]
                    print(f"  '{char}' -> Mapped to '{dec_char}'")
                    result += dec_char if char.isupper() else dec_char.lower()
                else:
                    print(f"  '{char}' is not in the map, skipping.")
                    result += char
        else:  # Encrypt
            print_step_header(1, "Processing each character")
            for char in text:
                if char.upper() in alphabet:
                    index = alphabet.index(char.upper())
                    enc_char = key[index]
                    print(f"  '{char}' (index {index}) -> Mapped to '{enc_char}'")
                    result += enc_char if char.isupper() else enc_char.lower()
                else:
                    print(f"  '{char}' is not in the alphabet, skipping.")
                    result += char

        print_section_header("Result")
        print(f"{'Ciphertext' if mode == 'e' else 'Plaintext'}: {result}")

    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")


def _create_playfair_matrix(key):
    """Creates a 5x5 Playfair matrix from the given key."""
    key = key.upper().replace("J", "I")
    matrix_chars = []
    used_chars = set()

    for char in key:
        if char not in used_chars and "A" <= char <= "Z":
            used_chars.add(char)
            matrix_chars.append(char)

    for char_code in range(ord("A"), ord("Z") + 1):
        char = chr(char_code)
        if char == "J":
            continue
        if char not in used_chars:
            matrix_chars.append(char)

    matrix = [matrix_chars[i : i + 5] for i in range(0, 25, 5)]
    return matrix


def _playfair_process(text, key, mode):
    """Core process for Playfair encryption and decryption."""
    matrix = _create_playfair_matrix(key)
    char_to_pos = {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}

    print_step_header(1, "Playfair Matrix Generation")
    for row in matrix:
        print("  " + " ".join(row))

    # Prepare text
    original_text = text
    text = text.upper().replace("J", "I")
    text = "".join(filter(str.isalpha, text))
    print_step_header(2, "Text Preparation")
    print(f"Original: '{original_text}' -> Processed: '{text}'")

    # Create digraphs
    print_step_header(3, "Digraph Creation")
    digraphs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "X"
        if a == b:
            print(f"  Found double letter '{a}{b}', inserting 'X'. New digraph: '{a}X'")
            digraphs.append((a, "X"))
            i += 1
        else:
            if i + 1 >= len(text):
                print(f"  Odd letter at end. Appending 'X'. New digraph: '{a}X'")
            digraphs.append((a, b))
            i += 2
    print("  Digraphs:", " ".join([d[0] + d[1] for d in digraphs]))

    # Process digraphs
    print_step_header(4, f"{'En' if mode == 'e' else 'De'}cryption Process")
    result = ""
    shift = 1 if mode == "e" else -1
    for a, b in digraphs:
        r1, c1 = char_to_pos[a]
        r2, c2 = char_to_pos[b]

        new_a, new_b = "", ""
        rule = ""
        if r1 == r2:  # Same row
            new_a = matrix[r1][(c1 + shift) % 5]
            new_b = matrix[r2][(c2 + shift) % 5]
            rule = "Same Row"
        elif c1 == c2:  # Same column
            new_a = matrix[(r1 + shift) % 5][c1]
            new_b = matrix[(r2 + shift) % 5][c2]
            rule = "Same Column"
        else:  # Rectangle
            new_a = matrix[r1][c2]
            new_b = matrix[r2][c1]
            rule = "Rectangle"

        print(
            f"  Digraph: {a}{b} -> Pos: ({r1},{c1}) ({r2},{c2}) -> Rule: {rule} -> New Digraph: {new_a}{new_b}"
        )
        result += new_a
        result += new_b
    return result


def handle_playfair_cipher(mode):
    """Handler for Playfair cipher."""
    prompt = "plaintext" if mode == "e" else "ciphertext"
    text = input(f"Enter the {prompt}: ")
    key = input("Enter the keyword: ")
    result = _playfair_process(text, key, mode)

    print_section_header("Result")
    out_label = "Ciphertext" if mode == "e" else "Plaintext"
    print(f"{out_label}: {result}")


def vigenere_cipher(mode):
    """Handler for Vigenère cipher."""
    try:
        text = input(f"Enter the {'plaintext' if mode == 'e' else 'ciphertext'}: ")
        key = input("Enter the keyword: ").upper()
        if not key.isalpha():
            print("\n[Error] Keyword must only contain letters.")
            return

        result = ""
        key_index = 0
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        print_step_header(1, "Processing each character")
        for char in text:
            if char.isalpha():
                key_char = key[key_index % len(key)]
                shift = alphabet.index(key_char)
                if mode == "d":
                    shift = -shift

                original_index = alphabet.index(char.upper())
                shifted_index = (original_index + shift) % 26
                new_char = alphabet[shifted_index]
                if not char.isupper():
                    new_char = new_char.lower()

                print(
                    f"  '{char}' (index {original_index}) + Key '{key_char}' (shift {shift if mode != 'd' else -shift}) -> '{new_char}' (index {shifted_index})"
                )
                result += new_char
                key_index += 1
            else:
                print(f"  '{char}' is not alphabetic, skipping.")
                result += char

        print_section_header("Result")
        print(f"{'Ciphertext' if mode == 'e' else 'Plaintext'}: {result}")

    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")


# --- Subsection 3.2: Transposition Ciphers ---


def rail_fence_cipher(mode):
    """Handler for Rail Fence cipher."""
    try:
        text = input(f"Enter the {'plaintext' if mode == 'e' else 'ciphertext'}: ")
        num_rails = int(input("Enter the number of rails: "))
        if num_rails <= 1:
            print("\n[Error] Number of rails must be greater than 1.")
            return

        if mode == "e":
            print_step_header(
                1, "Distributing plaintext characters onto rails in a zigzag pattern"
            )
            rails_content = [""] * num_rails
            rail_index, direction = 0, 1
            for char in text:
                rails_content[rail_index] += char
                rail_index += direction
                if rail_index == 0 or rail_index == num_rails - 1:
                    direction *= -1

            print_step_header(2, "Reading off rails row by row to form ciphertext")
            for i, content in enumerate(rails_content):
                print(f"  Rail {i+1}: {content}")
            result = "".join(rails_content)
        else:  # Decrypt
            text_len = len(text)

            print_step_header(1, "Calculate how many characters belong to each rail")
            rail_lengths = [0] * num_rails
            rail_index, direction = 0, 1
            for _ in range(text_len):
                rail_lengths[rail_index] += 1
                rail_index += direction
                if rail_index == 0 or rail_index == num_rails - 1:
                    direction *= -1
            print(f"  Characters per rail: {rail_lengths}")

            print_step_header(2, "Slice ciphertext and assign to each rail")
            rails = []
            current_pos = 0
            for i, length in enumerate(rail_lengths):
                rail_content = text[current_pos : current_pos + length]
                rails.append(list(rail_content))
                print(f"  Rail {i+1} content: '{rail_content}'")
                current_pos += length

            print_step_header(
                3, "Reconstruct plaintext by reading from rails in a zigzag pattern"
            )
            result = ""
            rail_index, direction = 0, 1
            for _ in range(text_len):
                char = rails[rail_index].pop(0)
                result += char
                rail_index += direction
                if rail_index == 0 or rail_index == num_rails - 1:
                    direction *= -1
            print(
                f"  The reconstructed plaintext is read by picking the first available character from each rail in sequence."
            )

        print_section_header("Result")
        print(f"{'Ciphertext' if mode == 'e' else 'Plaintext'}: {result}")

    except ValueError:
        print("\n[Error] Invalid number of rails. Please enter an integer.")


def row_transposition_cipher(mode):
    """Handler for Row Transposition cipher."""
    try:
        text = input(f"Enter the {'plaintext' if mode == 'e' else 'ciphertext'}: ")
        keyword = input("Enter the keyword: ").upper()
        if not keyword.isalpha():
            print("\n[Error] Keyword must be alphabetic.")
            return

        key_order = sorted(range(len(keyword)), key=lambda k: keyword[k])

        if mode == "e":
            text = text.replace(" ", "").upper()
            num_cols = len(keyword)
            num_rows = (len(text) + num_cols - 1) // num_cols
            padded_text = text.ljust(num_rows * num_cols, "X")

            grid = [
                list(padded_text[i : i + num_cols])
                for i in range(0, len(padded_text), num_cols)
            ]
            print_step_header(1, "Writing plaintext into a grid")
            for row in grid:
                print("  " + " ".join(row))

            print_step_header(
                2,
                f"Reading columns in order: {'-'.join(map(str, [k+1 for k in key_order]))}",
            )
            ciphertext = ""
            for col_index in key_order:
                column_data = "".join([grid[row][col_index] for row in range(num_rows)])
                print(
                    f"  Reading column {col_index+1} ('{keyword[col_index]}'): {column_data}"
                )
                ciphertext += column_data
            result = ciphertext

        else:  # Decrypt
            num_cols = len(keyword)
            num_rows = len(text) // num_cols
            if len(text) % num_cols != 0:
                print("\n[Error] Invalid ciphertext length for the given key.")
                return

            grid = [[""] * num_cols for _ in range(num_rows)]
            print_step_header(
                1,
                f"Writing ciphertext into grid by columns in order: {'-'.join(map(str, [k+1 for k in key_order]))}",
            )
            text_index = 0
            for col_index in key_order:
                print(f"  Writing to column {col_index+1} ('{keyword[col_index]}')")
                for row_index in range(num_rows):
                    grid[row_index][col_index] = text[text_index]
                    text_index += 1

            print_step_header(2, "Viewing the reconstructed grid")
            for row in grid:
                print("  " + " ".join(row))

            plaintext = "".join("".join(row) for row in grid)
            result = plaintext.rstrip("X")

        print_section_header("Result")
        print(f"{'Ciphertext' if mode == 'e' else 'Plaintext'}: {result}")

    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")


# ==============================================================================
# SECTION 4: CRYPTANALYSIS TOOLS
# ==============================================================================

ENGLISH_LETTER_FREQUENCY = {
    "E": 12.70,
    "T": 9.06,
    "A": 8.17,
    "O": 7.51,
    "I": 6.97,
    "N": 6.75,
    "S": 6.33,
    "H": 6.09,
    "R": 5.99,
    "D": 4.25,
    "L": 4.03,
    "C": 2.78,
    "U": 2.76,
    "M": 2.41,
    "W": 2.36,
    "F": 2.23,
    "G": 2.02,
    "Y": 1.97,
    "P": 1.93,
    "B": 1.29,
    "V": 0.98,
    "K": 0.77,
    "J": 0.15,
    "X": 0.15,
    "Q": 0.10,
    "Z": 0.07,
}


def handle_frequency_analysis():
    """Performs a frequency analysis on a given ciphertext."""
    text = input("Enter the ciphertext to analyze:\n> ")
    frequency = {}
    total_letters = 0
    for char in text.upper():
        if "A" <= char <= "Z":
            frequency[char] = frequency.get(char, 0) + 1
            total_letters += 1
    if total_letters == 0:
        print("\n[Info] No alphabetic characters found to analyze.")
        return

    for char in frequency:
        frequency[char] = (frequency[char] / total_letters) * 100

    sorted_freq = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    sorted_english = sorted(
        ENGLISH_LETTER_FREQUENCY.items(), key=lambda item: item[1], reverse=True
    )
    suggested_mapping = {
        cipher_char: english_char
        for (cipher_char, _), (english_char, _) in zip(sorted_freq, sorted_english)
    }

    print_section_header("Frequency Analysis Results")
    print(
        f"{'Cipher Letter':<15}{'Frequency (%)':<15}{'Suggested Plaintext Letter':<25}"
    )
    print("-" * 55)
    for char, freq in sorted_freq:
        mapped_char = suggested_mapping.get(char, "?")
        print(f"{char:<15}{freq:<15.2f}{mapped_char:<25}")

    print("\n--- Sample Decryption ---")
    sample_decryption = ""
    for char in text:
        upper_char = char.upper()
        if upper_char in suggested_mapping:
            dec_char = suggested_mapping[upper_char]
            sample_decryption += dec_char if char.isupper() else dec_char.lower()
        else:
            sample_decryption += char
    print(sample_decryption)


# ==============================================================================
# SECTION 5: BLOCK CIPHERS (from DES-algorithm.py and 3DES-algorithm.py)
# ==============================================================================

# --- DES Constants (Corrected according to FIPS-46-3) ---

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
S_BOXES = [S1, S2, S3, S4, S5, S6, S7, S8]
IP_table = [
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    60,
    52,
    44,
    36,
    28,
    20,
    12,
    4,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    64,
    56,
    48,
    40,
    32,
    24,
    16,
    8,
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
]
IP_inverse_table = [
    40,
    8,
    48,
    16,
    56,
    24,
    64,
    32,
    39,
    7,
    47,
    15,
    55,
    23,
    63,
    31,
    38,
    6,
    46,
    14,
    54,
    22,
    62,
    30,
    37,
    5,
    45,
    13,
    53,
    21,
    61,
    29,
    36,
    4,
    44,
    12,
    52,
    20,
    60,
    28,
    35,
    3,
    43,
    11,
    51,
    19,
    59,
    27,
    34,
    2,
    42,
    10,
    50,
    18,
    58,
    26,
    33,
    1,
    41,
    9,
    49,
    17,
    57,
    25,
]
E_table = [
    32,
    1,
    2,
    3,
    4,
    5,
    4,
    5,
    6,
    7,
    8,
    9,
    8,
    9,
    10,
    11,
    12,
    13,
    12,
    13,
    14,
    15,
    16,
    17,
    16,
    17,
    18,
    19,
    20,
    21,
    20,
    21,
    22,
    23,
    24,
    25,
    24,
    25,
    26,
    27,
    28,
    29,
    28,
    29,
    30,
    31,
    32,
    1,
]
P_table = [
    16,
    7,
    20,
    21,
    29,
    12,
    28,
    17,
    1,
    15,
    23,
    26,
    5,
    18,
    31,
    10,
    2,
    8,
    24,
    14,
    32,
    27,
    3,
    9,
    19,
    13,
    30,
    6,
    22,
    11,
    4,
    25,
]
PC1_table = [
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    60,
    52,
    44,
    36,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    28,
    20,
    12,
    4,
]
PC2_table = [
    14,
    17,
    11,
    24,
    1,
    5,
    3,
    28,
    15,
    6,
    21,
    10,
    23,
    19,
    12,
    4,
    26,
    8,
    16,
    7,
    27,
    20,
    13,
    2,
    41,
    52,
    31,
    37,
    47,
    55,
    30,
    40,
    51,
    45,
    33,
    48,
    44,
    49,
    39,
    56,
    34,
    53,
    46,
    42,
    50,
    36,
    29,
    32,
]
SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


# --- DES Core Functions ---
def _permute(block, table):
    return [block[i - 1] for i in table]


def _feistel_function(R, K, verbose=False):
    """Internal Feistel function used by DES."""
    expanded_R = _permute(R, E_table)
    if verbose:
        print_binary_data("      Expanded R", expanded_R, show_hex=False)

    xor_result = [expanded_R[i] ^ K[i] for i in range(48)]
    if verbose:
        print_binary_data("      XOR result", xor_result, show_hex=False)

    sbox_output = []
    if verbose:
        print("\n      📦 S-BOX SUBSTITUTIONS:")
    for i in range(8):
        block = xor_result[i * 6 : (i + 1) * 6]
        row = (block[0] << 1) | block[5]
        col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
        sbox_value = S_BOXES[i][row][col]
        sbox_output.extend([(sbox_value >> j) & 1 for j in reversed(range(4))])
        if verbose:
            print(
                f"      S{i+1}: {format_binary_grouped(block, 6)} -> {sbox_value:2d} -> {format_binary_grouped([(sbox_value >> j) & 1 for j in reversed(range(4))], 4)}"
            )

    p_output = _permute(sbox_output, P_table)
    if verbose:
        print_binary_data("      After P", p_output, show_hex=False)
    return p_output


def _generate_des_subkeys(key_64bit):
    """Internal function to generate the 16 DES subkeys."""
    key_56bit = _permute(key_64bit, PC1_table)
    C, D = key_56bit[:28], key_56bit[28:]
    subkeys = []
    for shift in SHIFTS:
        C = C[shift:] + C[:shift]
        D = D[shift:] + D[:shift]
        subkeys.append(_permute(C + D, PC2_table))
    return subkeys


def des_process(block_64bit, key_64bit, mode="e", verbose=False):
    """Core DES process for encryption or decryption of a single 64-bit block."""
    subkeys = _generate_des_subkeys(key_64bit)
    if mode == "d":
        subkeys = subkeys[::-1]

    if verbose:
        print_section_header("KEY GENERATION")
        for i, sk in enumerate(subkeys):
            print_binary_data(f"Subkey K{i+1}", sk)

    permuted_block = _permute(block_64bit, IP_table)
    L, R = permuted_block[:32], permuted_block[32:]

    if verbose:
        print_section_header("ENCRYPTION/DECRYPTION PROCESS")
        print_step_header(0, "Initial State")
        print_binary_data("L0", L)
        print_binary_data("R0", R)

    for i in range(16):
        prev_L = L
        L = R
        if verbose:
            print_step_header(i + 1, f"Round {i+1}")
            print("      🔄 FEISTEL FUNCTION DETAILS")
            print_binary_data("      Input R", R, show_hex=False)
            print_binary_data("      Subkey K", subkeys[i], show_hex=False)
        f_output = _feistel_function(R, subkeys[i], verbose)
        R = [prev_L[j] ^ f_output[j] for j in range(32)]
        if verbose:
            print_binary_data(f"L{i+1}", L)
            print_binary_data(f"R{i+1}", R)

    final_block = _permute(R + L, IP_inverse_table)
    return final_block


# --- 3DES Functions ---
def tdes_process(block_64bit, key1, key2, key3=None, mode="e", verbose=False):
    """Core 3DES process for a single block."""
    if key3 is None:
        key3 = key1

    if mode == "e":
        print_step_header("3DES Stage 1", "Encrypting with Key 1")
        res1 = des_process(block_64bit, key1, "e", verbose)
        print_binary_data("Intermediate Result 1", res1)

        print_step_header("3DES Stage 2", "Decrypting with Key 2")
        res2 = des_process(res1, key2, "d", verbose)
        print_binary_data("Intermediate Result 2", res2)

        print_step_header("3DES Stage 3", "Encrypting with Key 3")
        final_res = des_process(res2, key3, "e", verbose)
    else:  # Decrypt
        print_step_header("3DES Stage 1", "Decrypting with Key 3")
        res1 = des_process(block_64bit, key3, "d", verbose)
        print_binary_data("Intermediate Result 1", res1)

        print_step_header("3DES Stage 2", "Encrypting with Key 2")
        res2 = des_process(res1, key2, "e", verbose)
        print_binary_data("Intermediate Result 2", res2)

        print_step_header("3DES Stage 3", "Decrypting with Key 1")
        final_res = des_process(res2, key1, "d", verbose)

    return final_res


# ==============================================================================
# SECTION 6: COMMAND-LINE INTERFACE (CLI)
# ==============================================================================


def get_block_cipher_input(prompt, key_prompt, key_count=1):
    """Helper to get user input for block ciphers."""
    text_hex = input(prompt + " (16 hex chars, e.g., 0123456789ABCDEF): ").strip()
    text_bin = hex_string_to_binary_list(text_hex, 64)
    if not text_bin or len(text_bin) != 64:
        print("\n[Error] Invalid input. Must be exactly 16 hexadecimal characters.")
        return None, None

    keys_bin = []
    for i in range(key_count):
        key_hex = input(key_prompt.format(i + 1) + " (16 hex chars): ").strip()
        key_bin = hex_string_to_binary_list(key_hex, 64)
        if not key_bin or len(key_bin) != 64:
            print(
                f"\n[Error] Invalid key {i+1}. Must be exactly 16 hexadecimal characters."
            )
            return None, None
        keys_bin.append(key_bin)

    return text_bin, keys_bin


def handle_des():
    mode = input("Choose mode: (e)ncrypt or (d)ecrypt: ").lower()
    if mode not in ["e", "d"]:
        return

    prompt_text = "Enter plaintext" if mode == "e" else "Enter ciphertext"
    text_bin, keys_bin = get_block_cipher_input(prompt_text, "Enter key {}", 1)

    if text_bin and keys_bin:
        verbose = input("Show step-by-step details? (y/n): ").lower() == "y"
        result_bin = des_process(text_bin, keys_bin[0], mode, verbose)
        print_section_header("Final Result")
        print_binary_data("Input", text_bin)
        print_binary_data("Output", result_bin)


def handle_3des():
    mode = input("Choose mode: (e)ncrypt or (d)ecrypt: ").lower()
    if mode not in ["e", "d"]:
        return

    key_type = input("Use (2) different keys or (3) different keys? ")
    if key_type not in ["2", "3"]:
        return

    key_count = int(key_type)
    prompt_text = "Enter plaintext" if mode == "e" else "Enter ciphertext"
    text_bin, keys_bin = get_block_cipher_input(prompt_text, "Enter key {}", key_count)

    if text_bin and keys_bin:
        verbose = (
            input("Show step-by-step details for each DES stage? (y/n): ").lower()
            == "y"
        )
        result_bin = tdes_process(
            text_bin,
            keys_bin[0],
            keys_bin[1],
            keys_bin[2] if key_count == 3 else None,
            mode,
            verbose,
        )
        print_section_header("Final Result")
        print_binary_data("Input", text_bin)
        print_binary_data("Output", result_bin)


def handle_math_tools():
    while True:
        print_section_header("Mathematical Tools")
        print("1. Euclidean GCD Algorithm")
        print("2. Extended Euclidean Algorithm (Multiplicative Inverse)")
        print("3. Polynomial GCD over GF(2)")
        print("0. Back to Main Menu")
        choice = input("> ")

        if choice == "1":
            try:
                a = int(input("Enter first integer (a): "))
                b = int(input("Enter second integer (b): "))
                print(f"Result: GCD({a}, {b}) = {gcd(a,b)}")
            except ValueError:
                print("[Error] Invalid input.")
        elif choice == "2":
            try:
                m = int(input("Enter modulus (m): "))
                b = int(input("Enter number to find inverse for (b): "))
                print(
                    f"Result: The multiplicative inverse of {b} mod {m} is {extended_euclidean(m, b)}"
                )
            except (ValueError, TypeError) as e:
                print(f"[Error] {e}")
        elif choice == "3":
            try:
                f_hex = input("Enter first polynomial in hex: ")
                g_hex = input("Enter second polynomial in hex: ")
                f_int = int(f_hex, 16)
                g_int = int(g_hex, 16)
                result = poly_gcd(f_int, g_int)
                print(f"Result: GCD is {hex(result)} ({bin(result)})")
            except ValueError:
                print("[Error] Invalid hex input.")
        elif choice == "0":
            break
        else:
            print("[Error] Invalid choice.")
        input("\nPress Enter to continue...")
        clear_screen()


def main_menu():
    """Main menu for the toolkit."""
    menu_map = {
        "1": ("Caesar Cipher", lambda: caesar_cipher("e")),
        "2": ("Caesar Cipher (Decrypt)", lambda: caesar_cipher("d")),
        "3": ("Monoalphabetic Cipher", lambda: monoalphabetic_substitution("e")),
        "4": (
            "Monoalphabetic Cipher (Decrypt)",
            lambda: monoalphabetic_substitution("d"),
        ),
        "5": ("Playfair Cipher", lambda: handle_playfair_cipher("e")),
        "6": ("Playfair Cipher (Decrypt)", lambda: handle_playfair_cipher("d")),
        "7": ("Vigenère Cipher", lambda: vigenere_cipher("e")),
        "8": ("Vigenère Cipher (Decrypt)", lambda: vigenere_cipher("d")),
        "9": ("Rail Fence Cipher", lambda: rail_fence_cipher("e")),
        "10": ("Rail Fence Cipher (Decrypt)", lambda: rail_fence_cipher("d")),
        "11": ("Row Transposition Cipher", lambda: row_transposition_cipher("e")),
        "12": (
            "Row Transposition Cipher (Decrypt)",
            lambda: row_transposition_cipher("d"),
        ),
        "13": ("DES", handle_des),
        "14": ("3DES", handle_3des),
        "15": ("Mathematical Tools", handle_math_tools),
        "16": ("Frequency Analysis Attack", handle_frequency_analysis),
        "0": ("Exit", sys.exit),
    }

    while True:
        clear_screen()
        print_section_header("Cryptographic Toolkit")
        print("--- Substitution Ciphers ---")
        print(" 1. Encrypt with Caesar Cipher")
        print(" 2. Decrypt with Caesar Cipher")
        print(" 3. Encrypt with Monoalphabetic Cipher")
        print(" 4. Decrypt with Monoalphabetic Cipher")
        print(" 5. Encrypt with Playfair Cipher")
        print(" 6. Decrypt with Playfair Cipher")
        print(" 7. Encrypt with Vigenère Cipher")
        print(" 8. Decrypt with Vigenère Cipher")
        print("\n--- Transposition Ciphers ---")
        print(" 9. Encrypt with Rail Fence Cipher")
        print("10. Decrypt with Rail Fence Cipher")
        print("11. Encrypt with Row Transposition Cipher")
        print("12. Decrypt with Row Transposition Cipher")
        print("\n--- Block Ciphers ---")
        print("13. DES (Encrypt/Decrypt)")
        print("14. 3DES (Encrypt/Decrypt)")
        print("\n--- Tools ---")
        print("15. Mathematical Tools")
        print("16. Frequency Analysis Attack")
        print("\n 0. Exit")

        choice = input("\nEnter your choice: ")

        if choice in menu_map:
            clear_screen()
            print_section_header(menu_map[choice][0])
            menu_map[choice][1]()
            input("\nPress Enter to return to the main menu...")
        else:
            print("\n[Error] Invalid choice. Please try again.")
            input("Press Enter to continue...")


# ==============================================================================
# SECTION 7: MAIN EXECUTION BLOCK
# ==============================================================================


def self_test_des():
    print_section_header("INTERNAL DES SELF-TEST")
    plaintext_hex = "0123456789ABCDEF"
    key_hex = "133457799BBCDFF1"
    expected_ciphertext_hex = "85E813540F0AB405"

    p_bin = hex_string_to_binary_list(plaintext_hex, 64)
    k_bin = hex_string_to_binary_list(key_hex, 64)

    print(f"Test Plaintext: {plaintext_hex}")
    print(f"Test Key:       {key_hex}")

    c_bin = des_process(p_bin, k_bin, "e", verbose=False)
    c_hex = binary_to_hex(c_bin)

    print(f"Expected Ciphertext:  {expected_ciphertext_hex}")
    print(f"Actual Ciphertext:    {c_hex}")

    if c_hex == expected_ciphertext_hex:
        print("\n[SUCCESS] DES implementation matches the known test vector.")
    else:
        print("\n[FAILURE] DES implementation does NOT match the known test vector.")
    print("=" * 70)


if __name__ == "__main__":
    try:
        self_test_des()
        input("\nPress Enter to start the toolkit...")
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting program. Goodbye!")
        sys.exit(0)
