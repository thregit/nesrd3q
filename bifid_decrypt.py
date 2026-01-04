#!/usr/bin/env python3
"""
Bifid Cipher Decryption for NESRD3Q Puzzle
Keyword: dbifhceg
Input: 570-character faed block
Expected output: btcseed + 563 characters
"""

def create_polybius_square(keyword):
    """
    Create a Polybius square from a keyword.
    For a 9-letter alphabet (a-i), we use a 3x3 grid.
    """
    # The alphabet is a-i (9 letters)
    alphabet = 'abcdefghi'
    
    # Build the square: keyword letters first, then remaining letters
    square = []
    seen = set()
    
    # Add keyword letters
    for char in keyword.lower():
        if char in alphabet and char not in seen:
            square.append(char)
            seen.add(char)
    
    # Add remaining letters
    for char in alphabet:
        if char not in seen:
            square.append(char)
            seen.add(char)
    
    return ''.join(square)

def get_coordinates(char, square, size=3):
    """Get row, col coordinates for a character in the square."""
    idx = square.index(char)
    return idx // size, idx % size

def get_char(row, col, square, size=3):
    """Get character at row, col in the square."""
    return square[row * size + col]

def bifid_decrypt(ciphertext, keyword, size=3):
    """
    Decrypt using Bifid cipher.
    
    For decryption:
    1. Convert each ciphertext letter to row,col coordinates
    2. Split the coordinate sequence in half
    3. Interleave the two halves
    4. Convert back to letters
    """
    square = create_polybius_square(keyword)
    print(f"Polybius square: {square}")
    print(f"Grid layout:")
    for i in range(size):
        print(f"  {square[i*size:(i+1)*size]}")
    
    # Get coordinates for each character
    rows = []
    cols = []
    for char in ciphertext.lower():
        if char in square:
            r, c = get_coordinates(char, square, size)
            rows.append(r)
            cols.append(c)
    
    # Combine rows and cols
    all_coords = rows + cols
    
    # For decryption, we need to reverse the process
    # The ciphertext was created by:
    # 1. Getting plaintext coordinates
    # 2. Splitting into first half (rows) and second half (cols)
    # 3. Pairing them up to get ciphertext
    
    # So to decrypt, we need to:
    # 1. Get ciphertext coordinates
    # 2. Take pairs (row[i], col[i]) as the split coordinates
    # 3. Reconstruct the original sequence
    
    # Actually, for Bifid decryption:
    # The coordinates are interleaved differently
    
    n = len(ciphertext)
    
    # Method 1: Standard Bifid decryption
    # Ciphertext coordinates: (r0,c0), (r1,c1), ...
    # These represent: first half = r0,r1,r2... second half = c0,c1,c2...
    # Plaintext coords come from pairing: (r0,c0), (r1,c1) but from the split
    
    # Let me implement proper Bifid decryption
    plaintext = []
    
    # Get all coordinates as pairs
    coords = []
    for char in ciphertext.lower():
        if char in square:
            r, c = get_coordinates(char, square, size)
            coords.append((r, c))
    
    # Split into rows and cols
    all_rows = [c[0] for c in coords]
    all_cols = [c[1] for c in coords]
    
    # Interleave to get plaintext coordinates
    combined = all_rows + all_cols
    
    # Take pairs
    for i in range(0, len(combined), 2):
        if i + 1 < len(combined):
            r = combined[i]
            c = combined[i + 1]
            plaintext.append(get_char(r, c, square, size))
    
    return ''.join(plaintext)

def bifid_decrypt_v2(ciphertext, keyword, size=3):
    """
    Alternative Bifid decryption implementation.
    """
    square = create_polybius_square(keyword)
    
    # Get coordinates
    coords = []
    for char in ciphertext.lower():
        if char in square:
            r, c = get_coordinates(char, square, size)
            coords.append((r, c))
    
    n = len(coords)
    
    # Extract rows and cols
    rows = [c[0] for c in coords]
    cols = [c[1] for c in coords]
    
    # Combine: rows first, then cols
    combined = rows + cols
    
    # Pair up to get plaintext coordinates
    plaintext = []
    for i in range(n):
        r = combined[i]
        c = combined[i + n]
        plaintext.append(get_char(r, c, square, size))
    
    return ''.join(plaintext)

# Read the faed block
with open('faed_block.txt', 'r') as f:
    faed_block = f.read().strip()

print("=" * 70)
print("BIFID CIPHER DECRYPTION")
print("=" * 70)
print(f"\nInput length: {len(faed_block)}")
print(f"Input (first 50): {faed_block[:50]}")
print(f"Keyword: dbifhceg")

# Try decryption
keyword = "dbifhceg"

print("\n--- Method 1 ---")
result1 = bifid_decrypt(faed_block, keyword)
print(f"Result length: {len(result1)}")
print(f"First 20 chars: {result1[:20]}")
print(f"Last 20 chars: {result1[-20:]}")
print(f"Starts with 'btcseed': {result1.startswith('btcseed')}")

print("\n--- Method 2 ---")
result2 = bifid_decrypt_v2(faed_block, keyword)
print(f"Result length: {len(result2)}")
print(f"First 20 chars: {result2[:20]}")
print(f"Last 20 chars: {result2[-20:]}")
print(f"Starts with 'btcseed': {result2.startswith('btcseed')}")

# Save results
with open('bifid_result.txt', 'w') as f:
    f.write(f"Method 1: {result1}\n")
    f.write(f"Method 2: {result2}\n")

# Try different keyword variations
print("\n--- Trying keyword variations ---")
keywords_to_try = [
    "dbifhceg",
    "DBIFHCEG", 
    "dbifhcega",  # with 'a' added
    "adbifhceg",  # 'a' prepended
]

for kw in keywords_to_try:
    try:
        r = bifid_decrypt_v2(faed_block, kw)
        print(f"Keyword '{kw}': starts with '{r[:10]}', ends with '{r[-10:]}'")
    except Exception as e:
        print(f"Keyword '{kw}': Error - {e}")
