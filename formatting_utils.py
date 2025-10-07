"""
Formatting and Display Utilities for Cryptographic Algorithms

This module provides utility functions for formatting and displaying binary data,
hexadecimal values, and creating structured output for cryptographic algorithms
like DES, AES, etc.

Author: Cryptographic Implementation Helper
Date: October 2025
"""

def format_binary_grouped(binary_list, group_size=4):
    """
    Format binary list in groups of bits with spaces between groups.
    
    Args:
        binary_list (list): List of binary digits (0s and 1s)
        group_size (int): Number of bits per group (default: 4 for nibbles)
    
    Returns:
        str: Formatted binary string with spaces between groups
        
    Example:
        >>> format_binary_grouped([1,0,1,1,0,0,1,1], 4)
        '1011 0011'
    """
    if not binary_list:
        return ""
    
    # Convert to string and group by group_size
    binary_str = ''.join(str(bit) for bit in binary_list)
    grouped = []
    for i in range(0, len(binary_str), group_size):
        grouped.append(binary_str[i:i+group_size])
    
    return ' '.join(grouped)


def binary_to_hex(binary_list):
    """
    Convert binary list to hexadecimal string.
    
    Args:
        binary_list (list): List of binary digits (0s and 1s)
    
    Returns:
        str: Hexadecimal representation (uppercase)
        
    Example:
        >>> binary_to_hex([1,0,1,1,0,0,1,1])
        'B3'
    """
    if not binary_list:
        return ""
    
    # Pad to multiple of 4 if needed
    padded = binary_list[:]
    while len(padded) % 4 != 0:
        padded.insert(0, 0)
    
    # Convert to hex
    binary_str = ''.join(str(bit) for bit in padded)
    hex_value = hex(int(binary_str, 2))[2:].upper().zfill(len(padded)//4)
    return hex_value


def print_section_header(title, char='='):
    """
    Print a formatted section header with decorative characters.
    
    Args:
        title (str): Title text to display
        char (str): Character to use for decoration (default: '=')
        
    Example:
        >>> print_section_header("DES ENCRYPTION")
        ========================= DES ENCRYPTION =========================
    """
    width = 70
    padding = (width - len(title) - 2) // 2
    print(f"\n{char * padding} {title} {char * padding}")


def print_binary_data(label, binary_list, show_hex=True):
    """
    Print binary data in formatted groups with optional hex representation.
    
    Args:
        label (str): Descriptive label for the data
        binary_list (list): List of binary digits
        show_hex (bool): Whether to show hexadecimal equivalent (default: True)
        
    Example:
        >>> print_binary_data("Plaintext", [1,0,1,1,0,0,1,1])
        Plaintext            ( 8 bits): 1011 0011
                              HEX: B3
    """
    formatted_binary = format_binary_grouped(binary_list)
    
    if show_hex and binary_list:
        hex_value = binary_to_hex(binary_list)
        print(f"{label:20} ({len(binary_list):2d} bits): {formatted_binary}")
        print(f"{' ' * 20}     HEX: {hex_value}")
    else:
        print(f"{label:20} ({len(binary_list):2d} bits): {formatted_binary}")


def print_step_header(step_num, title):
    """
    Print a formatted step header for algorithm phases.
    
    Args:
        step_num (int): Step number
        title (str): Step description
        
    Example:
        >>> print_step_header(1, "Initial Permutation")
        --- Step 1: Initial Permutation ---
    """
    print(f"\n--- Step {step_num}: {title} ---")


def print_algorithm_summary(algorithm_name, input_size, output_size, rounds=None):
    """
    Print a summary of algorithm parameters.
    
    Args:
        algorithm_name (str): Name of the cryptographic algorithm
        input_size (int): Size of input in bits
        output_size (int): Size of output in bits
        rounds (int, optional): Number of rounds (if applicable)
    """
    print_section_header(f"{algorithm_name} ALGORITHM SUMMARY")
    print(f"Input size:  {input_size} bits")
    print(f"Output size: {output_size} bits")
    if rounds:
        print(f"Rounds:      {rounds}")


# Additional utility functions for cryptographic display

def format_key_schedule(subkeys, algorithm="DES"):
    """
    Display a formatted key schedule for cryptographic algorithms.
    
    Args:
        subkeys (list): List of subkey binary arrays
        algorithm (str): Algorithm name for display
    """
    print_section_header(f"{algorithm} KEY SCHEDULE")
    for i, subkey in enumerate(subkeys[:3]):  # Show first 3 subkeys
        print_binary_data(f"K{i+1}", subkey)
    
    if len(subkeys) > 3:
        print(f"... and {len(subkeys) - 3} more subkeys")
        print_binary_data(f"K{len(subkeys)}", subkeys[-1])  # Show last subkey


def hex_string_to_binary(hex_str):
    """
    Convert hexadecimal string to binary list.
    
    Args:
        hex_str (str): Hexadecimal string (with or without '0x' prefix)
    
    Returns:
        list: List of binary digits
        
    Example:
        >>> hex_string_to_binary("B3")
        [1, 0, 1, 1, 0, 0, 1, 1]
    """
    # Remove '0x' prefix if present
    if hex_str.startswith(('0x', '0X')):
        hex_str = hex_str[2:]
    
    # Convert to integer then to binary
    value = int(hex_str, 16)
    bit_length = len(hex_str) * 4
    
    return [(value >> i) & 1 for i in reversed(range(bit_length))]


if __name__ == "__main__":
    # Test the utility functions
    print("Testing Formatting Utilities")
    print("=" * 40)
    
    # Test binary data
    test_binary = [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1]
    
    print("Test binary data:")
    print_binary_data("Test Data", test_binary)
    
    print("\nFormatted binary (grouped by 4):")
    print(format_binary_grouped(test_binary, 4))
    
    print("\nFormatted binary (grouped by 8):")
    print(format_binary_grouped(test_binary, 8))
    
    print("\nHex conversion:")
    print(f"Binary: {test_binary}")
    print(f"Hex: {binary_to_hex(test_binary)}")
    
    print_section_header("Test Complete")
