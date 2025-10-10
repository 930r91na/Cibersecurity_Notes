from formatting_utils import print_section_header, print_step_header
# ==================== Transposition Ciphers ====================
# Transposition ciphers rearrange the letters of the plaintext to create the ciphertext.
# Unlike substitution ciphers, they do not change the actual letters but rather their positions.
# These hide the message by rearranging the letter order without altering the actual letters used
# Common types of transposition ciphers include rail fence cipher and columnar transposition cipher.

# ==================== Rail Fence Cipher ====================
# The rail fence cipher is a form of transposition cipher that writes the message in a zigzag pattern across multiple "rails" (rows) and then reads it off row by row to create the ciphertext.

# PROBLEMS WITH RAIL FENCE CIPHER:
# 1. Vulnerable to frequency analysis if the number of rails is known.

def rail_fence_encrypt(text, num_rails):
    """Encrypt plaintext using Rail Fence cipher."""
    if num_rails <= 1:
        return text  # No encryption needed for 1 rail
    print_step_header(1, "Distributing plaintext characters onto rails in a zigzag pattern")
    
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

def rail_fence_decrypt(text, num_rails):
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


def rail_fence_cipher(mode):
    """Handler for Rail Fence cipher."""
    try:
        if mode not in ['e', 'd']:
            raise ValueError("Mode must be 'e' for encryption or 'd' for decryption.")
        if mode == 'e':
            plaintext = input("Enter the plaintext: ").replace(" ", "").upper()
            num_rails = int(input("Enter the number of rails (>=2): "))
            if num_rails < 2:
                raise ValueError("Number of rails must be at least 2.")
            print_section_header("RAIL FENCE CIPHER - ENCRYPTION")
            result = rail_fence_encrypt(plaintext, num_rails)
        else:
            ciphertext = input("Enter the ciphertext: ").replace(" ", "").upper()
            num_rails = int(input("Enter the number of rails (>=2): "))
            if num_rails < 2:
                raise ValueError("Number of rails must be at least 2.")
            print_section_header("RAIL FENCE CIPHER - DECRYPTION")
            result = rail_fence_decrypt(ciphertext, num_rails)

        print_section_header("Result")
        print(f"{'Ciphertext' if mode == 'e' else 'Plaintext'}: {result}")
    except ValueError:
        print("Invalid input. Please enter a valid number of rails.")            
        




# ==================== ROW TRANSPOSITION CIPHER ====================
# The row transposition cipher is a form of transposition cipher that rearranges the characters in each row of a grid.
# It uses a keyword to determine the order of the columns for encryption and decryption.

# PROBLEMS WITH ROW TRANSPOSITION CIPHER:
# 1. Vulnerable to frequency analysis if the keyword is known or can be guessed.

def row_transposition_encrypt(text, keyword):
    key_order = sorted(range(len(keyword)), key=lambda k: keyword[k])
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
    return ciphertext

def row_transposition_decrypt(text, keyword):
    key_order = sorted(range(len(keyword)), key=lambda k: keyword[k])
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
    return result    

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
            row_transposition_encrypt(text, keyword)
        else:  # Decrypt
            row_transposition_decrypt(text, keyword)

        print_section_header("Result")
        print(f"{'Ciphertext' if mode == 'e' else 'Plaintext'}: {result}")

    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")


# Test the rail fence cipher
if __name__ == "__main__":
    # Example usage rail fence cipher
    print("=== Rail Fence Cipher Test ===")
    plaintext = "meetmeafterthetogaparty"
    num_rails = 3
    encrypted = rail_fence_encrypt(plaintext, num_rails)
    print("Encrypted:", encrypted)
    #decrypted = rail_fence_decrypt(encrypted, num_rails)
    #print("Decrypted:", decrypted)

    # Example usage row transposition cipher
    print("\n=== Row Transposition Cipher Test ===")
    plaintext = "ennemyattackstonight"
    keyword = [3, 1, 4, 5, 2] 
    encrypted = row_transposition_encrypt(plaintext, keyword)
    print("Encrypted:", encrypted)
    decrypted = row_transposition_decrypt(encrypted, keyword)
    print("Decrypted:", decrypted)