#!/usr/bin/env python3
"""
Thorough Bifid Cipher Analysis for NESRD3Q Puzzle
The prompt says Bifid with keyword "dbifhceg" should produce "btcseed" + 563 chars
"""

import itertools

# Load data
with open('faed_block.txt', 'r') as f:
    faed_block = f.read().strip()

print("=" * 70)
print("BIFID CIPHER THOROUGH ANALYSIS")
print("=" * 70)
print(f"FAED block length: {len(faed_block)}")
print(f"FAED block: {faed_block[:50]}...")

# The FAED block uses letters a-i (9 letters)
# This fits a 3x3 Polybius square perfectly

# Standard Bifid cipher operations
def create_square(keyword, alphabet='abcdefghi'):
    """Create Polybius square from keyword."""
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

def get_coords(char, square, size=3):
    """Get row, col for a character."""
    idx = square.index(char)
    return idx // size, idx % size

def get_char(row, col, square, size=3):
    """Get character at row, col."""
    return square[row * size + col]

def bifid_encrypt(plaintext, square, size=3):
    """Encrypt using Bifid cipher."""
    rows, cols = [], []
    for c in plaintext.lower():
        if c in square:
            r, c_coord = get_coords(c, square, size)
            rows.append(r)
            cols.append(c_coord)
    
    combined = rows + cols
    n = len(rows)
    
    ciphertext = []
    for i in range(n):
        r = combined[i]
        c = combined[i + n]
        ciphertext.append(get_char(r, c, square, size))
    
    return ''.join(ciphertext)

def bifid_decrypt(ciphertext, square, size=3):
    """Decrypt using Bifid cipher."""
    coords = []
    for c in ciphertext.lower():
        if c in square:
            r, col = get_coords(c, square, size)
            coords.append((r, col))
    
    n = len(coords)
    
    # Extract rows and cols from ciphertext coordinates
    combined = []
    for r, c in coords:
        combined.append(r)
    for r, c in coords:
        combined.append(c)
    
    # Split back to get plaintext coordinates
    rows = combined[:n]
    cols = combined[n:]
    
    plaintext = []
    for i in range(n):
        plaintext.append(get_char(rows[i], cols[i], square, size))
    
    return ''.join(plaintext)

# Test with keyword "dbifhceg"
keyword = "dbifhceg"
square = create_square(keyword)

print(f"\nKeyword: {keyword}")
print(f"Square: {square}")
print("Grid:")
for i in range(3):
    print(f"  {square[i*3:(i+1)*3]}")

# Decrypt FAED
decrypted = bifid_decrypt(faed_block, square)
print(f"\nDecrypted: {decrypted[:50]}...")
print(f"Starts with 'btcseed': {decrypted.startswith('btcseed')}")

# The problem: the alphabet is a-i, but "btcseed" contains 't' and 's' which are NOT in a-i!
# So the expected output "btcseed" must be encoded somehow

# Maybe "btcseed" is in a different encoding?
# Or maybe the Bifid output needs to be converted?

print("\n" + "=" * 70)
print("INVESTIGATING 'btcseed' ENCODING")
print("=" * 70)

# If we're limited to a-i, how would "btcseed" be represented?
# Option 1: b=b, t=?, c=c, s=?, e=e, e=e, d=d
# Letters b, c, d, e are in a-i
# Letters t, s are NOT in a-i

# Maybe the output is in a different format?
# Or maybe we need to interpret the output differently?

# Let's see what "btcseed" would encrypt to with this square
# First, we need to map btcseed to a-i somehow

# Option: Use only the letters that ARE in a-i
btc_in_ai = ''.join(c for c in 'btcseed' if c in 'abcdefghi')
print(f"'btcseed' filtered to a-i: '{btc_in_ai}'")

# What if the Bifid output is meant to be interpreted as hex?
# a=0xa, b=0xb, c=0xc, d=0xd, e=0xe, f=0xf, g=?, h=?, i=?

print("\n" + "=" * 70)
print("TRYING DIFFERENT INTERPRETATIONS")
print("=" * 70)

# Interpretation 1: The decrypted output IS the key material (not "btcseed")
print(f"\nDecrypted as-is: {decrypted[:64]}")

# Extract hex-valid chars (a-f)
hex_valid = ''.join(c for c in decrypted if c in 'abcdef')
print(f"Hex-valid chars: {hex_valid[:64]}...")
print(f"Total hex-valid: {len(hex_valid)}")

# Interpretation 2: Convert a-i to hex (a=a, b=b, ..., f=f, g=0, h=1, i=2)
def ai_to_hex(text):
    result = []
    for c in text:
        if c in 'abcdef':
            result.append(c)
        elif c == 'g':
            result.append('0')
        elif c == 'h':
            result.append('1')
        elif c == 'i':
            result.append('2')
    return ''.join(result)

decrypted_hex = ai_to_hex(decrypted)
print(f"\nDecrypted as hex (g=0,h=1,i=2): {decrypted_hex[:64]}...")

# Interpretation 3: The FAED block itself might be the encrypted form of something
# that decrypts to hex

# Let's try all possible 3x3 squares (9! = 362880 permutations)
# Too many, but let's try some strategic ones

print("\n" + "=" * 70)
print("TRYING DIFFERENT SQUARES")
print("=" * 70)

# Try squares that might produce "btc" at the start
# We need the first 3 chars of decryption to be b, t, c
# But t is not in a-i, so this won't work directly

# Alternative: What if the expected output is NOT "btcseed" literally?
# What if it's a pattern that LOOKS like "btcseed" when interpreted?

# Let's check what the FAED block decrypts to with different squares
test_keywords = [
    'abcdefghi',  # standard
    'dbifhceg',   # given keyword
    'dbifhcega',  # keyword + a
    'adbifhceg',  # a + keyword
    'bcdefghia',  # rotated
    'ihgfedcba',  # reversed
]

for kw in test_keywords:
    sq = create_square(kw)
    dec = bifid_decrypt(faed_block, sq)
    print(f"\nKeyword '{kw}' -> Square '{sq}'")
    print(f"  First 30: {dec[:30]}")
    print(f"  Last 30: {dec[-30:]}")
    
    # Check for any recognizable patterns
    hex_only = ''.join(c for c in dec if c in 'abcdef')
    print(f"  Hex chars: {len(hex_only)}")

# ============================================================
# CRITICAL INSIGHT: Maybe the Bifid cipher uses a DIFFERENT alphabet
# ============================================================
print("\n" + "=" * 70)
print("TRYING EXTENDED ALPHABET")
print("=" * 70)

# What if the puzzle uses a 5x5 Polybius square with 25 letters?
# Standard Bifid uses 25 letters (usually combining i/j)

# But our input only has a-i (9 letters)
# This suggests a 3x3 square is correct

# However, the OUTPUT might be in a different format
# Let's see if the decrypted text can be converted to something meaningful

# Try treating pairs of letters as coordinates
def pairs_to_text(text, alphabet='abcdefghijklmnopqrstuvwxyz'):
    """Convert pairs of a-i to letters using them as coordinates."""
    result = []
    for i in range(0, len(text) - 1, 2):
        r = ord(text[i]) - ord('a')
        c = ord(text[i+1]) - ord('a')
        idx = r * 9 + c  # 9x9 grid
        if idx < len(alphabet):
            result.append(alphabet[idx])
        else:
            result.append('?')
    return ''.join(result)

converted = pairs_to_text(decrypted)
print(f"Pairs as coordinates: {converted[:30]}...")

# Or maybe each letter represents a digit?
def letters_to_digits(text):
    """a=0, b=1, ..., i=8"""
    return ''.join(str(ord(c) - ord('a')) for c in text if c in 'abcdefghi')

digits = letters_to_digits(decrypted)
print(f"As digits: {digits[:64]}...")

# Convert digit pairs to hex
def digit_pairs_to_hex(digits):
    """Convert pairs of base-9 digits to hex."""
    result = []
    for i in range(0, len(digits) - 1, 2):
        val = int(digits[i]) * 9 + int(digits[i+1])
        result.append(format(val % 256, '02x'))
    return ''.join(result)

hex_from_digits = digit_pairs_to_hex(digits)
print(f"Digit pairs to hex: {hex_from_digits[:64]}...")

print("\n" + "=" * 70)
print("Analysis complete.")
print("=" * 70)
