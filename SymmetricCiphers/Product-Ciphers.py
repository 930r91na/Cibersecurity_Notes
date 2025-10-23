# Product Ciphers


#Plaintext: HOWAREYOU (7 14 22 0 17 4 24 14 20) +Keyword: NCBTZQARX (13 2 1 19 25 16 0 17 23)
#2 0 16 23 19 42 20 24 31 43 mod (26)
#Ciphertext: UQXTQUYFR(20 16 23 19 16 20 24 5 17) ‐Keyword: NCBTZQARX (13 2 1 19 25 16 0 17 23) Hence consider using several ciphers in succession to make harder, but:
#• two substitutions make a more complex substitution.
#• two transpositions make more complex transposition.
#• but a substitution followed by a transposition makes a new much harder cipher.

def product_cipher_encrypt(plaintext, keyword):
    # Step 1: Write plaintext in int values A=0, B=1,...,Z=25
    plaintext = plaintext.replace(" ", "").upper()
    plain_nums = [ord(c) - ord('A') for c in plaintext]
    print(f"Plaintext:        {plaintext}")
    
    # Write keyword in int values A=0, B=1,...,Z=25
    keyword = keyword.replace(" ", "").upper()
    key_nums = [ord(c) - ord('A') for c in keyword]
    print(f"Keyword:          {keyword}")

    # Add values 
    added = [(p + k) for p, k in zip(plain_nums, key_nums)]
    
    # Apply mod 26
    modded = [x % 26 for x in added]
    
    # Convert back to letters
    final_ciphertext = ''.join(chr(n + ord('A')) for n in modded)
    
    # Format aligned vectors
    print("\nStep-by-step calculation:")
    print("Plaintext nums:  ", end="")
    for num in plain_nums:
        print(f"{num:3d}", end="")
    print()
    
    print("Keyword nums:    ", end="")
    for num in key_nums:
        print(f"{num:3d}", end="")
    print()
    
    print("Added values:    ", end="")
    for num in added:
        print(f"{num:3d}", end="")
    print()
    
    print("Mod 26 values:   ", end="")
    for num in modded:
        print(f"{num:3d}", end="")
    print()
    
    print(f"\nFinal cipher:     {final_ciphertext}")
    
    return final_ciphertext

def product_cipher_decrypt(ciphertext, keyword):
    # Step 1: Write ciphertext in int values A=0, B=1,...,Z=25
    ciphertext = ciphertext.replace(" ", "").upper()
    cipher_nums = [ord(c) - ord('A') for c in ciphertext]
    print(f"Ciphertext:       {ciphertext}")
    
    # Write keyword in int values A=0, B=1,...,Z=25
    keyword = keyword.replace(" ", "").upper()
    key_nums = [ord(c) - ord('A') for c in keyword]
    print(f"Keyword:          {keyword}")

    # Subtract values 
    subtracted = [(c - k) for c, k in zip(cipher_nums, key_nums)]
    
    # Apply mod 26
    modded = [x % 26 for x in subtracted]
    
    # Convert back to letters
    final_plaintext = ''.join(chr(n + ord('A')) for n in modded)
    
    # Format aligned vectors
    print("\nStep-by-step calculation:")
    print("Cipher nums:     ", end="")
    for num in cipher_nums:
        print(f"{num:3d}", end="")
    print()
    
    print("Keyword nums:    ", end="")
    for num in key_nums:
        print(f"{num:3d}", end="")
    print()
    
    print("Subtracted vals: ", end="")
    for num in subtracted:
        print(f"{num:3d}", end="")
    print()
    
    print("Mod 26 values:   ", end="")
    for num in modded:
        print(f"{num:3d}", end="")
    print()
    
    print(f"\nFinal plaintext:  {final_plaintext}")
    
    return final_plaintext

if __name__ == "__main__":
    plaintext = "WEAREDISCOVEREDSAVEYOURSELF"
    keyword =   "ZHBVCXSERTZUIKMNBVGTZUIOLKM"
    
    print("=" * 50)
    print("ENCRYPTION")
    print("=" * 50)
    final_ciphertext = product_cipher_encrypt(plaintext, keyword)
    
    print("\n" + "=" * 50)
    print("DECRYPTION")
    print("=" * 50)
    final_plaintext = product_cipher_decrypt(final_ciphertext, keyword)