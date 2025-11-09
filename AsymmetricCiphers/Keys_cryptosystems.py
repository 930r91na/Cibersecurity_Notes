 
 # Public Key Encryption 
# Uses 2 keys: a public key and a private key
# Asymmetric since parties are not equal
# Complements rather than replaces symmetric encryption


# Provides confidentiality
# A gives Ka+ to trusted authority
# B gives Kb+ to trusted authority
# Trusted authority creates encrypted session key certificates
# Trusted authority sends encrypted session key certificates to A (has Cb) and B (has Ca)
# A sends 

# A - Ka+ , Ka- 
# A recives Cb from Trusted authority
# C = E(Kb+, Kab)
# P = D(Caes, Kab
# A send Ckab to B
# B send Caes to A


# Authentication with digital signatures
# A gives Ka+ to trusted authority
# B gives Kb+ to trusted authority
# Trusted authority creates signed public key certificates
# Trusted authority sends signed public key certificates to A (has Kb+) and B (has Ka+)

# A wants to send P to B
# A creates C = E(P, Ka-) - digital signature
# B recives C from A
# B decrypts P = D(C, Ka+) - verifies signature
# B gets the text P and knows it came from A since only A has Ka-



# RSA *(Rivest, Shamir, Adleman)*

