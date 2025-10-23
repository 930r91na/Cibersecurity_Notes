# Block Cipher Modes of Operation

# This module implements various block cipher modes of operation for symmetric encryption algorithms using the DES and AES algorithms 
# Modes included:
# 1. ECB (Electronic Codebook)
# 2. CBC (Cipher Block Chaining)
# 3. CFB (Cipher Feedback)
# 4. OFB (Output Feedback)
# 5. CTR (Counter)

# Import necessary cryptographic functions and utilities


# ECB (Electronic Codebook) Mode
# In ECB mode, each block of plaintext is encrypted independently using the same key.
# This mode is simple but can be insecure for certain types of data due to pattern leakage.



# CBC (Cipher Block Chaining) Mode
# In CBC mode, each block of plaintext is XORed with the previous ciphertext block before being encrypted.
# This creates dependency between blocks, enhancing security.
# An initialization vector (IV) is used for the first block to ensure uniqueness.
# This mode provides better security than ECB by introducing dependency between blocks.


# CFB (Cipher Feedback) Mode
# In CFB mode, the previous ciphertext block is encrypted and the output is XORed with the current plaintext block to produce the ciphertext.
# This mode allows encryption of data in units smaller than the block size and can operate as a stream cipher.
# It is useful for applications that require real-time encryption and decryption, such as video streaming or online gaming.

# OFB (Output Feedback) Mode
# In OFB mode, the previous output block is encrypted and the output is XORed with the current plaintext block to produce the ciphertext.
# This mode also allows encryption of data in units smaller than the block size and can operate as a stream cipher.
# OFB mode is less error-prone than CFB since errors in the ciphertext do not propagate to subsequent blocks.

# Counter (CTR) Mode
# In CTR mode, a counter value is combined with a nonce and encrypted to produce a keystream block.
# This keystream block is then XORed with the plaintext block to produce the ciphertext.
# CTR mode allows for parallel processing of blocks, making it efficient for high-speed applications.
# It is widely used in modern cryptographic applications due to its efficiency and security.

