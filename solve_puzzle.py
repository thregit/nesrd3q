#!/usr/bin/env python3
"""
NESRD3Q Bitcoin Puzzle Solver
Extracts and processes the dbbi and faed blocks from salphaseion
"""

# The raw data from salphaseion.ipynb
# Combined block: first 91 chars are "dbbi" block, remaining 570 chars are "faed" block

dbbi_raw = """d b b i b f b h c c b e g b i h a b e b e i h b e g g e g e b e b b g e h h e b h h f b a b f d h b e f f c d b b f c c c g b f b e e g g e c b e d c i b f b f f g i g b e e e a b e"""

faed_raw = """f a e d g g e e d f c b d a b h h g g c a d c f e d d g f d g b g i g a a e d g g i a f a e c g h g g c d a i h e h a h b a h i g c e i f g b f g e f g a i f a b i f a g a e g e a c g b b e a g f g g e e g g a f b a c g f c d b e i f f a a f c i d a h g d e e f g h h c g g a e g d e b h h e g e g h c e g a d f b d i a g e f c i c g g i f d c g a a g g f b i g a i c f b h e c a e c b c e i a i c e b g b g i e c d e g g f g e g a e d g g f i i c i i i f i f h g g c g f g d c d g g e f c b e e i g e f i b g i b g g g h h f b c g i f d e h e d f d a g i c d b h i c g a i e d a e h a h g h h c i h d g h f h b i i c e c b i i c h i h i i i g i d d g e h h d f d c h c b a f g f b h a h e a g e g e c a f e h g c f g g g g c a g f h h g h b a i h i d i e h h f d e g g d g c i h g g g g g h a d a h i g i g b g e c g e d f c d g g a c c d e h i i c i g f b f f h g g a e i d b b e i b b e i i f d g f d h i e e e i e e e c i f d g d a h d i g g f h e g f i a f f i g g b c b c e h c e a b f b e d b i i b f b f d e d e e h g i g f a a i g g a g b e i i c h i e d i f b e h g b c c a h h b i i b i b b i b d c b a h a i d h f a h i i h i c"""

# Clean the blocks (remove spaces)
dbbi_block = dbbi_raw.replace(' ', '')
faed_block = faed_raw.replace(' ', '')

print("=" * 70)
print("BLOCK EXTRACTION")
print("=" * 70)
print(f"\nDBBI block length: {len(dbbi_block)}")
print(f"FAED block length: {len(faed_block)}")
print(f"Combined length: {len(dbbi_block) + len(faed_block)}")
print(f"\nDBBI block (first 91 chars):\n{dbbi_block}")
print(f"\nFAED block (570 chars):\n{faed_block[:100]}...")
print(f"...{faed_block[-50:]}")

# Verify character sets
dbbi_chars = set(dbbi_block)
faed_chars = set(faed_block)
print(f"\nDBBI unique chars: {sorted(dbbi_chars)}")
print(f"FAED unique chars: {sorted(faed_chars)}")

# Save to files for further processing
with open('dbbi_block.txt', 'w') as f:
    f.write(dbbi_block)
    
with open('faed_block.txt', 'w') as f:
    f.write(faed_block)

print("\nBlocks saved to dbbi_block.txt and faed_block.txt")
