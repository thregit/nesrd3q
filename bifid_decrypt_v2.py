#!/usr/bin/env python3
"""
Proper Bifid Cipher Implementation for NESRD3Q Puzzle
The puzzle uses a 9-letter alphabet (a-i) with a 3x3 Polybius square
"""

def create_polybius_square_3x3(keyword):
    """
    Create a 3x3 Polybius square for alphabet a-i.
    """
    alphabet = 'abcdefghi'
    square = []
    seen = set()
    
    for char in keyword.lower():
        if char in alphabet and char not in seen:
            square.append(char)
            seen.add(char)
    
    for char in alphabet:
        if char not in seen:
            square.append(char)
            seen.add(char)
    
    return ''.join(square)

def bifid_encrypt(plaintext, square, size=3):
    """Encrypt using Bifid cipher."""
    # Get coordinates
    rows = []
    cols = []
    for char in plaintext.lower():
        if char in square:
            idx = square.index(char)
            rows.append(idx // size)
            cols.append(idx % size)
    
    # Combine rows then cols
    combined = rows + cols
    
    # Pair up to get ciphertext
    ciphertext = []
    n = len(rows)
    for i in range(n):
        r = combined[i]
        c = combined[i + n]
        ciphertext.append(square[r * size + c])
    
    return ''.join(ciphertext)

def bifid_decrypt(ciphertext, square, size=3):
    """
    Decrypt using Bifid cipher.
    
    For decryption, we reverse the encryption process:
    1. Get coordinates of ciphertext
    2. The coordinates represent paired (row_i, col_i) from combined sequence
    3. Split back into original rows and cols
    4. Reconstruct plaintext
    """
    # Get coordinates of ciphertext
    coords = []
    for char in ciphertext.lower():
        if char in square:
            idx = square.index(char)
            coords.append((idx // size, idx % size))
    
    n = len(coords)
    
    # The ciphertext coordinates came from pairing combined[i] with combined[i+n]
    # where combined = rows + cols
    # So coords[i] = (rows[i], cols[i]) from the combined sequence
    
    # Extract the combined sequence
    combined = []
    for r, c in coords:
        combined.append(r)
    for r, c in coords:
        combined.append(c)
    
    # Now combined = rows + cols of plaintext
    # Split back
    rows = combined[:n]
    cols = combined[n:]
    
    # Reconstruct plaintext
    plaintext = []
    for i in range(n):
        plaintext.append(square[rows[i] * size + cols[i]])
    
    return ''.join(plaintext)

# Test with known example
print("=" * 70)
print("TESTING BIFID CIPHER IMPLEMENTATION")
print("=" * 70)

# Test square
test_square = "dbifhcega"
print(f"Test square: {test_square}")

# Test encryption/decryption round trip
test_plain = "btcseed"
encrypted = bifid_encrypt(test_plain, test_square)
decrypted = bifid_decrypt(encrypted, test_square)
print(f"Original: {test_plain}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
print(f"Round trip success: {test_plain == decrypted}")

# Now try to decrypt the faed block
print("\n" + "=" * 70)
print("DECRYPTING FAED BLOCK")
print("=" * 70)

with open('faed_block.txt', 'r') as f:
    faed_block = f.read().strip()

print(f"Input length: {len(faed_block)}")

# Try different square arrangements
keyword = "dbifhceg"
square = create_polybius_square_3x3(keyword)
print(f"\nKeyword: {keyword}")
print(f"Square: {square}")
print("Grid:")
for i in range(3):
    print(f"  {square[i*3:(i+1)*3]}")

result = bifid_decrypt(faed_block, square)
print(f"\nDecrypted length: {len(result)}")
print(f"First 30 chars: {result[:30]}")
print(f"Last 30 chars: {result[-30:]}")
print(f"Starts with 'btcseed': {result.startswith('btcseed')}")

# Try encrypting "btcseed" to see what pattern it produces
btcseed_encrypted = bifid_encrypt("btcseed", square)
print(f"\n'btcseed' encrypts to: {btcseed_encrypted}")
print(f"Does faed start with this? {faed_block.startswith(btcseed_encrypted)}")

# Check if the first 7 chars of faed decrypt to btcseed
first_7_decrypted = bifid_decrypt(faed_block[:7], square)
print(f"First 7 chars of faed decrypt to: {first_7_decrypted}")

# Try different interpretations
print("\n" + "=" * 70)
print("TRYING DIFFERENT APPROACHES")
print("=" * 70)

# Maybe the keyword defines the square differently
# Standard order: fill with keyword, then remaining alphabet
keywords_to_try = [
    "dbifhceg",
    "dbifhcega",  # 9 letters
    "abcdefghi",  # standard alphabet
    "matrixsum",  # from hint "matrixsumlist"
]

for kw in keywords_to_try:
    sq = create_polybius_square_3x3(kw)
    res = bifid_decrypt(faed_block, sq)
    print(f"\nKeyword '{kw}' -> Square '{sq}'")
    print(f"  Result starts: {res[:20]}")
    print(f"  Starts with 'btcseed': {res.startswith('btcseed')}")
    
    # Also try encrypting btcseed
    enc = bifid_encrypt("btcseed", sq)
    print(f"  'btcseed' encrypts to: {enc}")

# What if we need to find what encrypts to "faedgge..."?
# Let's try to find a plaintext that starts with "btcseed"
print("\n" + "=" * 70)
print("SEARCHING FOR CORRECT SQUARE")
print("=" * 70)

import itertools

# Try all permutations of 'dbifhceg' + 'a'
base_letters = "dbifhcega"

# That's 9! = 362880 permutations - too many
# Let's try a smarter approach

# The hint says keyword is "dbifhceg" - 8 letters
# For a 9-letter alphabet, we need 9 letters in the square
# The missing letter is 'a'

# Try placing 'a' at different positions
for pos in range(9):
    sq = base_letters[:pos] + 'a' + base_letters[pos:8]
    sq = sq[:9]  # ensure 9 chars
    if len(set(sq)) != 9:
        continue
    res = bifid_decrypt(faed_block, sq)
    if res.startswith('btc') or 'seed' in res[:10]:
        print(f"Position {pos}: Square '{sq}' -> '{res[:20]}'")
