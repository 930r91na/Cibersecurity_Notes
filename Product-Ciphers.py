# Product Ciphers


#Plaintext: HOWAREYOU (7 14 22 0 17 4 24 14 20) +Keyword: NCBTZQARX (13 2 1 19 25 16 0 17 23)
#2 0 16 23 19 42 20 24 31 43 mod (26)
#Ciphertext: UQXTQUYFR(20 16 23 19 16 20 24 5 17) ‐Keyword: NCBTZQARX (13 2 1 19 25 16 0 17 23) Hence consider using several ciphers in succession to make harder, but:
#• two substitutions make a more complex substitution.
#• two transpositions make more complex transposition.
#• but a substitution followed by a transposition makes a new much harder cipher.

def product_cipher(plaintext, keyword):
    # Step 1: Encrypt the plaintext using the first cipher (e.g., Vigenère)
    
    return final_ciphertext
