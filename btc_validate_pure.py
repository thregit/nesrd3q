#!/usr/bin/env python3
"""
Bitcoin Private Key Validation - Pure Python Implementation
Uses hashlib with fallback for RIPEMD160
"""

import hashlib
import struct

# Pure Python RIPEMD-160 implementation
def ripemd160(message):
    """Pure Python RIPEMD-160 implementation."""
    # Try hashlib first
    try:
        h = hashlib.new('ripemd160')
        h.update(message)
        return h.digest()
    except ValueError:
        pass
    
    # Pure Python fallback
    def f(j, x, y, z):
        if j < 16:
            return x ^ y ^ z
        elif j < 32:
            return (x & y) | (~x & z)
        elif j < 48:
            return (x | ~y) ^ z
        elif j < 64:
            return (x & z) | (y & ~z)
        else:
            return x ^ (y | ~z)
    
    def K(j):
        if j < 16:
            return 0x00000000
        elif j < 32:
            return 0x5A827999
        elif j < 48:
            return 0x6ED9EBA1
        elif j < 64:
            return 0x8F1BBCDC
        else:
            return 0xA953FD4E
    
    def Kp(j):
        if j < 16:
            return 0x50A28BE6
        elif j < 32:
            return 0x5C4DD124
        elif j < 48:
            return 0x6D703EF3
        elif j < 64:
            return 0x7A6D76E9
        else:
            return 0x00000000
    
    def rol(x, n):
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    
    r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
         7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
         3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
         1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
         4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
    
    rp = [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
          6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
          15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
          8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
          12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
    
    s = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
         7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
         11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
         11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
         9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
    
    sp = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
          9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
          9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
          15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
          8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
    
    # Padding
    msg = bytearray(message)
    msg_len = len(message)
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0x00)
    msg += struct.pack('<Q', msg_len * 8)
    
    # Initial hash values
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    # Process each 64-byte block
    for i in range(0, len(msg), 64):
        block = msg[i:i+64]
        X = struct.unpack('<16I', block)
        
        A, B, C, D, E = h0, h1, h2, h3, h4
        Ap, Bp, Cp, Dp, Ep = h0, h1, h2, h3, h4
        
        for j in range(80):
            T = (A + f(j, B, C, D) + X[r[j]] + K(j)) & 0xFFFFFFFF
            T = (rol(T, s[j]) + E) & 0xFFFFFFFF
            A = E
            E = D
            D = rol(C, 10)
            C = B
            B = T
            
            T = (Ap + f(79-j, Bp, Cp, Dp) + X[rp[j]] + Kp(j)) & 0xFFFFFFFF
            T = (rol(T, sp[j]) + Ep) & 0xFFFFFFFF
            Ap = Ep
            Ep = Dp
            Dp = rol(Cp, 10)
            Cp = Bp
            Bp = T
        
        T = (h1 + C + Dp) & 0xFFFFFFFF
        h1 = (h2 + D + Ep) & 0xFFFFFFFF
        h2 = (h3 + E + Ap) & 0xFFFFFFFF
        h3 = (h4 + A + Bp) & 0xFFFFFFFF
        h4 = (h0 + B + Cp) & 0xFFFFFFFF
        h0 = T
    
    return struct.pack('<5I', h0, h1, h2, h3, h4)

def base58_encode(data):
    """Base58 encode bytes."""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    num = int.from_bytes(data, 'big')
    result = ''
    while num > 0:
        num, rem = divmod(num, 58)
        result = alphabet[rem] + result
    
    return '1' * leading_zeros + result

def point_add(p1, p2, p):
    """Add two points on secp256k1 curve."""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2 and y1 != y2:
        return None
    
    if x1 == x2:
        m = (3 * x1 * x1) * pow(2 * y1, -1, p) % p
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p
    
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    
    return (x3, y3)

def scalar_mult(k, point, p):
    """Multiply point by scalar on secp256k1."""
    result = None
    addend = point
    
    while k:
        if k & 1:
            result = point_add(result, addend, p)
        addend = point_add(addend, addend, p)
        k >>= 1
    
    return result

def private_key_to_address(private_key_hex):
    """Convert hex private key to Bitcoin address."""
    # secp256k1 parameters
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    G = (Gx, Gy)
    
    # Convert private key to integer
    private_key = int(private_key_hex, 16)
    
    # Generate public key point
    public_point = scalar_mult(private_key, G, p)
    
    if public_point is None:
        return [('error', 'Invalid private key')]
    
    x, y = public_point
    
    # Uncompressed public key
    public_key_uncompressed = b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
    
    # Compressed public key
    prefix = b'\x02' if y % 2 == 0 else b'\x03'
    public_key_compressed = prefix + x.to_bytes(32, 'big')
    
    addresses = []
    
    for pk_type, public_key in [('uncompressed', public_key_uncompressed),
                                 ('compressed', public_key_compressed)]:
        # SHA256
        sha256_hash = hashlib.sha256(public_key).digest()
        
        # RIPEMD160
        hash160 = ripemd160(sha256_hash)
        
        # Add version byte
        versioned = b'\x00' + hash160
        
        # Checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        
        # Encode
        address = base58_encode(versioned + checksum)
        addresses.append((pk_type, address))
    
    return addresses

# Target address
TARGET = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# Candidate keys
candidates = {
    "OTP mod16": "72fa661d07369634dd5cf01305f007c98b9146413d78342a4e172133ce1cbc06",
    "OTP direct": "7cfa66bda7d696d4dd5cfab3affaa7c98b9b46e1dd78de2a4eb7cbddcebcbc06",
    "FAED hex": "faedeedfcbdabcadcfeddfdbaaedafaeccdaeabacefbfefafabfaaeeacbbeafe",
    "XOR result": "22b900593217a623ab3ef33646c654a8e3f14277557d300c387511b4891bac7e",
    "OTP V1": "7c9460b7a7d030d477569ab3af9aa763859b46e1d778de2448b7cbdd68b65606",
}

print("=" * 70)
print("BITCOIN ADDRESS VALIDATION")
print("=" * 70)
print(f"Target: {TARGET}\n")

for name, key in candidates.items():
    print(f"\n{name}:")
    print(f"  Key: {key}")
    
    addresses = private_key_to_address(key)
    for pk_type, addr in addresses:
        match = "✓ MATCH!" if addr == TARGET else ""
        print(f"  {pk_type}: {addr} {match}")

# Try variations
print("\n" + "=" * 70)
print("TRYING VARIATIONS")
print("=" * 70)

# Reverse keys
for name, key in list(candidates.items())[:3]:
    reversed_key = key[::-1]
    print(f"\n{name} (reversed): {reversed_key[:32]}...")
    addresses = private_key_to_address(reversed_key)
    for pk_type, addr in addresses:
        match = "✓ MATCH!" if addr == TARGET else ""
        if match:
            print(f"  {pk_type}: {addr} {match}")

# Byte-swap
for name, key in list(candidates.items())[:3]:
    pairs = [key[i:i+2] for i in range(0, 64, 2)]
    swapped = ''.join(reversed(pairs))
    print(f"\n{name} (byte-swapped): {swapped[:32]}...")
    addresses = private_key_to_address(swapped)
    for pk_type, addr in addresses:
        match = "✓ MATCH!" if addr == TARGET else ""
        if match:
            print(f"  {pk_type}: {addr} {match}")
