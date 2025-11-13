

from formatting_utils import (
    format_binary_grouped,
    binary_to_hex,
    print_section_header,
    print_binary_data,
    print_step_header
)

# RC4 key scheduling algorithm (KSA)
def KSA(s_len, input_key):
    S = []
    T = []
    for i in range(s_len):
        S.append(i)
        T.append(input_key[i % len(input_key)])

    print_section_header("RC4 Key Scheduling Algorithm (KSA)")
    print(f"Initial S: {S}")
    # Initial permutation of S
    j = 0
    for i in range(s_len):
        print_step_header(f"KSA Step {i+1}:", "Step description")
        print(f"  Before: i={i}, j={j}, S={S}")
        j = (j + S[i] + T[i]) % s_len
        print(f"  Updated j = (j + S[i] + T[i]) mod {s_len} = ({j} + {S[i]} + {T[i]}) mod {s_len} = {j}")
        print(f"  After: i={i}, j={j}, S={S}")
        S[i], S[j] = S[j], S[i]  # Swap
        print(f"  Swapped S: {S}\n")

    return S

def PRGA(S, M):
    """
    Pseudo-Random Generation Algorithm (PRGA) for RC4.
    """
    i, j = 0, 0  # Initialize i and j
    key_stream = []  # Store generated keystream bytes
    encrypted_message = []  # Store the XOR results (encrypted output)

    print(f"Reset i = j = 0, Recall S = {S}\n")

    for char in M:
        # Step 1: Increment i
        print(f"i = (i + 1) = {i+1} (mod {len(S)})")
        i = (i + 1) % len(S)

        # Step 2: Update j
        print(f"j = (j + S[i]) = ({j} + {S[i]}) = {j + S[i]} (mod {len(S)})")
        j = (j + S[i]) % len(S)


        # Step 3: Swap S[i] and S[j]
        S[i], S[j] = S[j], S[i]
        print(f"Swap (S[i] and S[j]): S = {S}")

        # Step 4: Generate t and k
        t = (S[i] + S[j]) % len(S)
        k = S[t]
        key_stream.append(k)
        print(f"t = (S[i] + S[j]) mod {len(S)} = ({S[i]} + {S[j]}) mod {len(S)} = {t}")
        print(f"Output k = S[{t}] = {k}\n")

        # Step 5: XOR the keystream with the plaintext character
        char_bin = format(ord(char), '08b')  # Convert character to binary
        k_bin = format(k, '08b')             # Convert keystream byte to binary
        result = ord(char) ^ k               # XOR operation
        character = chr(result)              # Directly convert integer to ASCII
        encrypted_message.append(character)

        print(f"{char}    ({char_bin})")
        print(f"XOR")
        print(f"      {k_bin}")
        print(f"=     {format(result, '08b')} (encrypted)\n")

    print("Final Key Stream: ", key_stream)
    print("Encrypted Message (in decimal): ", encrypted_message)




if __name__ == "__main__":
    print("RC4 Stream Cipher Example")
    M = "MEET"
    K = {1,2,3,6}

    S = KSA(8, list(K))
    print(f"Final S from KSA: {S}")

    print("\nGenerating keystream and encrypting plaintext:")
    PRGA(S, M)