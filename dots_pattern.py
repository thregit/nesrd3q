#!/usr/bin/env python3
"""
Parse and analyze the dots pattern from January 4, 2026
Convert to 14x14 matrix and analyze positions
"""

# The dots pattern from the puzzle
dots_raw = """. . . . . . 0 1 . . . . . . . . . . . 1 . . . . . 0 0 . . . . . . . . . 0 0 . . . . . . . . . 0 1 . . . . . . . . . . 1 . . . . . . 0 0 . . . . . . . . . 0 0 . . 0 0 . . . . . . 1 . . . . . . 0 0 . . 1 . . . . 0 . . . . . 0 . . . . 0 . 0 0 . . . . . . . . 1 . 0 . . . . . . . . . . . . 1 . . . . . 0 0 . . . . . . 0 1 . . . . 0 0 . . . . . . 0 0 1 . . . . . 0 0 . . . . . 0 . . . . . . 0 0 ."""

# Parse the pattern
elements = dots_raw.split()
print(f"Total elements: {len(elements)}")

# Convert to 14x14 matrix
matrix = []
for i in range(0, len(elements), 14):
    row = elements[i:i+14]
    matrix.append(row)

print("\n14x14 Matrix:")
print("-" * 50)
for i, row in enumerate(matrix):
    print(f"Row {i:2d}: {' '.join(row)}")

# Analyze positions
print("\n" + "=" * 70)
print("POSITION ANALYSIS")
print("=" * 70)

# Find positions of 0s, 1s, and dots
pos_0 = []
pos_1 = []
pos_dot = []

for i, elem in enumerate(elements):
    if elem == '0':
        pos_0.append(i)
    elif elem == '1':
        pos_1.append(i)
    else:
        pos_dot.append(i)

print(f"\nPositions of '0' ({len(pos_0)} total): {pos_0}")
print(f"\nPositions of '1' ({len(pos_1)} total): {pos_1}")
print(f"\nPositions of '.' ({len(pos_dot)} total): {len(pos_dot)} positions")

# Convert to row,col format
print("\n" + "=" * 70)
print("COORDINATE ANALYSIS")
print("=" * 70)

def idx_to_coord(idx):
    return (idx // 14, idx % 14)

print("\n'1' positions as (row, col):")
for idx in pos_1:
    r, c = idx_to_coord(idx)
    print(f"  Index {idx:3d} -> ({r:2d}, {c:2d})")

print("\n'0' positions as (row, col):")
for idx in pos_0:
    r, c = idx_to_coord(idx)
    print(f"  Index {idx:3d} -> ({r:2d}, {c:2d})")

# Create a visual representation
print("\n" + "=" * 70)
print("VISUAL MATRIX (0=0, 1=1, .=space)")
print("=" * 70)

for i, row in enumerate(matrix):
    visual = ''.join(c if c in '01' else ' ' for c in row)
    print(f"{i:2d}: |{visual}|")

# Count totals
print(f"\nTotal '0's: {len(pos_0)}")
print(f"Total '1's: {len(pos_1)}")
print(f"Total '.'s: {len(pos_dot)}")
print(f"Sum: {len(pos_0) + len(pos_1) + len(pos_dot)}")

# Save the pattern data
with open('dots_positions.txt', 'w') as f:
    f.write(f"0 positions: {pos_0}\n")
    f.write(f"1 positions: {pos_1}\n")
    f.write(f"dot positions: {pos_dot}\n")

# Create binary representation
print("\n" + "=" * 70)
print("BINARY INTERPRETATION")
print("=" * 70)

# Convert to binary: 0=0, 1=1, .=?
# Try different interpretations

# Interpretation 1: Only 0s and 1s matter
binary_01 = ''.join(elem if elem in '01' else '' for elem in elements)
print(f"\nOnly 0s and 1s: {binary_01}")
print(f"Length: {len(binary_01)}")

# Interpretation 2: .=0, 0=0, 1=1
binary_dot0 = ''.join('0' if elem in '.0' else '1' for elem in elements)
print(f"\n.=0, 0=0, 1=1: {binary_dot0[:50]}...")
print(f"Length: {len(binary_dot0)}")

# Interpretation 3: .=1, 0=0, 1=1
binary_dot1 = ''.join('1' if elem == '.' else elem for elem in elements)
print(f"\n.=1, 0=0, 1=1: {binary_dot1[:50]}...")
print(f"Length: {len(binary_dot1)}")

# The pattern has 196 elements (14x14)
# 64 hex chars = 256 bits, but we only have 196 positions
# Maybe the pattern is used as a mask

print("\n" + "=" * 70)
print("MASK APPLICATION")
print("=" * 70)

# Load the decoded data
otp_64 = "XCPKWGBNAXDGJGDUNNVMPABTAFPAAXMJYLZBUWERDNXYDESKUOBXCBDDMOBMLMQW"

print(f"\nOTP 64-char result: {otp_64}")
print(f"Length: {len(otp_64)}")

# Try using positions of 1s to extract characters
extracted_1s = ''.join(otp_64[i] for i in pos_1 if i < len(otp_64))
print(f"\nChars at '1' positions from OTP: {extracted_1s}")

# Try using positions of 0s
extracted_0s = ''.join(otp_64[i] for i in pos_0 if i < len(otp_64))
print(f"Chars at '0' positions from OTP: {extracted_0s}")

# The faed block is 570 chars - let's see if the pattern applies there
with open('faed_block.txt', 'r') as f:
    faed_block = f.read().strip()

# Extract chars at 1 positions from faed
extracted_faed_1s = ''.join(faed_block[i] for i in pos_1 if i < len(faed_block))
print(f"\nChars at '1' positions from FAED: {extracted_faed_1s}")

# Extract chars at 0 positions from faed
extracted_faed_0s = ''.join(faed_block[i] for i in pos_0 if i < len(faed_block))
print(f"Chars at '0' positions from FAED: {extracted_faed_0s}")
