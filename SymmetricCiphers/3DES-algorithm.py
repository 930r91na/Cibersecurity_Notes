# DES is vulnerable to BFA, because the possible values of the 56 -bit keys have 2^56 = 7.2 x 10^16 = 1999 breaked in 22 hours
# Therefore the alternative is 3DES (TDEA) or AES (Advanced Encryption Standard)
#     This are encryption of the type Block Symmetric Crypher
# 3DES is based on DES, but it applies the DES algorithm three times to each data block.
# The key length is 168 bits (3 x 56 bits) or 112 bits (2 x 56 bits)
# The block length is 64 bits
# This implied more computational time, but it is more secure than DES
# It allowed the reuse of DES hardware and software

# Encryption: process
# P -> Encrypt with K1 -> D (Decrypt with K2) -> Encrypt with K1 -> C
# Decryption: process
# C -> Decrypt with K3 -> E (Encrypt with K2) -> Decrypt with K1 -> P


# Process for 2 keys (112 bits)
# Encrypt Process:
# X = Encrypt(P,K1)
# C = Encrypt(X,K2)

# Decrypt Process:
# X = Decrypt(C,K2)
# P = Decrypt(X,K1)

# NOTE: K1 and K2 must be different if not the process is equivalent to DES

# Process for 3 keys (168 bits)
# Encrypt Process:
# X = Encrypt(P,K1)
# Y = Encrypt(X,K2)
# C = Encrypt(Y,K3)

# Decrypt Process:
# Y = Decrypt(C,K3)
# X = Decrypt(Y,K2)
# P = Decrypt(X,K1)

# Application:
# PGP (Pretty Good Privacy), SSL/TLS (Secure Sockets Layer/Transport Layer Security) protocol for secure web browsing (HTTPS)
# S/MIME (Secure/Multipurpose Internet Mail Extensions) for secure email

# Expired standard on  July 18 2018
