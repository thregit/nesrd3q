#!/usr/bin/env python3
"""
Comprehensive cipher solver for NESRD3Q puzzle
Trying multiple cipher approaches on the dbbi and faed blocks
"""

# Load the blocks
with open('dbbi_block.txt', 'r') as f:
    dbbi_block = f.read().strip()

with open('faed_block.txt', 'r') as f:
    faed_block = f.read().strip()

print("=" * 70)
print("CIPHER ANALYSIS")
print("=" * 70)
print(f"DBBI block: {len(dbbi_block)} chars")
print(f"FAED block: {len(faed_block)} chars")

# The blocks use letters a-i (9 letters)
# This suggests a 3x3 Polybius square or base-9 encoding

# ============================================================
# APPROACH 1: Simple letter-to-number mapping
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 1: Letter-to-number mapping (a=0, b=1, ..., i=8)")
print("=" * 70)

def letters_to_numbers(text, mapping='a=0'):
    """Convert letters to numbers."""
    if mapping == 'a=0':
        return ''.join(str(ord(c) - ord('a')) for c in text)
    elif mapping == 'a=1':
        return ''.join(str(ord(c) - ord('a') + 1) for c in text)
    return text

dbbi_nums = letters_to_numbers(dbbi_block, 'a=0')
faed_nums = letters_to_numbers(faed_block, 'a=0')

print(f"DBBI as numbers (a=0): {dbbi_nums[:50]}...")
print(f"FAED as numbers (a=0): {faed_nums[:50]}...")

# Try converting to hex
def nums_to_hex(nums):
    """Convert digit string to hex."""
    # Each digit is 0-8, so we can try treating pairs as base-9
    result = []
    for i in range(0, len(nums) - 1, 2):
        val = int(nums[i]) * 9 + int(nums[i+1])
        result.append(format(val, 'x'))
    return ''.join(result)

hex_dbbi = nums_to_hex(dbbi_nums)
hex_faed = nums_to_hex(faed_nums)
print(f"\nAs hex (base-9 pairs):")
print(f"DBBI: {hex_dbbi[:50]}...")
print(f"FAED: {hex_faed[:50]}...")

# ============================================================
# APPROACH 2: Bifid cipher with different period lengths
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 2: Bifid cipher with period")
print("=" * 70)

def create_square(keyword):
    alphabet = 'abcdefghi'
    square = []
    seen = set()
    for c in keyword.lower():
        if c in alphabet and c not in seen:
            square.append(c)
            seen.add(c)
    for c in alphabet:
        if c not in seen:
            square.append(c)
            seen.add(c)
    return ''.join(square)

def bifid_decrypt_period(ciphertext, square, period=5, size=3):
    """Bifid decrypt with a period (block size)."""
    result = []
    
    for start in range(0, len(ciphertext), period):
        block = ciphertext[start:start+period]
        
        # Get coordinates
        rows = []
        cols = []
        for c in block:
            if c in square:
                idx = square.index(c)
                rows.append(idx // size)
                cols.append(idx % size)
        
        # Combine and pair
        combined = rows + cols
        n = len(rows)
        
        for i in range(n):
            r = combined[i]
            c = combined[i + n] if i + n < len(combined) else 0
            result.append(square[r * size + c])
    
    return ''.join(result)

square = create_square("dbifhceg")
print(f"Square: {square}")

for period in [5, 7, 10, 14, 19, 91, 570]:
    if period <= len(faed_block):
        res = bifid_decrypt_period(faed_block, square, period)
        if 'btc' in res[:20].lower() or 'seed' in res[:20].lower():
            print(f"Period {period}: {res[:30]}... (MATCH!)")
        else:
            print(f"Period {period}: {res[:30]}...")

# ============================================================
# APPROACH 3: OTP cipher on DBBI block
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 3: OTP cipher on DBBI block")
print("=" * 70)

otp_key = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDEDFUNDSTOLIVE"
print(f"OTP Key length: {len(otp_key)}")
print(f"DBBI length: {len(dbbi_block)}")

# Convert dbbi to uppercase for OTP
dbbi_upper = dbbi_block.upper()

# OTP decryption: (ciphertext - key) mod 26
def otp_decrypt(ciphertext, key):
    """OTP decryption using subtraction mod 26."""
    result = []
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            k = key[i % len(key)]
            # (c - k) mod 26
            c_val = ord(c.upper()) - ord('A')
            k_val = ord(k.upper()) - ord('A')
            p_val = (c_val - k_val) % 26
            result.append(chr(p_val + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

def otp_decrypt_add(ciphertext, key):
    """OTP decryption using addition mod 26."""
    result = []
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            k = key[i % len(key)]
            c_val = ord(c.upper()) - ord('A')
            k_val = ord(k.upper()) - ord('A')
            p_val = (c_val + k_val) % 26
            result.append(chr(p_val + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

# But wait - dbbi uses letters a-i (only 9 letters)
# We need to map these to the full alphabet first

# Let's try treating a-i as positions 0-8 in the alphabet
def expand_to_alphabet(text):
    """Expand a-i to full alphabet positions."""
    return text  # a-i are already valid alphabet letters

# Try OTP with the key
otp_result_sub = otp_decrypt(dbbi_block, otp_key)
otp_result_add = otp_decrypt_add(dbbi_block, otp_key)

print(f"\nOTP decrypt (subtraction): {otp_result_sub}")
print(f"OTP decrypt (addition): {otp_result_add}")

# Check for "YOUWON" at position 21
print(f"\nPosition 21-27 (sub): {otp_result_sub[21:27]}")
print(f"Position 21-27 (add): {otp_result_add[21:27]}")

# The prompt says the dbbi block should decrypt to reveal "YOUWON" at position 21
# Let's check if the key length matches
print(f"\nKey length: {len(otp_key)}")
print(f"DBBI length: {len(dbbi_block)}")

# Maybe we need to use a different approach
# The prompt mentions: (plaintext - key) mod 26
# So ciphertext = (plaintext - key) mod 26
# Therefore plaintext = (ciphertext + key) mod 26

print("\n--- Trying different OTP interpretations ---")

# Try with key truncated to match dbbi length
key_truncated = otp_key[:len(dbbi_block)]
print(f"Truncated key: {key_truncated}")

result1 = otp_decrypt_add(dbbi_block, key_truncated)
print(f"Add mod 26: {result1}")
print(f"Position 21-27: {result1[21:27]}")

# ============================================================
# APPROACH 4: Direct hex interpretation
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 4: Direct hex interpretation")
print("=" * 70)

# The letters a-f are valid hex, g-i are not
# Count hex-valid characters
hex_chars_dbbi = sum(1 for c in dbbi_block if c in 'abcdef')
hex_chars_faed = sum(1 for c in faed_block if c in 'abcdef')

print(f"Hex-valid chars in DBBI: {hex_chars_dbbi}/{len(dbbi_block)}")
print(f"Hex-valid chars in FAED: {hex_chars_faed}/{len(faed_block)}")

# Extract only hex-valid characters
hex_only_dbbi = ''.join(c for c in dbbi_block if c in 'abcdef')
hex_only_faed = ''.join(c for c in faed_block if c in 'abcdef')

print(f"\nHex-only DBBI ({len(hex_only_dbbi)} chars): {hex_only_dbbi[:50]}...")
print(f"Hex-only FAED ({len(hex_only_faed)} chars): {hex_only_faed[:50]}...")

# ============================================================
# APPROACH 5: Check the combined block structure
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 5: Combined block analysis")
print("=" * 70)

combined = dbbi_block + faed_block
print(f"Combined length: {len(combined)}")
print(f"First 50: {combined[:50]}")
print(f"Last 50: {combined[-50:]}")

# Look for patterns
from collections import Counter
char_freq = Counter(combined)
print(f"\nCharacter frequency: {dict(sorted(char_freq.items()))}")

# Check if it could be base64-like
import string
base64_chars = set(string.ascii_letters + string.digits + '+/=')
valid_b64 = all(c in base64_chars for c in combined)
print(f"Valid base64: {valid_b64}")
