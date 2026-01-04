#!/usr/bin/env python3
"""
Last attempt - trying more creative approaches
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
            with open('SOLUTION_FOUND.txt', 'w') as f:
                f.write(f"Method: {name}\n")
                f.write(f"Private Key: {key}\n")
                f.write(f"Address: {addr}\n")
            return True
    return False

print("=" * 70)
print("LAST ATTEMPT - CREATIVE APPROACHES")
print("=" * 70)

# ============================================================
# The hint says "btcseed" should appear
# What if we need to find where "btcseed" is encoded?
# ============================================================

print("\n--- Looking for btcseed encoding ---")

# "btcseed" as ASCII hex
btcseed_hex = ''.join(format(ord(c), '02x') for c in 'btcseed')
print(f"'btcseed' as hex: {btcseed_hex}")

# Check if this appears in any of our data
if btcseed_hex in combined:
    print("Found in combined block!")
    
# What if the FAED block starts with encoded "btcseed"?
# b=1, t=19, c=2, s=18, e=4, e=4, d=3 (0-indexed)
# In a-i: b=1, c=2, d=3, e=4 are valid
# t=19, s=18 are NOT in a-i range

# ============================================================
# Try using the OTP key itself as part of the solution
# ============================================================

print("\n--- Using OTP key ---")

# SHA256 of the OTP key
otp_key_hash = hashlib.sha256(otp_key.encode()).hexdigest()
print(f"SHA256(OTP key): {otp_key_hash}")
check_key(otp_key_hash, "SHA256(OTP key)")

# XOR OTP result with OTP key
def xor_strings(s1, s2):
    result = []
    for i in range(len(s1)):
        c1 = ord(s1[i].upper()) - ord('A') if s1[i].isalpha() else 0
        c2 = ord(s2[i % len(s2)].upper()) - ord('A') if s2[i % len(s2)].isalpha() else 0
        result.append(format((c1 ^ c2) % 16, 'x'))
    return ''.join(result)

xored = xor_strings(otp_64, otp_key)
print(f"OTP64 XOR OTP_key: {xored}")
check_key(xored, "OTP64 XOR OTP_key")

# ============================================================
# Try the full OTP result (91 chars) 
# ============================================================

print("\n--- Full OTP result approaches ---")

# The full result is 91 chars
# 91 = 64 + 27 (YOUWON is at position 21, so 21 + 6 = 27 before the 64)
# What if we need to use all 91 chars?

# Convert all 91 to hex
full_hex = ''.join(format((ord(c) - ord('A')) % 16, 'x') for c in otp_result)
print(f"Full OTP as hex ({len(full_hex)} chars): {full_hex}")

# Take specific portions
check_key(full_hex[:64], "Full OTP first 64")
check_key(full_hex[-64:], "Full OTP last 64")
check_key(full_hex[27:91], "Full OTP 27-91")

# ============================================================
# The "YOUWON" might be significant
# ============================================================

print("\n--- YOUWON significance ---")

# YOUWON as hex
youwon_hex = ''.join(format(ord(c), '02x') for c in 'YOUWON')
print(f"'YOUWON' as hex: {youwon_hex}")

# SHA256 of YOUWON + 64 chars
combined_str = "YOUWON" + otp_64
h = hashlib.sha256(combined_str.encode()).hexdigest()
check_key(h, "SHA256(YOUWON + OTP64)")

# What if YOUWON tells us something about the key?
# Y=24, O=14, U=20, W=22, O=14, N=13
# Sum = 107
# Product = 24*14*20*22*14*13 = very large

# ============================================================
# Try the address itself
# ============================================================

print("\n--- Address-based approaches ---")

# The address is 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
# What if we need to decode it?

# SHA256 of address
addr_hash = hashlib.sha256(TARGET.encode()).hexdigest()
check_key(addr_hash, "SHA256(address)")

# ============================================================
# Try combining DBBI and FAED in different ways
# ============================================================

print("\n--- DBBI + FAED combinations ---")

# Interleave DBBI and FAED
interleaved = ''
for i in range(max(len(dbbi_block), len(faed_block))):
    if i < len(dbbi_block):
        interleaved += dbbi_block[i]
    if i < len(faed_block):
        interleaved += faed_block[i]

# Convert to hex
inter_hex = ''.join(format(ord(c) - ord('a'), 'x') for c in interleaved[:64])
print(f"Interleaved first 64 as hex: {inter_hex}")

# ============================================================
# Try base conversion
# ============================================================

print("\n--- Base conversion ---")

# The combined block uses base 9 (letters a-i = 0-8)
# Convert to base 16 (hex)

# First 64 chars of combined as base-9 number
base9_str = ''.join(str(ord(c) - ord('a')) for c in combined[:64])
print(f"Base-9 string: {base9_str}")

# Convert to integer
try:
    base9_num = int(base9_str, 9)
    hex_from_base9 = format(base9_num, 'x')
    print(f"As hex: {hex_from_base9[:64]}...")
    if len(hex_from_base9) >= 64:
        check_key(hex_from_base9[:64], "Base9 to hex first 64")
        check_key(hex_from_base9[-64:], "Base9 to hex last 64")
except:
    print("Base-9 conversion failed")

# ============================================================
# Try the puzzle image colors
# ============================================================

print("\n--- Color-based approach ---")

# 9 yellow squares, 15 blue squares
# Primes up to 9: 2, 3, 5, 7
# Primes up to 15: 2, 3, 5, 7, 11, 13

yellow_primes = [2, 3, 5, 7]
blue_primes = [2, 3, 5, 7, 11, 13]

# Extract chars at these positions from combined
yellow_chars = ''.join(combined[p] for p in yellow_primes if p < len(combined))
blue_chars = ''.join(combined[p] for p in blue_primes if p < len(combined))

print(f"Yellow prime positions: {yellow_chars}")
print(f"Blue prime positions: {blue_chars}")

# ============================================================
# Try double hashing
# ============================================================

print("\n--- Double hashing ---")

# Double SHA256 (like Bitcoin uses)
h1 = hashlib.sha256(otp_64.encode()).digest()
h2 = hashlib.sha256(h1).hexdigest()
check_key(h2, "Double SHA256(OTP64)")

# ============================================================
# Try the "in front of your eyes" hint literally
# ============================================================

print("\n--- Literal interpretation ---")

# What's literally in front of our eyes?
# The puzzle image, the address, the blocks...

# The address starts with "1GSMG" - what if we use this?
# 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe

# Extract letters only from address
addr_letters = ''.join(c for c in TARGET if c.isalpha())
print(f"Address letters: {addr_letters}")

# Convert to hex
addr_hex = ''.join(format((ord(c.upper()) - ord('A')) % 16, 'x') for c in addr_letters)
print(f"Address letters as hex: {addr_hex}")

if len(addr_hex) >= 64:
    check_key(addr_hex[:64], "Address letters hex")

print("\n" + "=" * 70)
print("Last attempt complete.")
print("=" * 70)
