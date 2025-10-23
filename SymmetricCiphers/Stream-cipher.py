

from formatting_utils import (
    format_binary_grouped,
    binary_to_hex,
    print_section_header,
    print_binary_data,
    print_step_header
)

# RC4 key scheduling algorithm (KSA)
def KSA(s_len, input_key):
    
    # Initialize S and T
    for i in range(s_len):
        S[i] = i
        T

    # Initial permutation of S
    j = 0
    for i in range(s_len):
        j = (j + S[i] + input_key[i % len(input_key)]) % s_len
        S[i], S[j] = S[j], S[i]  # Swap

        
    return S

def PRGA(S, plaintext_length):
    # Pseudo-Random Generation Algorithm (PRGA)
    # Reset i and j 
    # Obtain S from KSA
    i = 0
    j = 0
    S = KSA(S)

    # Change i and j 
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]  # Swap

    # Locate t and k
    t = (S[i] + S[j]) % 256
    k = S[t]
    return k

def stream_cipher(plaintext):
    initial_vector = bytearray(plaintext)

if __name__ == "__main__":
    print("RC4 Stream Cipher Example")
    S = [0,1,2,3]
    M = "HI"
    K = {1,7}

    key_schedule(list(K))
    stream_cipher(M)