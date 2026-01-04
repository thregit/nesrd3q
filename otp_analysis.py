#!/usr/bin/env python3
"""
OTP Analysis for NESRD3Q Puzzle
Extract the 64-character string after "YOUWON"
"""

# Load the dbbi block
with open('dbbi_block.txt', 'r') as f:
    dbbi_block = f.read().strip()

# OTP key from the puzzle
otp_key = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDEDFUNDSTOLIVE"

def otp_decrypt(ciphertext, key):
    """OTP decryption: (ciphertext - key) mod 26."""
    result = []
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            k = key[i % len(key)]
            c_val = ord(c.upper()) - ord('A')
            k_val = ord(k.upper()) - ord('A')
            p_val = (c_val - k_val) % 26
            result.append(chr(p_val + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

print("=" * 70)
print("OTP DECRYPTION ANALYSIS")
print("=" * 70)

# Decrypt
otp_result = otp_decrypt(dbbi_block, otp_key)

print(f"\nDBBI block ({len(dbbi_block)} chars):")
print(dbbi_block)

print(f"\nOTP Key ({len(otp_key)} chars):")
print(otp_key)

print(f"\nDecrypted result ({len(otp_result)} chars):")
print(otp_result)

# Find YOUWON
youwon_pos = otp_result.find("YOUWON")
print(f"\n'YOUWON' found at position: {youwon_pos}")

# Extract the 64 characters after YOUWON
if youwon_pos >= 0:
    after_youwon = otp_result[youwon_pos + 6:]
    print(f"\nCharacters after 'YOUWON' ({len(after_youwon)} chars):")
    print(after_youwon)
    
    # The first 64 characters after YOUWON
    key_material = after_youwon[:64]
    print(f"\nFirst 64 chars after 'YOUWON':")
    print(key_material)
    print(f"Length: {len(key_material)}")
    
    # Also get the prefix before YOUWON
    before_youwon = otp_result[:youwon_pos]
    print(f"\nCharacters before 'YOUWON' ({len(before_youwon)} chars):")
    print(before_youwon)

# Analyze the structure
print("\n" + "=" * 70)
print("STRUCTURE ANALYSIS")
print("=" * 70)

# The prompt says: vozijbdtiqbrgveomznbc[YOUWON][64 characters]
# Let's verify this structure
print(f"\nExpected structure: vozijbdtiqbrgveomznbc[YOUWON][64 chars]")
print(f"Position 0-21: {otp_result[:21]}")
print(f"Position 21-27: {otp_result[21:27]}")
print(f"Position 27-91: {otp_result[27:]}")
print(f"Length of position 27-91: {len(otp_result[27:])}")

# The 64 characters after YOUWON
final_64 = otp_result[27:]
print(f"\n64-char key material from OTP:")
print(final_64)
print(f"Length: {len(final_64)}")

# Save the key material
with open('otp_key_material.txt', 'w') as f:
    f.write(final_64)

# Check if it's valid hex
hex_chars = set('0123456789abcdefABCDEF')
is_hex = all(c in hex_chars for c in final_64)
print(f"\nIs valid hex: {is_hex}")

# Convert to lowercase for potential hex use
final_64_lower = final_64.lower()
print(f"Lowercase: {final_64_lower}")

# Check which characters are hex-valid
hex_valid = ''.join(c if c.lower() in 'abcdef' else '_' for c in final_64)
print(f"Hex-valid positions: {hex_valid}")

# Count hex-valid characters
hex_count = sum(1 for c in final_64 if c.lower() in 'abcdef')
print(f"Hex-valid character count: {hex_count}/64")
