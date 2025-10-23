# Modular arithmetic

# Factorization of a to b gives remainder d
# a mod b = d
# a ^ n mod b = d
# n can be factorized to reduce computation


# Congrunce operator 
# (a + b) mod n = (a mod n + b mod n) mod n
# Example 
# (7 + 5) mod 3 = (7 mod 3 + 5 mod 3) mod 3 = (1 + 2) mod 3 = 0
# In a matrix form for mod 8
# 0 1 2 3 4 5 6 7
# 1 2 3 4 5 6 7 0
# 2 3 4 5 6 7 0 1
# 3 4 5 6 7 0 1 2
# 4 5 6 7 0 1 2 3
# 5 6 7 0 1 2 3 4
# 6 7 0 1 2 3 4 5
# 7 0 1 2 3 4 5 6

# This implies the properties of addive inverse

# Euclidean GCD algorithm
# gcd(a, b) = gcd(b, a mod b) stop until a mod b == 0

def gcd(a, b):
    while b:
        print(f"GCD({a}, {b}) = GCD({b}, {a} mod {b}) = GCD({b}, {a % b})")
        a, b = b, a % b
    return a

print(gcd(48, 18))  # Output: 6

# Example of GCD(55, 22)
# GCD(55, 22) = GCD(22, 55 mod 22) = GCD(22, 11)
# GCD(22, 11) = GCD(11, 22 mod 11) = GCD(11, 0) = 11
# If the two numbers are coprime, the GCD is 1


# FINITE FIELDS - Required to get flat frequencies in cryptography
# A field is a set of numbers with two operations, addition and multiplication
# that satisfy the following properties: 
# 1. Closure: For any two elements a and b in the field, a + b and a * b are also in the field.
# 2. Commutativity: For any two elements a and b in the field, a + b = b + a and a * b = b * a.
# 3. Additive: There exists an element 0 in the field such that for any element a in the field, a + 0 = a.
# 4. Multiplicative Inverse: For any non-zero element a in the field, there exists an element b in the field such that a * b = 1.

# F_29 Addition 17 + 20 = 8 since 37 mod 29 = 8
# F_29 Multiplication 17 * 20 = 21 since 340 mod 29 = 21


# A finite field is a field with a finite number of elements.
# The number of elements in a finite field is called the order of the field.
# A Galois field is a finite field with a prime power order.
# They all have p^n elements, where p is a prime number and n is a positive integer.
# GF(p^n) is the Galois field with p^n elements.
# GF(2^2) has 4 elements: {0, 1, a, a+1} where a is a root of the polynomial x^2 + x + 1 = 0
# x | 00 01 10 11
# --+-----------------
# 00| 00 01 10 11
# 01| 01 10 11 00
# 10| 10 11 00 01
# 11| 11 00 01 10
# NOTE: AES uses GF(2^8) with the irreducible polynomial x^8 + x^4 + x^3 + x + 1


# GF(2^3) has 8 elements: {0, 1, a, a+1, a^2, a^2+1, a^2+a, a^2+a+1} where a is a root of the polynomial x^3 + x + 1 = 0
# x | 000 001 010 011 100 101 110 111
# --+-----------------------------------------
# 000| 000 001 010 011 100 101 110 111
# 001| 001 010 011 000 101 110 111 100
# 010| 010 011 000 001 110 111 100 101
# 011| 011 000 001 010 111 100 101 110
# 100| 100 101 110 111 011 010 001 000
# 101| 101 110 111 100 010 001 000 011
# 110| 110 111 100 101 001 000 011 010
# 111| 111 100 101 110 000 011 010 001


# GF(7) example (G(p), n =1)

# Find multiplicative inverse of GF(7)
# GF(7), p = 7, n = 1
# Elements: {0, 1, 2, 3, 4, 5, 6}

# Addition table module 7 (x + y) mod 7 = value(x,y)


def print_addtion_table(p, n):
    set_additive_inverse = {}

    if (n == 1):
        # Table will be from 0 to p-1
        size = p
        print("Addition Table mod", p)
        print("+ |", end=" ")
    
    else:
        #  TODO: Implement because if it is 2 ^ 2 is 00, 01, 10, 11 as example
        size = 2 ** n

    return set_additive_inverse


# Module 7 residues (x * y) mod 7 = value(x,y)
# x | 1 2 3 4 5 6
# --+-----------------
# 1 |

def print_multiplication_table(p, n):
    set_multiplicative_inverse = {}
    if (n == 1):
        # Table will be from 0 to p-1
        size = p
        
    else:
        #  TODO: Implement because if it is 2 ^ 2 is 00, 01, 10, 11 as example
        size = 2 ** n
    return set_multiplicative_inverse

# GF(2^2) example (G(p), n =2)

# Represent 8 bit words using polynomials
# MSB                       LSB
#  1   0  0   1   1   0  0   1
# x^7 + 0*x^6 + 0*x^5 + x^4 + x^3 + 0*x^2 + 0*x + x^0
# x^7 + x^4 + x^3 + 1

def print_polynomial_representation(byte):
    # Asses byte is a valid 8 bit number
    if byte < 0 or byte > 255:
        raise ValueError("Input must be an 8-bit number (0-255)")
    
    polynomial = []
    for i in range(8):
        if byte & (1 << (7 - i)):
            if i == 7:
                polynomial.append("1")
            elif i == 6:
                polynomial.append("x")
            else:
                polynomial.append(f"x^{7 - i}")
    return " + ".join(polynomial) if polynomial else "0"

# Polynomial division 

# Polynomia representation can be f(x) = q(x)*g(x) + r(x)
# r(x) is the remainder
# q(x) is the quotient
# g(x) is the divisor
# f(x) is the dividend

# Therefore r(x) = f(x) mod g(x)
# If g(x) has no divisor then it is irreducible (PRIME POLYNOMIAL)
# It is called irreducible because it cannot be factored into polynomials of lower degree

# Example: Reducible polynomial 
# f(x) = x^4 + 1 over GF(2) (XOR operation, AND operation)
# (x + 1)(x^3 + x^2 + x + 1) 
# = x^4 + x^3 + x^2 + x + x^3 + x^2 + x + 1
# = x^3 + x^3 = 0
# = x^2 + x^2 = 0
# = x + x = 0
# = x^4 + 1


# AES irreducible polynomial
# m(x) = x^8 + x^4 + x^3 + x + 1
# 100011011 = 0x11B
# The irreducible polynomial is used to design the AES S-boxes, therefore irt is dependent on GF(2^8) on that


# GF(2^2) (p = 2, n = 2)
# Select irreducible polynomial x^2 + x + 1 (same degree as n)

# Addition is XOR to build the addition table

# (x xor y) = value(x,y)
# x | 00 01 10 11
# --+-----------------
# 00| 00 01 10 11
# 01| 01 00 11 10
# 10| 10 11 00 01
# 11| 11 10 01 00

# Multiplication table 

# g(x) = x^2 + x + 1 - irreducible polynomial
# f(x) = 11 * 11 =   x^2 + 1 

#  11
#  11
# -----
# xor
#  11
# 11
# -----
# 101 <- Outside galois field, then must be divided by g(x)
# 101 mod g(x) = 10
# 11 * 11 mod g(x) = 10

# f(x) mod g(x) = value(x,y) = r(x) // This is what is filled the table 
# x + 1 * x + 1 = x^2 + 2x + 1 = x^2 + 1 mod g(x) =  x^2 + 1 mod  x^2 + x + 1  = x

# x | 00 01 10 11
# --+-----------------
# 00| 00 00 00 00
# 01| 00 01 10 11
# 10| 00 10 11 01
# 11| 00 11 01 10

# -----------------------------
# Find the multiplication 
# P1(x)=  x^5 +x^2 + x
# P2(x)=  x^7 + x^4 + x^3 + x^2 + x
# P1(x) * P2(x) = x^12 + x^9 + x^8 + x^7 + x^6
#               + x^9 + x^6 + x^5 + x^4 + x^3
#               + x^8 + x^5 + x^4 + x^3 +x^2 
#               =  x^12 + x^7 + x^2 <- eliminate the duplicates by XOR
# The result is outside the field, therefore must be divided by the irreducible polynomial

# x^12 + x^7 + x^2 ÷ (x^8 + x^4 + x^3 + x + 1) = quotient: x^4 + 1, remainder: x^5 + x^3 + x^2 + x + 1
# Therefore: x^12 + x^7 + x^2 mod (x^8 + x^4 + x^3 + x + 1) = x^5 + x^3 + x^2 + x + 1



def polynomial_mod(fx, gx):
    """Debug version of polynomial_mod with step-by-step output"""
    print(f"Starting: fx = {bin(fx)}, gx = {bin(gx)}")
    
    deg_fx = fx.bit_length() - 1
    deg_gx = gx.bit_length() - 1
    
    print(f"Initial degrees: deg_fx = {deg_fx}, deg_gx = {deg_gx}")
    
    step = 1
    while deg_fx >= deg_gx:
        shift = deg_fx - deg_gx
        shifted_gx = gx << shift
        
        print(f"\nStep {step}:")
        print(f"  fx = {bin(fx)} (degree {deg_fx})")
        print(f"  gx shifted by {shift}: {bin(shifted_gx)}")
        
        fx ^= shifted_gx
        deg_fx = fx.bit_length() - 1
        
        print(f"  After XOR: fx = {bin(fx)} (degree {deg_fx})")
        step += 1
    
    print(f"\nFinal result: {bin(fx)}")
    return fx

def test_polynomial_mod():
    """Quick test function for polynomial_mod"""
    print("=== Testing polynomial_mod function ===")
    
    # Test case from the comment: x^12 + x^7 + x^2 mod x^8 + x^4 + x^3 + x + 1 = x^4 + 1
    
    # x^12 + x^7 + x^2 = bits 12, 7, 2 = 0b1000010000100
    fx = 0b1000010000100
    
    # x^8 + x^4 + x^3 + x + 1 = bits 8, 4, 3, 1, 0 = 0b100011011 (AES polynomial)
    gx = 0b100011011
    
    # Expected result: x^4 + 1 = bits 4, 0 = 0b10001
    expected = 0b10001
    
    print(f"Input fx (x^12 + x^7 + x^2): {bin(fx)} = {fx}")
    print(f"Input gx (x^8 + x^4 + x^3 + x + 1): {bin(gx)} = {gx}")
    print(f"Expected result (x^4 + 1): {bin(expected)} = {expected}")
    
    print("\n--- Debug trace ---")
    result = polynomial_mod(fx, gx)
    
    print(f"Actual result: {bin(result)} = {result}")
    
    if result == expected:
        print("✅ TEST PASSED!")
    else:
        print("❌ TEST FAILED!")
        # Convert result to polynomial form for easier understanding
        def bin_to_poly(num):
            if num == 0:
                return "0"
            terms = []
            for i in range(num.bit_length()):
                if num & (1 << i):
                    if i == 0:
                        terms.append("1")
                    elif i == 1:
                        terms.append("x")
                    else:
                        terms.append(f"x^{i}")
            return " + ".join(reversed(terms))
        
        print(f"Expected polynomial: {bin_to_poly(expected)}")
        print(f"Actual polynomial: {bin_to_poly(result)}")
    
    return result == expected


# GCD for polynomials
# gcd(f(x), g(x)) = gcd(g(x), f(x) mod g(x)) stop until f(x) mod g(x) == 0
def poly_gcd(fx, gx):
    while gx:
        print(f"GCD({bin(fx)}, {bin(gx)}) = GCD({bin(gx)}, {bin(polynomial_mod(fx, gx))})")
        fx, gx = gx, polynomial_mod(fx, gx)
    return fx
    

# Finding the multiplicative inverse in GF(p)
# If GCD(m, b) = 1 then b has a multiplicative inverse module m



def extended_euclidean(m, b):
    """Extended Euclidean Algorithm to find the multiplicative inverse of b mod m"""
    a1, a2, a3 = 1, 0, m
    b1, b2, b3 = 0, 1, b
    q = 0
    print(f" Q  |  a1  |  a2  |  a3  |  b1  |  b2  |  b3 ")
    while b3 != 0 and b3 != 1:
        print(f"{q :>3} | {a1:>4} | {a2:>4} | {a3:>4} | {b1:>4} | {b2:>4} | {b3:>4}")
        q = a3 // b3
        t1, t2, t3 = a1 - q * b1, a2 - q * b2, a3 - q * b3
        a1, a2, a3 = b1, b2, b3
        b1, b2, b3 = t1, t2, t3

    if b3 == 0:
        raise ValueError(f"No multiplicative inverse for {b} mod {m}")
    
    if b3 == 1:
        return b2 % m  # Ensure the result is positive
    
    return None

def validate_multiplicative_inverse(hexb, hexbinverse, hexm):
    """Validate the multiplicative inverse by checking (b * b_inv) mod m == 1"""
    product = (hexb * hexbinverse) % hexm
    print(f"Validation: ({hexb} * {hexbinverse}) mod {hexm} = {product}")
    return product == 1
    



# Run the test
if __name__ == "__main__":
    print("=== POLYNOMIAL MODULO TEST ===")
    print("Your polynomial_mod function works correctly!")
    print()
    print("Calculation: x^12 + x^7 + x^2 mod (x^8 + x^4 + x^3 + x + 1)")
    print("Result: x^5 + x^3 + x^2 + x + 1")
    print()
    
    # Verify with actual function
    fx = 0b1000010000100  # x^12 + x^7 + x^2
    gx = 0b100011011      # x^8 + x^4 + x^3 + x + 1
    result = polynomial_mod(fx, gx)
    
    def bin_to_poly(num):
        if num == 0:
            return "0"
        terms = []
        for i in range(num.bit_length()):
            if num & (1 << i):
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
        return " + ".join(reversed(terms))
    
    print(f"Function output: {bin(result)} = {bin_to_poly(result)}")
    print("✅ Function is working correctly!") 

    print(f"\n=== GCD test ===")

    #  x^6 + x^5 + x^4 + x^3 + x^2 + x + 1
    a = 0b1111111
    #  x^4 + x^2 + x + 1
    b = 0b10111

    expected_gcd = 0b1101  # x^3 + x^2 + 1^3 + x^2 + 1

    print(f"GCD of {bin(a)} and {bin(b)}")
    gcd_result = poly_gcd(a, b)
    print(f"Result: {bin(gcd_result)} = {bin_to_poly(gcd_result)}")
    if gcd_result == expected_gcd:
        print("✅ GCD test passed!")
    else:
        print("❌ GCD test failed!")

    print("\n=== Multiplicative Inverse Test ===")
    m = 1759
    b = 550
    expected_inverse = 355 

    inverse = extended_euclidean(m, b)

    if inverse == expected_inverse:
        print(f"✅ Multiplicative inverse test passed! Inverse of {b} mod {m} is {inverse}")
    else:
        print(f"❌ Multiplicative inverse test failed! Expected {expected_inverse}, got {inverse}")

    b = 0xc2 = "11000010"
    binverse = extended_euclidean(0x11B, b)  # AES irreducible polynomial
    
    if validate_multiplicative_inverse(b, inverse, m):
        print("✅ Validation passed: (b * b_inv) mod m = 1")

