# Substitution Ciphers
# - Caesar Cipher
# - Monoalphabetic Substitution Cipher
# - Vigenère Cipher


# =================== Caesar Cipher ===================#
# This cypher is also known as a shift cipher.
# Each letter in the plaintext is 'shifted' a certain number of places down or up the alphabet.

# PROBLEMS WITH CAESAR CIPHER:
# 1. Limited number of possible keys (25 possible shifts in English alphabet)
# 2. Frequency analysis can easily break the cipher (e.g., 'E' is the most common letter in English)
# 3. Only works with alphabetic characters, non-alphabetic characters are not encrypted

def caesar_cipher_encrypt(plaintext, shift, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Encrypts plaintext using Caesar cipher with a given shift."""
    ciphertext = ""
    for char in plaintext:
        if char.upper() in alphabet:
            print(f"Char: {char} -> Index: {alphabet.index(char.upper())} Shift: {shift} -> New Index: {(alphabet.index(char.upper()) + shift) % 26} -> New Char: {alphabet[(alphabet.index(char.upper()) + shift) % 26]}")
            shifted_index = (alphabet.index(char.upper()) + shift) % 26
            if char.isupper():
                ciphertext += alphabet[shifted_index]
            else:
                ciphertext += alphabet[shifted_index].lower()
        else:
            ciphertext += char
    return ciphertext


def caesar_cipher_decrypt(ciphertext, shift, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Decrypts ciphertext using Caesar cipher with a given shift."""
    return caesar_cipher_encrypt(ciphertext, -shift, alphabet)


# =================== Monoalphabetic Substitution Cipher ===================#
# Each letter in the plaintext is replaced by a letter with some fixed relationship to it.
# The alphabet is not shifted but rather scrambled.
# Each letter maps to a unique letter.
# The number of possible keys is 26! (factorial of 26), making brute-force attacks impractical, because there are 4x10^26 possible keys.

# PROBLEMS WITH MONOALPHABETIC SUBSTITUTION CIPHER:
# 1. Vulnerable to frequency analysis (e.g., 'E' is the most common letter in English) aka language characteristics
# 2. Still only works with alphabetic characters, non-alphabetic characters are not encrypted


def monoalphabetic_substitution_encrypt(plaintext, key, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Encrypts plaintext using a monoalphabetic substitution cipher with a given key."""
    ciphertext = ""
    for char in plaintext:
        if char.upper() in alphabet:
            index = alphabet.index(char.upper())
            print(f"Char: {char} -> Index: {index} -> New Char: {key[index]}")
            if char.isupper():
                ciphertext += key[index]
            else:
                ciphertext += key[index].lower()
        else:
            ciphertext += char
    return ciphertext

def monoalphabetic_substitution_decrypt(ciphertext, key, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Decrypts ciphertext using a monoalphabetic substitution cipher with a given key."""
    reverse_key = [''] * 26
    for i, char in enumerate(key):
        print(f"Key Char: {char} -> Index: {i} -> Reverse Key Char: {alphabet[i]}")
        reverse_key[alphabet.index(char)] = alphabet[i]
    return monoalphabetic_substitution_encrypt(ciphertext, ''.join(reverse_key), alphabet)

english_letter_frequency = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
    'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
    'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
    'Q': 0.1, 'Z': 0.07
}

def frequency_analysis(text):
    """Performs frequency analysis on the given text."""
    frequency = {}
    total_letters = 0
    for char in text.upper():
        if char.isalpha():
            frequency[char] = frequency.get(char, 0) + 1
            total_letters += 1
    for char in frequency:
        frequency[char] = (frequency[char] / total_letters) * 100

    frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))
    return frequency

def frequency_analysis_compare(frequency):
    """Compares the frequency analysis result with standard English letter frequency and associates letters."""
    comparison = {}
    sorted_freq = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    sorted_english = sorted(english_letter_frequency.items(), key=lambda item: item[1], reverse=True)
    for (char1, _), (char2, _) in zip(sorted_freq, sorted_english):
        comparison[char1] = char2

    # Print comparison table
    print(f"{'Cipher Letter':<15}{'Frequency (%)':<15}{'Mapped to English Letter':<25}")
    print("-" * 55)
    for char, freq in frequency.items():
        mapped_char = comparison.get(char, '?')
        print(f"{char:<15}{freq:<15.2f}{mapped_char:<25}")

    return comparison

# =================== Polygraphic Ciphers ===================
# It uses multiple cipher alphabets to encrypt the data.
# Make cryptanalysis harder with more alphabets to guess and flatter the frequency distribution.
# Make frequency analysis more difficult.

# Example: Playfair cipher, Hill cipher, Vigenère cipher

# ================== Vigenère Cipher ===================#
# This cipher uses a keyword to shift letters in the plaintext.
# - simplest polyalphabetic substitution cipher.
# - effectively multiple Caesar ciphers.
# - key is multiple letters long K = k0 k1 ... km-1
# - repeat from start after m letters in message.
# - decryption simply works in reverse.

# Steps to encrypt:
# 1. Write down the plaintext.
# 2. Write the key above the plaintext, repeating it as necessary.
# 3. For each letter in the plaintext, shift it by the position of the corresponding key letter.

# PROBLEMS WITH VIGENÈRE CIPHER:
# 1. Vulnerable to Kasiski examination and Friedman test (to determine key length)
# 2. If the key is shorter than the plaintext, patterns may emerge.

vigenere_table = [[chr((i + j) % 26 + ord('A')) for j in range(26)] for i in range(26)]
# Print Vigenère table
def print_vigenere_table():
    for row in vigenere_table:
        print(' '.join(row))

def vigenere_cipher_encrypt(plaintext, key):
    """Encrypts plaintext using Vigenère cipher with a given key."""
    ciphertext = ""
    key = key.upper()
    key_length = len(key)
    key_index = 0

    for char in plaintext:
        if char.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            row = ord(key[key_index % key_length]) - ord('A')
            col = ord(char.upper()) - ord('A')
            encrypted_char = vigenere_table[row][col]
            print(f"Char: {char} -> Key Char: {key[key_index % key_length]} -> Encrypted Char: {encrypted_char}")
            if char.isupper():
                ciphertext += encrypted_char
            else:
                ciphertext += encrypted_char.lower()
            key_index += 1
        else:
            ciphertext += char
    return ciphertext

def vigenere_cipher_decrypt(ciphertext, key):
    """Decrypts ciphertext using Vigenère cipher with a given key."""
    plaintext = ""
    key = key.upper()
    key_length = len(key)
    key_index = 0

    for char in ciphertext:
        if char.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            row = ord(key[key_index % key_length]) - ord('A')
            col = vigenere_table[row].index(char.upper())
            decrypted_char = chr(col + ord('A'))
            print(f"Char: {char} -> Key Char: {key[key_index % key_length]} -> Decrypted Char: {decrypted_char}")
            if char.isupper():
                plaintext += decrypted_char
            else:
                plaintext += decrypted_char.lower()
            key_index += 1
        else:
            plaintext += char
    return plaintext

# ===================== PLAYFAIR CIPHER =====================#
# Not even the large number of keys in a monoalphabetic cipher provides better security.
# One approach to improving security was to encrypt multiple letters.

# Steps to create a Playfair matrix:
# 1. Choose a keyword (e.g., "KEYWORD").
# 2. Remove duplicate letters from the keyword.
# 3. Fill the matrix with the letters of the keyword, followed by the remaining letters of the alphabet (combine I/J).
# 4. The matrix will be 5x5, containing 25 letters (I and J share a cell).

def create_playfair_matrix(key):
    """Creates a 5x5 Playfair matrix from the given key."""
    key = key.upper().replace('J', 'I')  # Combine I and J
    matrix = []
    used_chars = set()

    for char in key:
        if char not in used_chars and char.isalpha():
            used_chars.add(char)
            matrix.append(char)

    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # Note: 'J' is omitted
        if char not in used_chars:
            used_chars.add(char)
            matrix.append(char)

    print("Playfair Matrix for key '{}':".format(key))
    for row in [matrix[i:i + 5] for i in range(0, 25, 5)]:
        print(" ".join(row))

    return [matrix[i:i + 5] for i in range(0, 25, 5)]


# Steps to encrypt using Playfair cipher:
# 1. Split the plaintext into digraphs (pairs of letters). If a pair consists of the same letter, insert an 'X' between them.
# 2. If there's an odd letter out, append an 'X' to the end.
# 3. For each digraph:
#    - If both letters are in the same row, replace them with the letters to their immediate right (wrap around to the start of the row if needed).
#    - If both letters are in the same column, replace them with the letters immediately below (wrap around to the top if needed).
#    - If the letters form a rectangle, replace them with the letters on the same row but at the opposite corners of the rectangle.

# Note: Decryption follows the same rules but in reverse (left for row, up for column).

def playfair_cipher_encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    print("Playfair Matrix for key '{}':".format(key))
    for row in matrix:
        print(" ".join(row))
    char_position = {matrix[i][j]: (i, j) for i in range(5) for j in range(5)}  
    plaintext = plaintext.upper().replace('J', 'I').replace(' ', '')
    digraphs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = ''
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
        if a == b or b == '':
            digraphs.append((a, 'X'))
            i += 1
        else:
            digraphs.append((a, b))
            i += 2
    ciphertext = ""
    for a, b in digraphs:
        row_a, col_a = char_position[a]
        row_b, col_b = char_position[b]
        if row_a == row_b:
            ciphertext += matrix[row_a][(col_a + 1) % 5]
            ciphertext += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a]
            ciphertext += matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b]
            ciphertext += matrix[row_b][col_a]
        print(f"Digraph: {a}{b} -> Encrypted Digraph: {ciphertext[-2:]}")

    return ciphertext

def playfair_cipher_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    char_position = {matrix[i][j]: (i, j) for i in range(5) for j in range(5)}  
    digraphs = [(ciphertext[i], ciphertext[i + 1]) for i in range(0, len(ciphertext), 2)]
    plaintext = ""
    for a, b in digraphs:
        row_a, col_a = char_position[a]
        row_b, col_b = char_position[b]
        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5]
            plaintext += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a]
            plaintext += matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b]
            plaintext += matrix[row_b][col_a]
        print(f"Digraph: {a}{b} -> Decrypted Digraph: {plaintext[-2:]}")
    return plaintext

if __name__ == "__main__":
    print("Substitution Ciphers module loaded. Implement specific ciphers as needed.")
    # Example usage caesar cipher
    print("\n=== Caesar Cipher Test ===")
    plaintext = "meet me after the toga party"
    shift = 3
    print("Plaintext:", plaintext)
    encrypted = caesar_cipher_encrypt(plaintext, shift)
    print("Encrypted:", encrypted)
    decrypted = caesar_cipher_decrypt(encrypted, shift)
    print("Decrypted:", decrypted)

    # Example usage monoalphabetic substitution cipher
    print("\n=== Monoalphabetic Substitution Cipher Test ===")
    plaintext = "ifwewishtoreplaceletters"
    key = "DKVQFIBJWPESCXHTMYAUOLRGZN"
    print("Plaintext:", plaintext)
    encrypted = monoalphabetic_substitution_encrypt(plaintext, key)
    print("Encrypted:", encrypted)
    decrypted = monoalphabetic_substitution_decrypt(encrypted, key)
    print("Decrypted:", decrypted)

    # Example usage frequency analysis
    print("\n=== Frequency Analysis Test ===")
    text = "UZQSOVUOHXMOPVGPOZPEVSGZWSZOPFPESXUDBMETSXAIZVUEPHZHMDZSHZWSFPAPPDTSVPQUZWYMXUZUHSXEPYEPOPDZSZUFPOMBZWPFUPZHMDJUDTMOHMQ"
    frequency = frequency_analysis(text)
    print("Frequency Analysis:", frequency)
    comparison = frequency_analysis_compare(frequency)


    # Example usage vigenere cipher
    print("\n=== Vigenère Cipher Test ===")
    print("\nVigenère Table:")
    print_vigenere_table()

    plaintext = "wearediscoveredsaveyourself"
    key = "DECEPTIVE"

    # without autokey system
    print("Plaintext:", plaintext)
    print("Key:", key)
    encrypted = vigenere_cipher_encrypt(plaintext, key)
    print("Encrypted:", encrypted)
    decrypted = vigenere_cipher_decrypt(encrypted, key)
    print("Decrypted:", decrypted)

    # with autokey system
    # Here the keyword is concatenated with the plaintext to form the key.
    print("\n=== Vigenère Cipher with Autokey System Test ===")
    plaintext = "wearediscoveredsaveyourself"
    key = "DECEPTIVE" + plaintext[:-len("DECEPTIVE")]
    print("Plaintext:", plaintext)
    print("Key (Autokey):", key)
    encrypted = vigenere_cipher_encrypt(plaintext, key)
    print("Encrypted:", encrypted)
    decrypted = vigenere_cipher_decrypt(encrypted, key)
    print("Decrypted:", decrypted)

    # Example usage playfair cipher
    print("\n=== Playfair Cipher Test ===")
    



    