# ==================== Transposition Ciphers ====================
# Transposition ciphers rearrange the letters of the plaintext to create the ciphertext.
# Unlike substitution ciphers, they do not change the actual letters but rather their positions.
# These hide the message by rearranging the letter order without altering the actual letters used
# Common types of transposition ciphers include rail fence cipher and columnar transposition cipher.

# ==================== Rail Fence Cipher ====================
# The rail fence cipher is a form of transposition cipher that writes the message in a zigzag pattern across multiple "rails" (rows) and then reads it off row by row to create the ciphertext.

# PROBLEMS WITH RAIL FENCE CIPHER:
# 1. Vulnerable to frequency analysis if the number of rails is known.

def rail_fence_encrypt(plaintext, num_rails):
    # Create a list of strings for each rail
    rails = ['' for _ in range(num_rails)]
    rail = 0
    direction = 1  # 1 for down, -1 for up

    for char in plaintext:
        rails[rail] += char
        rail += direction

        # Change direction if we hit the top or bottom rail
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    # Concatenate all rails to get the ciphertext
    ciphertext = ''.join(rails)

    print(f"Rail Fence Cipher - Encryption:")
    for i, rail in enumerate(rails):
        for j in range(len(rail)):
            # Print characters in zigzag pattern with spaces
            if (j % (2 * (num_rails - 1))) < num_rails:
                print(rail[j], end=' ')
            else: print('  ', end=' ')
        print()  # New line after each rail
    return ciphertext

def rail_fence_decrypt(ciphertext, num_rails):
    """Decrypts ciphertext using rail fence cipher with a given number of rails."""
    # Create a matrix to mark the positions of characters
    rail_matrix = [['\n' for _ in range(len(ciphertext))] for _ in range(num_rails)]
    rail = 0
    direction = 1  # 1 for down, -1 for up  
    for i in range(len(ciphertext)):
        rail_matrix[rail][i] = '*'
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1
    index = 0
    for i in range(num_rails):
        for j in range(len(ciphertext)):
            if (rail_matrix[i][j] == '*' and index < len(ciphertext)):
                rail_matrix[i][j] = ciphertext[index]
                index += 1
    plaintext = ''
    rail = 0
    for i in range(len(ciphertext)):
        rail = i % num_rails
        plaintext += rail_matrix[rail][i]
        if rail == 0 or rail == num_rails - 1:
            direction *= -1
        rail += direction

    print(f"Rail Fence Cipher rail_matrix")
    for row in rail_matrix:
        print(' '.join(row).replace('\n', ' '))
    return plaintext

# ==================== ROW TRANSPOSITION CIPHER ====================
# The row transposition cipher is a form of transposition cipher that rearranges the characters in each row of a grid.
# It uses a keyword to determine the order of the columns for encryption and decryption.

# PROBLEMS WITH ROW TRANSPOSITION CIPHER:
# 1. Vulnerable to frequency analysis if the keyword is known or can be guessed.

def row_transposition_encrypt(plaintext, keyword):
    # Remove spaces and create a grid
    plaintext = plaintext.replace(" ", "")
    grid = []
    for i in range(0, len(plaintext), len(keyword)):
        grid.append(plaintext[i:i + len(keyword)])

    # Pad the last row if necessary
    if len(grid[-1]) < len(keyword):
        grid[-1] += 'X' * (len(keyword) - len(grid[-1]))

    # Create a list of columns based on the keyword
    columns = ['' for _ in range(len(keyword))]
    for char in keyword:
        index = ord(char) - ord('A')
        columns[index] = ''.join(row[index] for row in grid)

    # Concatenate all columns to get the ciphertext
    ciphertext = ''.join(columns)
    return ciphertext

def row_transposition_decrypt(ciphertext, keyword):
    # Create a grid for the ciphertext
    num_rows = len(ciphertext) // len(keyword)
    grid = [['' for _ in range(len(keyword))] for _ in range(num_rows)]

    # Fill the grid column by column based on the keyword
    col = 0
    for char in keyword:
        index = ord(char) - ord('A')
        for row in range(num_rows):
            grid[row][index] = ciphertext[col]
            col += 1

    # Read the grid row by row to get the plaintext
    plaintext = ''.join(''.join(row) for row in grid).replace('X', '')
    return plaintext

# Test the rail fence cipher
if __name__ == "__main__":
    # Example usage rail fence cipher
    print("=== Rail Fence Cipher Test ===")
    plaintext = "meetmeafterthetogaparty"
    num_rails = 2
    encrypted = rail_fence_encrypt(plaintext, num_rails)
    print("Encrypted:", encrypted)
    decrypted = rail_fence_decrypt(encrypted, num_rails)
    print("Decrypted:", decrypted)

    # Example usage row transposition cipher
    print("\n=== Row Transposition Cipher Test ===")
    plaintext = "ennemyattackstonight"
    keyword = [3, 1, 4, 5, 2] 
    encrypted = row_transposition_encrypt(plaintext, keyword)
    print("Encrypted:", encrypted)
    decrypted = row_transposition_decrypt(encrypted, keyword)
    print("Decrypted:", decrypted)