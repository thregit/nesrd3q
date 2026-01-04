#!/usr/bin/env python3
"""
Final comprehensive search for NESRD3Q Bitcoin puzzle
Based on all hints and patterns discovered
"""

import hashlib
import itertools

# Import validation
exec(open('btc_validate_pure.py').read().split('# Target address')[0])

TARGET = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# Load data
with open('dbbi_block.txt', 'r') as f:
    dbbi_block = f.read().strip()

with open('faed_block.txt', 'r') as f:
    faed_block = f.read().strip()

combined = dbbi_block + faed_block

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

def check_key(key, name, verbose=False):
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
            print(f"{'='*70}")
            return True
        elif verbose:
            print(f"  {name}: {addr[:20]}...")
    return False

print("=" * 70)
print("FINAL COMPREHENSIVE SEARCH")
print("=" * 70)
print(f"Target: {TARGET}")

# ============================================================
# The OTP 64 chars converted to hex using mod 16 gives us a candidate
# Let's verify this is being done correctly
# ============================================================

print("\n--- Verifying OTP to hex conversion ---")
print(f"OTP 64: {otp_64}")

# Standard mod 16 conversion
hex_key = ''.join(format((ord(c) - ord('A')) % 16, 'x') for c in otp_64)
print(f"Hex (mod 16): {hex_key}")

# Check this key
result = private_key_to_address(hex_key)
print(f"Generated addresses:")
for pk_type, addr in result:
    print(f"  {pk_type}: {addr}")

# ============================================================
# Try XOR with different keys
# ============================================================

print("\n--- XOR combinations ---")

# XOR the OTP hex with various patterns
def xor_hex(h1, h2):
    """XOR two hex strings."""
    if len(h1) != len(h2):
        h2 = (h2 * (len(h1) // len(h2) + 1))[:len(h1)]
    return ''.join(format(int(a, 16) ^ int(b, 16), 'x') for a, b in zip(h1, h2))

# XOR with the FAED hex
faed_hex = ''.join(c for c in faed_block if c in 'abcdef')[:64]
if len(faed_hex) == 64:
    xored = xor_hex(hex_key, faed_hex)
    check_key(xored, "OTP XOR FAED_hex")

# XOR with the dots binary pattern
dots_binary = ''.join('1' if d == '1' else '0' for d in dots)
dots_hex = hex(int(dots_binary.ljust(256, '0')[:256], 2))[2:].zfill(64)
xored_dots = xor_hex(hex_key, dots_hex)
check_key(xored_dots, "OTP XOR dots_binary")

# ============================================================
# Try different orderings and combinations
# ============================================================

print("\n--- Different orderings ---")

# Reverse the hex key
check_key(hex_key[::-1], "OTP hex reversed")

# Swap nibbles (reverse pairs)
swapped = ''.join(hex_key[i+1] + hex_key[i] for i in range(0, 64, 2))
check_key(swapped, "OTP hex nibble-swapped")

# Reverse byte order
byte_reversed = ''.join(hex_key[i:i+2] for i in range(62, -2, -2))
check_key(byte_reversed, "OTP hex byte-reversed")

# ============================================================
# Try using the dots pattern as indices
# ============================================================

print("\n--- Dots pattern as indices ---")

# The dots pattern has 42 non-dot positions
# What if these are indices into the OTP 64?
non_dot = sorted(pos_0 + pos_1)
print(f"Non-dot positions: {non_dot}")

# Extract from OTP at these positions (mod 64)
extracted = ''.join(otp_64[i % 64] for i in non_dot)
print(f"Extracted from OTP: {extracted}")

# Convert to hex
extracted_hex = ''.join(format((ord(c) - ord('A')) % 16, 'x') for c in extracted)
print(f"As hex: {extracted_hex}")

# Pad to 64
if len(extracted_hex) < 64:
    padded = extracted_hex + hex_key[len(extracted_hex):]
    check_key(padded, "Dots-extracted + OTP remainder")

# ============================================================
# Try the combined block as a direct key source
# ============================================================

print("\n--- Combined block analysis ---")

# The combined block is 661 chars of a-i
# Convert to hex using different mappings

# Mapping 1: a=a, b=b, c=c, d=d, e=e, f=f, g=0, h=1, i=2
def ai_to_hex_v1(text):
    mapping = {'a':'a', 'b':'b', 'c':'c', 'd':'d', 'e':'e', 'f':'f', 'g':'0', 'h':'1', 'i':'2'}
    return ''.join(mapping.get(c, '0') for c in text)

# Mapping 2: a=0, b=1, ..., i=8 (single digit)
def ai_to_hex_v2(text):
    return ''.join(str(ord(c) - ord('a')) for c in text)

hex_v1 = ai_to_hex_v1(combined)[:64]
hex_v2 = ai_to_hex_v2(combined)[:64]

print(f"V1 (a-f=hex, ghi=012): {hex_v1}")
print(f"V2 (a-i = 0-8): {hex_v2}")

check_key(hex_v1, "Combined V1")

# V2 has digits 0-8, need to convert to valid hex
# Take pairs and convert
pairs_hex = ''
for i in range(0, min(128, len(hex_v2)), 2):
    val = int(hex_v2[i]) * 9 + int(hex_v2[i+1]) if i+1 < len(hex_v2) else int(hex_v2[i])
    pairs_hex += format(val % 256, '02x')
check_key(pairs_hex[:64], "Combined V2 pairs")

# ============================================================
# Try SHA256 of various combinations
# ============================================================

print("\n--- SHA256 combinations ---")

hashes_to_try = [
    hex_key,
    otp_64.lower(),
    otp_result.lower(),
    dbbi_block + otp_key[:91],
    faed_block[:64],
    combined[:64],
    "YOUWON" + otp_64,
    otp_64 + "YOUWON",
]

for s in hashes_to_try:
    h = hashlib.sha256(s.encode()).hexdigest()
    check_key(h, f"SHA256({s[:20]}...)")

# ============================================================
# The "yin yang" hint - complementary opposites
# ============================================================

print("\n--- Yin Yang (complement) approach ---")

# Complement the hex key (XOR with all F's)
complement = ''.join(format(15 - int(c, 16), 'x') for c in hex_key)
check_key(complement, "OTP hex complement")

# Complement + original interleaved
interleaved = ''.join(hex_key[i] + complement[i] for i in range(32))
check_key(interleaved, "OTP interleaved with complement")

# ============================================================
# Try the exact 64 chars from different sources
# ============================================================

print("\n--- Exact 64 char extractions ---")

# First 64 hex chars from FAED (only a-f)
faed_hex_only = ''.join(c for c in faed_block if c in 'abcdef')
if len(faed_hex_only) >= 64:
    check_key(faed_hex_only[:64], "FAED first 64 hex")
    check_key(faed_hex_only[-64:], "FAED last 64 hex")
    
    # Middle 64
    mid = (len(faed_hex_only) - 64) // 2
    check_key(faed_hex_only[mid:mid+64], "FAED middle 64 hex")

# ============================================================
# Brute force small variations
# ============================================================

print("\n--- Small variations of main candidate ---")

# The main candidate is hex_key
# Try flipping individual bits/nibbles

main_key = hex_key
print(f"Main candidate: {main_key}")

# Try changing first nibble
for i in range(16):
    variant = format(i, 'x') + main_key[1:]
    if check_key(variant, f"First nibble = {i:x}"):
        break

# Try changing last nibble
for i in range(16):
    variant = main_key[:-1] + format(i, 'x')
    if check_key(variant, f"Last nibble = {i:x}"):
        break

print("\n" + "=" * 70)
print("Search complete.")
print("=" * 70)
