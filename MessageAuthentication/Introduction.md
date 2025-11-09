The security services that are missing to be provided is 
Data Integrity and Non repudation 
The most common cryptograohic techiniques for message authentication are

MAC and SHA


MAC
Message Authentication code 

A wants to send M
M generates MACa =  C(M, Kab)
MACa is appended to M
M + MACa is encrypted and send to B
B receives  M + MACa and computes also the MAC
MACb = C(M, Kab)
If MACa is equal MACb the non repudation and data integrity is provided

Hash function H(M)
Hash code = signature

M(1000 bytes) -> H(*) compression function -> hashcode H(M) 160 bits 

A  wants to send M to B
A sends M + H(M)a is sent to B 
B receives M computes H(M)b 
If  H(M)a  and  H(M)b is equal it is okey


%%%%%%%%%% MAC
MAC = C(K, M)+
must not be reversible
It is appended to message as a signature
It provides assurance that messafe is unaltered and comed from sender 

It can use any block cipher chainning mode  CBC  and use final block as a MAC 
Therefore the calculation of the MAC will only use always only the last block of the cbc  64 for DES an 128 AES

%%%%%%%%%% Hash function
signature, fingerprin, code 
hash value 


Digital signature is done with RSA

M 
H(M) -> h  (message digest MD)

Simple hash function 

        Bit1 Bit2 Bit3 Bit4
Block 1
Block 2
Block 3
Block 4
HC      C1    C2   C3   C4

If you add a key to the hash function process the 
Hash function plus secrecy key gives a MAC these are called HMACS


Case of the internet checksum

Has some properties of a hash function
It 


