#!/usr/bin/env python3
"""
Extract Bitcoin Private Key from NESRD3Q Puzzle
Combining OTP result, Bifid cipher, and dots pattern
"""

import hashlib
import binascii

# Load all the data
with open('dbbi_block.txt', 'r') as f:
    dbbi_block = f.read().strip()

with open('faed_block.txt', 'r') as f:
    faed_block = f.read().strip()

# OTP decryption result
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

print("=" * 70)
print("DATA SUMMARY")
print("=" * 70)
print(f"DBBI block: {dbbi_block}")
print(f"OTP result: {otp_result}")
print(f"OTP 64-char: {otp_64}")
print(f"FAED block ({len(faed_block)} chars): {faed_block[:50]}...")

# Dots pattern positions
pos_0 = [6, 25, 26, 36, 37, 47, 66, 67, 77, 78, 81, 82, 96, 97, 105, 111, 116, 118, 119, 130, 149, 150, 157, 163, 164, 171, 172, 179, 180, 186, 193, 194]
pos_1 = [7, 19, 48, 59, 89, 100, 128, 143, 158, 173]

print(f"\nDots pattern: {len(pos_0)} zeros, {len(pos_1)} ones")

# ============================================================
# APPROACH 1: Convert OTP 64 chars to hex
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 1: Letter-to-hex conversion of OTP 64")
print("=" * 70)

# Method A: a=0, b=1, ..., f=5, g=6, ..., p=15, then mod 16
def letter_to_hex_mod16(text):
    result = []
    for c in text.lower():
        val = ord(c) - ord('a')
        hex_val = val % 16
        result.append(format(hex_val, 'x'))
    return ''.join(result)

hex_mod16 = letter_to_hex_mod16(otp_64)
print(f"Method A (mod 16): {hex_mod16}")
print(f"Length: {len(hex_mod16)}")

# Method B: Only keep a-f, replace others with their position mod 16
def letter_to_hex_direct(text):
    result = []
    for c in text.lower():
        if c in 'abcdef':
            result.append(c)
        else:
            val = ord(c) - ord('a')
            result.append(format(val % 16, 'x'))
    return ''.join(result)

hex_direct = letter_to_hex_direct(otp_64)
print(f"Method B (direct): {hex_direct}")

# ============================================================
# APPROACH 2: Use dots pattern as extraction mask
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 2: Dots pattern as extraction mask")
print("=" * 70)

# The combined block is 661 chars (91 + 570)
combined = dbbi_block + faed_block
print(f"Combined block: {len(combined)} chars")

# Extract chars at positions where dots pattern has 0
extracted_at_0 = ''.join(combined[i] for i in pos_0 if i < len(combined))
print(f"Chars at '0' positions: {extracted_at_0}")
print(f"Length: {len(extracted_at_0)}")

# Extract chars at positions where dots pattern has 1
extracted_at_1 = ''.join(combined[i] for i in pos_1 if i < len(combined))
print(f"Chars at '1' positions: {extracted_at_1}")
print(f"Length: {len(extracted_at_1)}")

# Combine 0 and 1 extractions
combined_01 = extracted_at_0 + extracted_at_1
print(f"Combined (0s + 1s): {combined_01}")
print(f"Length: {len(combined_01)}")

# ============================================================
# APPROACH 3: Apply pattern to FAED block for Bifid
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 3: Pattern-guided Bifid decryption")
print("=" * 70)

# The faed block might need the dots pattern to guide decryption
# 32 zeros + 10 ones = 42 positions with values
# 42 * 1.5 = 63 (close to 64!)

# Try extracting every position that's NOT a dot
non_dot_positions = sorted(pos_0 + pos_1)
print(f"Non-dot positions: {non_dot_positions}")
print(f"Count: {len(non_dot_positions)}")

# Extract from faed at these positions
faed_extracted = ''.join(faed_block[i] for i in non_dot_positions if i < len(faed_block))
print(f"FAED at non-dot positions: {faed_extracted}")
print(f"Length: {len(faed_extracted)}")

# ============================================================
# APPROACH 4: Hex from faed block
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 4: Extract hex from FAED block")
print("=" * 70)

# The faed block uses a-i, where a-f are valid hex
# Extract only hex-valid characters
faed_hex_only = ''.join(c for c in faed_block if c in 'abcdef')
print(f"FAED hex-only: {faed_hex_only[:64]}")
print(f"Total hex chars: {len(faed_hex_only)}")

# First 64 hex chars
if len(faed_hex_only) >= 64:
    candidate_key = faed_hex_only[:64]
    print(f"First 64 hex chars: {candidate_key}")

# ============================================================
# APPROACH 5: Combine OTP and FAED
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 5: Combine OTP and FAED data")
print("=" * 70)

# XOR the OTP result with something from FAED
# First, convert both to numbers

def text_to_nums(text):
    return [ord(c.lower()) - ord('a') for c in text if c.isalpha()]

otp_nums = text_to_nums(otp_64)
faed_nums = text_to_nums(faed_block[:64])

print(f"OTP nums (first 10): {otp_nums[:10]}")
print(f"FAED nums (first 10): {faed_nums[:10]}")

# XOR them
xor_result = [(o ^ f) % 16 for o, f in zip(otp_nums, faed_nums)]
xor_hex = ''.join(format(x, 'x') for x in xor_result)
print(f"XOR result (hex): {xor_hex}")

# ============================================================
# APPROACH 6: Use the 42 binary digits from dots pattern
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 6: Binary from dots pattern")
print("=" * 70)

# The dots pattern has 32 zeros and 10 ones = 42 binary digits
# Read them in order of position
binary_from_dots = ''
for i in range(196):
    if i in pos_0:
        binary_from_dots += '0'
    elif i in pos_1:
        binary_from_dots += '1'

print(f"Binary from dots: {binary_from_dots}")
print(f"Length: {len(binary_from_dots)}")

# Convert to decimal
decimal_from_dots = int(binary_from_dots, 2)
print(f"Decimal: {decimal_from_dots}")
print(f"Hex: {hex(decimal_from_dots)}")

# ============================================================
# APPROACH 7: Map letters to hex using position in alphabet
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 7: Various letter-to-hex mappings")
print("=" * 70)

# The OTP result is all uppercase A-Z
# Map to hex: A=a, B=b, ..., F=f, G=0, H=1, ..., P=9, Q=a, etc.

def otp_to_hex_v1(text):
    """A-F -> a-f, G-P -> 0-9, Q-Z -> a-j"""
    result = []
    for c in text.upper():
        if 'A' <= c <= 'F':
            result.append(c.lower())
        elif 'G' <= c <= 'P':
            result.append(str(ord(c) - ord('G')))
        else:  # Q-Z
            result.append(format((ord(c) - ord('Q')) % 16, 'x'))
    return ''.join(result)

def otp_to_hex_v2(text):
    """Simple mod 16 mapping"""
    result = []
    for c in text.upper():
        val = ord(c) - ord('A')
        result.append(format(val % 16, 'x'))
    return ''.join(result)

def otp_to_hex_v3(text):
    """A=0, B=1, ..., O=e, P=f, then repeat"""
    result = []
    for c in text.upper():
        val = ord(c) - ord('A')
        result.append(format(val % 16, 'x'))
    return ''.join(result)

print(f"V1 mapping: {otp_to_hex_v1(otp_64)}")
print(f"V2 mapping: {otp_to_hex_v2(otp_64)}")
print(f"V3 mapping: {otp_to_hex_v3(otp_64)}")

# ============================================================
# APPROACH 8: Check if any candidate is a valid private key
# ============================================================
print("\n" + "=" * 70)
print("APPROACH 8: Validate candidate keys")
print("=" * 70)

def validate_btc_key(hex_key, target_address):
    """Check if a hex private key generates the target Bitcoin address."""
    try:
        # This requires ecdsa library
        import ecdsa
        import hashlib
        
        # Convert hex to bytes
        private_key_bytes = bytes.fromhex(hex_key)
        
        # Generate public key
        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        
        # Uncompressed public key
        public_key = b'\x04' + vk.to_string()
        
        # SHA256
        sha256_hash = hashlib.sha256(public_key).digest()
        
        # RIPEMD160
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        hash160 = ripemd160.digest()
        
        # Add version byte (0x00 for mainnet)
        versioned = b'\x00' + hash160
        
        # Double SHA256 for checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        
        # Base58 encode
        address_bytes = versioned + checksum
        
        # Base58 encoding
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        num = int.from_bytes(address_bytes, 'big')
        result = ''
        while num > 0:
            num, rem = divmod(num, 58)
            result = alphabet[rem] + result
        
        # Add leading 1s for leading zero bytes
        for byte in address_bytes:
            if byte == 0:
                result = '1' + result
            else:
                break
        
        return result == target_address, result
    except Exception as e:
        return False, str(e)

# Target address
target = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# Test candidates
candidates = [
    ("OTP mod16", hex_mod16),
    ("OTP direct", hex_direct),
    ("FAED hex", faed_hex_only[:64] if len(faed_hex_only) >= 64 else ""),
    ("XOR result", xor_hex),
    ("OTP V1", otp_to_hex_v1(otp_64)),
    ("OTP V2", otp_to_hex_v2(otp_64)),
]

print(f"Target address: {target}\n")

for name, key in candidates:
    if len(key) == 64 and all(c in '0123456789abcdef' for c in key):
        try:
            # Try to install ecdsa if not present
            import subprocess
            subprocess.run(['pip3', 'install', 'ecdsa', '-q'], capture_output=True)
            
            match, generated = validate_btc_key(key, target)
            status = "MATCH!" if match else f"Generated: {generated[:20]}..."
            print(f"{name}: {key[:32]}... -> {status}")
        except Exception as e:
            print(f"{name}: {key[:32]}... -> Error: {e}")
    else:
        print(f"{name}: Invalid key format (len={len(key)})")
