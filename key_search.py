#!/usr/bin/env python3
"""
Comprehensive Bitcoin Private Key Search for NESRD3Q Puzzle
Try many different approaches to find the correct key
"""

import hashlib
import struct
import itertools

# Import the validation function from btc_validate_pure
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
otp_64 = otp_result[27:]  # 64 chars after YOUWON

# Dots pattern
pos_0 = [6, 25, 26, 36, 37, 47, 66, 67, 77, 78, 81, 82, 96, 97, 105, 111, 116, 118, 119, 130, 149, 150, 157, 163, 164, 171, 172, 179, 180, 186, 193, 194]
pos_1 = [7, 19, 48, 59, 89, 100, 128, 143, 158, 173]

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
print("COMPREHENSIVE KEY SEARCH")
print("=" * 70)
print(f"Target: {TARGET}")
print(f"OTP 64: {otp_64}")

# ============================================================
# APPROACH 1: Different letter-to-hex mappings
# ============================================================
print("\n--- Approach 1: Letter-to-hex mappings ---")

mappings = {
    'mod16': lambda c: format((ord(c.upper()) - ord('A')) % 16, 'x'),
    'mod10+a': lambda c: format((ord(c.upper()) - ord('A')) % 10, 'x') if (ord(c.upper()) - ord('A')) >= 6 else c.lower(),
    'a=0': lambda c: format(ord(c.upper()) - ord('A'), 'x') if ord(c.upper()) - ord('A') < 16 else format((ord(c.upper()) - ord('A')) % 16, 'x'),
}

for name, mapping in mappings.items():
    key = ''.join(mapping(c) for c in otp_64)
    check_key(key, f"OTP {name}")

# ============================================================
# APPROACH 2: Use FAED block hex characters
# ============================================================
print("\n--- Approach 2: FAED hex extraction ---")

# Extract only a-f from faed
faed_hex = ''.join(c for c in faed_block if c in 'abcdef')
print(f"FAED hex chars: {len(faed_hex)}")

# Try first 64, last 64, middle 64
if len(faed_hex) >= 64:
    check_key(faed_hex[:64], "FAED first 64")
    check_key(faed_hex[-64:], "FAED last 64")
    mid = (len(faed_hex) - 64) // 2
    check_key(faed_hex[mid:mid+64], "FAED middle 64")

# ============================================================
# APPROACH 3: Use dots pattern positions
# ============================================================
print("\n--- Approach 3: Dots pattern extraction ---")

# Extract from combined block at specific positions
combined = dbbi_block + faed_block

# Characters at 0 positions (32 chars)
chars_at_0 = ''.join(combined[i] for i in pos_0 if i < len(combined))
# Characters at 1 positions (10 chars)
chars_at_1 = ''.join(combined[i] for i in pos_1 if i < len(combined))

print(f"Chars at 0 positions: {chars_at_0}")
print(f"Chars at 1 positions: {chars_at_1}")

# Try combining them in different ways
combined_01 = chars_at_0 + chars_at_1
if len(combined_01) == 42:
    # Pad to 64 with zeros or repeat
    padded = (combined_01 * 2)[:64]
    # Convert to hex
    hex_padded = ''.join(format(ord(c) - ord('a'), 'x') if c in 'abcdefghi' else '0' for c in padded)
    check_key(hex_padded, "Dots pattern padded")

# ============================================================
# APPROACH 4: SHA256 of various strings
# ============================================================
print("\n--- Approach 4: SHA256 hashes ---")

strings_to_hash = [
    otp_64,
    otp_result,
    dbbi_block,
    faed_block,
    dbbi_block + faed_block,
    "YOUWON" + otp_64,
    chars_at_0 + chars_at_1,
    "btcseed",
    "matrixsumlist",
]

for s in strings_to_hash:
    h = hashlib.sha256(s.encode()).hexdigest()
    check_key(h, f"SHA256({s[:20]}...)")

# ============================================================
# APPROACH 5: Bifid with different squares
# ============================================================
print("\n--- Approach 5: Bifid cipher variations ---")

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

def bifid_decrypt(ciphertext, square, size=3):
    coords = []
    for char in ciphertext.lower():
        if char in square:
            idx = square.index(char)
            coords.append((idx // size, idx % size))
    
    n = len(coords)
    combined = []
    for r, c in coords:
        combined.append(r)
    for r, c in coords:
        combined.append(c)
    
    rows = combined[:n]
    cols = combined[n:]
    
    plaintext = []
    for i in range(n):
        plaintext.append(square[rows[i] * size + cols[i]])
    
    return ''.join(plaintext)

# Try different keywords
keywords = ['dbifhceg', 'abcdefghi', 'matrixsum', 'btcseed']

for kw in keywords:
    sq = create_square(kw)
    decrypted = bifid_decrypt(faed_block, sq)
    
    # Extract hex chars from decrypted
    hex_chars = ''.join(c for c in decrypted if c in 'abcdef')
    if len(hex_chars) >= 64:
        check_key(hex_chars[:64], f"Bifid({kw}) hex")

# ============================================================
# APPROACH 6: XOR combinations
# ============================================================
print("\n--- Approach 6: XOR combinations ---")

def text_to_bytes(text, mapping='a=0'):
    if mapping == 'a=0':
        return bytes([ord(c.lower()) - ord('a') for c in text if c.isalpha()])
    return text.encode()

def xor_bytes(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, b2)])

# XOR OTP with FAED
otp_bytes = text_to_bytes(otp_64)
faed_bytes = text_to_bytes(faed_block[:64])

xored = xor_bytes(otp_bytes, faed_bytes)
xor_hex = xored.hex()
if len(xor_hex) >= 64:
    check_key(xor_hex[:64], "XOR OTP^FAED")

# ============================================================
# APPROACH 7: Try the 64 chars directly as hex (a-f only)
# ============================================================
print("\n--- Approach 7: Direct hex interpretation ---")

# The OTP 64 chars contain some letters that are valid hex (a-f)
# Try keeping those and converting others

def convert_to_hex_keep_valid(text):
    result = []
    for c in text.lower():
        if c in 'abcdef':
            result.append(c)
        elif c in 'ghij':
            result.append(str(ord(c) - ord('g')))  # g=0, h=1, i=2, j=3
        elif c in 'klmn':
            result.append(str(ord(c) - ord('k') + 4))  # k=4, l=5, m=6, n=7
        elif c in 'opqr':
            result.append(str(ord(c) - ord('o') + 8))  # o=8, p=9, q=a, r=b
        else:
            result.append(format((ord(c) - ord('a')) % 16, 'x'))
    return ''.join(result)

key = convert_to_hex_keep_valid(otp_64)
check_key(key, "OTP convert_keep_valid")

# ============================================================
# APPROACH 8: Use the binary from dots pattern
# ============================================================
print("\n--- Approach 8: Binary from dots ---")

# 42 binary digits from dots pattern
binary_str = ''
for i in range(196):
    if i in pos_0:
        binary_str += '0'
    elif i in pos_1:
        binary_str += '1'

print(f"Binary from dots: {binary_str}")

# Pad to 256 bits (64 hex chars)
binary_padded = binary_str.zfill(256)
hex_from_binary = hex(int(binary_padded, 2))[2:].zfill(64)
check_key(hex_from_binary, "Binary from dots padded")

# ============================================================
# APPROACH 9: Combined approaches
# ============================================================
print("\n--- Approach 9: Combined approaches ---")

# Use dots pattern to select from faed
selected = ''.join(faed_block[i] for i in sorted(pos_0 + pos_1) if i < len(faed_block))
print(f"Selected by dots: {selected}")

# Convert to hex
selected_hex = ''.join(format(ord(c) - ord('a'), 'x') for c in selected)
print(f"Selected as hex: {selected_hex}")

# Pad if needed
if len(selected_hex) < 64:
    selected_hex = selected_hex.ljust(64, '0')
check_key(selected_hex[:64], "Dots-selected from FAED")

print("\n" + "=" * 70)
print("Search complete. No match found in tested approaches.")
print("=" * 70)
