#!/usr/bin/env python3
"""
Deep Analysis of NESRD3Q Puzzle
Investigating all hints and patterns
"""

import hashlib

# Import validation
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

def check_key(key, name):
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
            print(f"{'='*70}")
            return True
    return False

print("=" * 70)
print("DEEP ANALYSIS")
print("=" * 70)

# ============================================================
# KEY INSIGHT: The Bifid decryption seems to return the same text!
# This suggests the FAED block might already BE the plaintext
# ============================================================

print("\n--- Investigating FAED as plaintext ---")

# The FAED block has 570 chars
# 570 = 7 + 563 (btcseed + key material)
# But "btcseed" can't be represented in a-i alphabet

# What if the first 7 chars of FAED represent something?
first_7 = faed_block[:7]
print(f"First 7 chars of FAED: {first_7}")

# Convert to numbers (a=0, b=1, ..., i=8)
first_7_nums = [ord(c) - ord('a') for c in first_7]
print(f"As numbers: {first_7_nums}")

# What if these are coordinates or indices?
# Or what if they encode "btcseed" somehow?

# ============================================================
# The OTP decryption WORKED - we got "YOUWON" at position 21
# The 64 chars after YOUWON are the key material
# ============================================================

print("\n--- OTP 64 chars analysis ---")
print(f"OTP 64: {otp_64}")

# The 64 chars are uppercase letters A-Z
# We need to convert them to 64 hex chars

# Method: Use the letter positions to create hex
# But A-Z is 26 letters, hex is 16 values

# What if we use a Polybius-like encoding?
# 26 letters -> 5x5 grid (with one letter combined)
# Each letter -> 2 digits (row, col)
# But that gives 128 digits, not 64

# Alternative: Use mod 16
# A=0, B=1, ..., O=14, P=15, Q=0, R=1, ...

def alpha_to_hex_mod16(text):
    return ''.join(format((ord(c) - ord('A')) % 16, 'x') for c in text.upper())

hex_mod16 = alpha_to_hex_mod16(otp_64)
print(f"Mod 16: {hex_mod16}")
check_key(hex_mod16, "OTP mod16")

# What if we need to combine OTP and FAED?
# OTP has 64 chars, FAED has 570 chars

# ============================================================
# The dots pattern has 32 zeros and 10 ones
# 32 + 10 = 42 positions
# ============================================================

print("\n--- Dots pattern deep analysis ---")

dots_raw = """. . . . . . 0 1 . . . . . . . . . . . 1 . . . . . 0 0 . . . . . . . . . 0 0 . . . . . . . . . 0 1 . . . . . . . . . . 1 . . . . . . 0 0 . . . . . . . . . 0 0 . . 0 0 . . . . . . 1 . . . . . . 0 0 . . 1 . . . . 0 . . . . . 0 . . . . 0 . 0 0 . . . . . . . . 1 . 0 . . . . . . . . . . . . 1 . . . . . 0 0 . . . . . . 0 1 . . . . 0 0 . . . . . . 0 0 1 . . . . . 0 0 . . . . . 0 . . . . . . 0 0 ."""
dots = dots_raw.split()

pos_0 = [i for i, d in enumerate(dots) if d == '0']
pos_1 = [i for i, d in enumerate(dots) if d == '1']

print(f"Zeros at: {pos_0}")
print(f"Ones at: {pos_1}")

# The hint says "hexdumping all the stuff"
# What if we need to hexdump the combined block and use dots as mask?

combined = dbbi_block + faed_block
print(f"Combined length: {len(combined)}")

# Hexdump: convert each char to its numeric value (a=0, b=1, ..., i=8)
# Then express as hex
hexdump = ''.join(format(ord(c) - ord('a'), 'x') for c in combined)
print(f"Hexdump length: {len(hexdump)}")
print(f"Hexdump first 64: {hexdump[:64]}")

# Use dots positions to extract from hexdump
extracted = ''.join(hexdump[i] for i in sorted(pos_0 + pos_1) if i < len(hexdump))
print(f"Extracted at dots positions: {extracted}")

# ============================================================
# What if the 64 chars need to come from specific positions?
# ============================================================

print("\n--- Position-based extraction ---")

# The OTP gives us 64 chars
# The dots pattern has 42 non-dot positions
# 64 - 42 = 22

# What if we need 64 specific positions from the combined block?
# Positions could be: 0, 1, 2, ..., 63 (first 64)
# Or: every 10th position (661/10 ≈ 66)
# Or: prime positions

# Try extracting at positions that are multiples of some number
for step in [10, 11, 12, 13]:
    extracted = combined[::step][:64]
    if len(extracted) == 64:
        # Convert to hex
        hex_extracted = ''.join(format(ord(c) - ord('a'), 'x') for c in extracted)
        print(f"Every {step}th char as hex: {hex_extracted}")
        check_key(hex_extracted, f"Every {step}th")

# ============================================================
# What if the answer is simpler?
# "The password is in front of your eyes but you're not seeing it"
# ============================================================

print("\n--- Simple approaches ---")

# What if the private key is just the SHA256 of something obvious?
obvious_strings = [
    "YOUWON",
    "youwon",
    otp_64,
    otp_result,
    "VOZIJBDTIQBRGVEOMZNBCYOUWON" + otp_64,
    dbbi_block,
    faed_block,
    combined,
    "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",  # the address itself
    "gsmg.io",
    "theseedisplanted",
    "theflowerblossomsthroughwhatseemstobeaconcretesurface",
]

for s in obvious_strings:
    h = hashlib.sha256(s.encode()).hexdigest()
    if check_key(h, f"SHA256({s[:30]}...)"):
        break

# ============================================================
# What if the OTP 64 chars ARE the key in some encoding?
# ============================================================

print("\n--- OTP as key directly ---")

# The OTP 64 chars: XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCBDDMOBMLMQW

# What if each letter represents a hex digit based on its position in the alphabet?
# A=0, B=1, C=2, D=3, E=4, F=5 (these are valid hex)
# G=6, H=7, I=8, J=9, K=A, L=B, M=C, N=D, O=E, P=F (extended mapping)

def alpha_to_hex_extended(text):
    mapping = {
        'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4', 'F': '5',
        'G': '6', 'H': '7', 'I': '8', 'J': '9', 'K': 'a', 'L': 'b',
        'M': 'c', 'N': 'd', 'O': 'e', 'P': 'f', 'Q': '0', 'R': '1',
        'S': '2', 'T': '3', 'U': '4', 'V': '5', 'W': '6', 'X': '7',
        'Y': '8', 'Z': '9'
    }
    return ''.join(mapping.get(c, '0') for c in text.upper())

hex_extended = alpha_to_hex_extended(otp_64)
print(f"Extended mapping: {hex_extended}")
check_key(hex_extended, "OTP extended mapping")

# Another mapping: A-P = 0-F (hex), Q-Z = 0-9
def alpha_to_hex_v2(text):
    result = []
    for c in text.upper():
        if 'A' <= c <= 'P':
            result.append(format(ord(c) - ord('A'), 'x'))
        else:
            result.append(str((ord(c) - ord('Q')) % 10))
    return ''.join(result)

hex_v2 = alpha_to_hex_v2(otp_64)
print(f"A-P=hex, Q-Z=digit: {hex_v2}")
check_key(hex_v2, "OTP A-P hex")

print("\n" + "=" * 70)
print("Analysis complete.")
print("=" * 70)
