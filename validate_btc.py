#!/usr/bin/env python3
"""
Bitcoin Private Key Validation
Generate Bitcoin address from private key and compare to target
"""

import hashlib
import ecdsa

def private_key_to_address(private_key_hex):
    """Convert a hex private key to a Bitcoin address."""
    try:
        # Convert hex to bytes
        private_key_bytes = bytes.fromhex(private_key_hex)
        
        # Generate public key using ECDSA secp256k1
        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        
        # Uncompressed public key (04 + x + y)
        public_key_uncompressed = b'\x04' + vk.to_string()
        
        # Also try compressed public key
        x = vk.to_string()[:32]
        y = vk.to_string()[32:]
        if y[-1] % 2 == 0:
            public_key_compressed = b'\x02' + x
        else:
            public_key_compressed = b'\x03' + x
        
        addresses = []
        
        for pk_type, public_key in [('uncompressed', public_key_uncompressed), 
                                     ('compressed', public_key_compressed)]:
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
            
            # Combine
            address_bytes = versioned + checksum
            
            # Base58 encode
            address = base58_encode(address_bytes)
            addresses.append((pk_type, address))
        
        return addresses
    except Exception as e:
        return [('error', str(e))]

def base58_encode(data):
    """Base58 encode bytes."""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    # Count leading zeros
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    # Convert to integer
    num = int.from_bytes(data, 'big')
    
    # Encode
    result = ''
    while num > 0:
        num, rem = divmod(num, 58)
        result = alphabet[rem] + result
    
    # Add leading 1s
    return '1' * leading_zeros + result

# Target address
TARGET = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# Candidate keys from various approaches
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

# Also try some variations
print("\n" + "=" * 70)
print("TRYING VARIATIONS")
print("=" * 70)

# Try reversing the keys
for name, key in list(candidates.items())[:3]:
    reversed_key = key[::-1]
    if len(reversed_key) == 64:
        print(f"\n{name} (reversed):")
        print(f"  Key: {reversed_key}")
        addresses = private_key_to_address(reversed_key)
        for pk_type, addr in addresses:
            match = "✓ MATCH!" if addr == TARGET else ""
            print(f"  {pk_type}: {addr} {match}")

# Try byte-swapping (reverse pairs)
for name, key in list(candidates.items())[:3]:
    pairs = [key[i:i+2] for i in range(0, 64, 2)]
    swapped = ''.join(reversed(pairs))
    print(f"\n{name} (byte-swapped):")
    print(f"  Key: {swapped}")
    addresses = private_key_to_address(swapped)
    for pk_type, addr in addresses:
        match = "✓ MATCH!" if addr == TARGET else ""
        print(f"  {pk_type}: {addr} {match}")
