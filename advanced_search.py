#!/usr/bin/env python3
"""
Advanced Key Search for NESRD3Q Puzzle
Based on all hints including the dots pattern and "hexdumping all the stuff"
"""

import hashlib
import struct

# Import validation function
exec(open('btc_validate_pure.py').read().split('# Target address')[0])

TARGET = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# Load data
with open('dbbi_block.txt', 'r') as f:
    dbbi_block = f.read().strip()

with open('faed_block.txt', 'r') as f:
    faed_block = f.read().strip()

# OTP result
otp_key = "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDEDFUNDSTOLIVE"

def otp_decrypt(ciphertext, key):
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

otp_result = otp_decrypt(dbbi_block, otp_key)
otp_64 = otp_result[27:]

# Dots pattern
dots_raw = """. . . . . . 0 1 . . . . . . . . . . . 1 . . . . . 0 0 . . . . . . . . . 0 0 . . . . . . . . . 0 1 . . . . . . . . . . 1 . . . . . . 0 0 . . . . . . . . . 0 0 . . 0 0 . . . . . . 1 . . . . . . 0 0 . . 1 . . . . 0 . . . . . 0 . . . . 0 . 0 0 . . . . . . . . 1 . 0 . . . . . . . . . . . . 1 . . . . . 0 0 . . . . . . 0 1 . . . . 0 0 . . . . . . 0 0 1 . . . . . 0 0 . . . . . 0 . . . . . . 0 0 ."""
dots = dots_raw.split()

pos_0 = [i for i, d in enumerate(dots) if d == '0']
pos_1 = [i for i, d in enumerate(dots) if d == '1']

def check_key(key, name):
    """Check if a key matches the target."""
    if len(key) != 64:
        return False
    if not all(c in '0123456789abcdef' for c in key.lower()):
        return False
    
    addresses = private_key_to_address(key.lower())
    for pk_type, addr in addresses:
        if addr == TARGET:
            print(f"\n{'='*70}")
            print(f"FOUND MATCH: {name}")
            print(f"Key: {key}")
            print(f"Type: {pk_type}")
            print(f"Address: {addr}")
            print(f"{'='*70}")
            return True
    return False

print("=" * 70)
print("ADVANCED KEY SEARCH")
print("=" * 70)

# ============================================================
# APPROACH: "Hexdumping all the stuff"
# ============================================================
print("\n--- Hexdump approach ---")

# The hint says "All these dots are about hexdumping all the stuff"
# Hexdump typically shows hex values of bytes

# Combined block as bytes (a=0, b=1, ..., i=8)
combined = dbbi_block + faed_block

def block_to_bytes(block):
    """Convert a-i block to bytes (a=0, b=1, ..., i=8)"""
    return bytes([ord(c) - ord('a') for c in block])

combined_bytes = block_to_bytes(combined)
print(f"Combined as bytes (first 20): {combined_bytes[:20].hex()}")

# Hexdump of combined block
hexdump = combined_bytes.hex()
print(f"Hexdump length: {len(hexdump)}")
print(f"First 64 chars of hexdump: {hexdump[:64]}")

# Try this as a key
check_key(hexdump[:64], "Hexdump first 64")

# ============================================================
# APPROACH: Use dots pattern as mask on hexdump
# ============================================================
print("\n--- Dots pattern on hexdump ---")

# The dots pattern has 196 elements
# If we hexdump the combined block, we get 661*2 = 1322 hex chars
# But the dots pattern is 14x14 = 196

# Maybe the dots pattern indicates which hex pairs to extract
# 32 zeros + 10 ones = 42 positions
# 42 hex pairs = 84 hex chars (too many for 64)

# Or maybe it's which single hex chars to extract
non_dot_positions = sorted(pos_0 + pos_1)
print(f"Non-dot positions: {non_dot_positions}")

# Extract hex chars at these positions
if len(hexdump) > max(non_dot_positions):
    extracted = ''.join(hexdump[i] for i in non_dot_positions)
    print(f"Extracted from hexdump: {extracted}")
    
    # Pad to 64 if needed
    if len(extracted) < 64:
        padded = extracted.ljust(64, '0')
        check_key(padded, "Dots-extracted from hexdump (padded)")

# ============================================================
# APPROACH: Interpret a-i as hex digits directly
# ============================================================
print("\n--- Direct hex interpretation ---")

# What if a-f are hex, and g-i need special handling?
# g=6+1=7? or g=0, h=1, i=2?

def block_to_hex_v1(block):
    """a-f as hex, g=0, h=1, i=2"""
    result = []
    for c in block:
        if c in 'abcdef':
            result.append(c)
        elif c == 'g':
            result.append('0')
        elif c == 'h':
            result.append('1')
        elif c == 'i':
            result.append('2')
    return ''.join(result)

def block_to_hex_v2(block):
    """a=a, b=b, c=c, d=d, e=e, f=f, g=7, h=8, i=9"""
    result = []
    for c in block:
        if c in 'abcdef':
            result.append(c)
        elif c == 'g':
            result.append('7')
        elif c == 'h':
            result.append('8')
        elif c == 'i':
            result.append('9')
    return ''.join(result)

hex_v1 = block_to_hex_v1(combined)
hex_v2 = block_to_hex_v2(combined)

print(f"V1 (g=0,h=1,i=2) first 64: {hex_v1[:64]}")
print(f"V2 (g=7,h=8,i=9) first 64: {hex_v2[:64]}")

check_key(hex_v1[:64], "Block hex V1")
check_key(hex_v2[:64], "Block hex V2")

# ============================================================
# APPROACH: Use the 14x14 grid positions
# ============================================================
print("\n--- 14x14 grid approach ---")

# The puzzle image is 14x14
# The dots pattern is 14x14
# Maybe we need to read the combined block as a 14x14 grid

# 14x14 = 196, but combined is 661 chars
# Maybe only the first 196 chars matter?

first_196 = combined[:196]
print(f"First 196 chars: {first_196[:50]}...")

# Extract at dots positions
extracted_at_dots = ''.join(first_196[i] for i in non_dot_positions if i < len(first_196))
print(f"Extracted at non-dot positions: {extracted_at_dots}")

# Convert to hex
extracted_hex = ''.join(format(ord(c) - ord('a'), 'x') for c in extracted_at_dots)
print(f"As hex: {extracted_hex}")

if len(extracted_hex) >= 64:
    check_key(extracted_hex[:64], "First 196 dots-extracted")

# ============================================================
# APPROACH: Yellow and blue primes hint
# ============================================================
print("\n--- Yellow/Blue primes approach ---")

# 9 yellow squares, 15 blue squares
# Primes up to 9: 2, 3, 5, 7 (sum = 17)
# Primes up to 15: 2, 3, 5, 7, 11, 13 (sum = 41)

primes_9 = [2, 3, 5, 7]
primes_15 = [2, 3, 5, 7, 11, 13]

# Extract chars at prime positions
extracted_primes = ''.join(combined[p] for p in primes_9 + primes_15 if p < len(combined))
print(f"Chars at prime positions: {extracted_primes}")

# ============================================================
# APPROACH: The OTP 64 chars might need transformation
# ============================================================
print("\n--- OTP transformation ---")

# The OTP result is: XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCBDDMOBMLMQW
# This is 64 uppercase letters

# What if we need to convert using the Polybius square from Bifid?
# Or what if we need to use the dots pattern to select?

# Use dots pattern to select from OTP 64
otp_at_dots = ''.join(otp_64[i] for i in non_dot_positions if i < len(otp_64))
print(f"OTP at non-dot positions: {otp_at_dots}")

# Convert to hex
otp_dots_hex = ''.join(format((ord(c) - ord('A')) % 16, 'x') for c in otp_at_dots)
print(f"As hex: {otp_dots_hex}")

# ============================================================
# APPROACH: Combine DBBI and FAED differently
# ============================================================
print("\n--- Alternative combinations ---")

# What if the 91 char DBBI and 570 char FAED need to be combined differently?
# 91 + 570 = 661
# 661 / 10 = 66.1 (close to 64)
# Maybe every 10th character?

every_10th = combined[::10]
print(f"Every 10th char: {every_10th}")

# Convert to hex
every_10th_hex = ''.join(format(ord(c) - ord('a'), 'x') for c in every_10th)
print(f"As hex: {every_10th_hex}")

if len(every_10th_hex) >= 64:
    check_key(every_10th_hex[:64], "Every 10th char")

# ============================================================
# APPROACH: The Bifid output should start with "btcseed"
# ============================================================
print("\n--- Searching for btcseed pattern ---")

# If the Bifid decryption should produce "btcseed" + 563 chars
# Let's try to find what input would produce that

# "btcseed" in the a-i alphabet would be: b, t->?, c, s->?, e, e, d
# But t and s are not in a-i alphabet!

# Maybe "btcseed" is encoded differently?
# Or maybe the output is in a different format?

# Let's check if any substring of faed contains the pattern
# that would decode to something starting with "btc"

print("\n" + "=" * 70)
print("Search complete.")
print("=" * 70)
