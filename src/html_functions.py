from blocktype import BlockType
import re


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split('\n\n')]

def block_to_block_type(block):
    if re.match(r'#{1,6} ', block):
        return BlockType.HEADING
    if re.match(r'`{3}\n(.*?)`{3}', block, re.DOTALL):
        return BlockType.MULTILINE_CODE
    lines = block.split("\n")
    if all(re.match(r'> ?', line) for line in lines):
        return BlockType.QUOTE
    if all(re.match(r'- ', line) for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(fr'{pos + 1}. ', line) for pos, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
    

examples = [
    # --- HEADING ---
    '# Heading',
    '## Another heading',
    '### Another nother heading',
    '###### Max level heading',
    '####### Too many hashes (bad)',
    '#No space heading (bad)',
    'a # Trailing char heading (bad)',

    # --- MULTILINE CODE ---
    '```\nThis is code\n```',
    '```\nThis is also code```',
    '```\nThis is code\nand more code\n```',
    '```This is not code\n```',
    '```\n```',                             # Empty code block
    '```\nline1\nline2\nline3\n```',         # Multi-line code block

# --- QUOTE ---
    '>single line quote',                        # Valid, no space
    '> single line quote with space',            # Valid, space after >
    '>line one\n>line two\n>line three',         # Valid multi-line, no spaces
    '> line one\n> line two\n> line three',      # Valid multi-line, with spaces
    '>line one\n> line two\n>line three',        # Valid multi-line, mixed spacing
    'no arrow (bad)',                            # Bad, no > at all
    '>line one\nline two (bad)',                 # Bad, second line missing >
    '>line one\n >indented arrow (bad)',         # Bad, space BEFORE >

    # --- UNORDERED LIST ---
    '- item one',
    '- item one\n- item two\n- item three',
    '- item one\n- item two\nbad item',     # Missing dash on last line
    '-no space (bad)',
    '- item\n -indented dash (bad)',

    # --- ORDERED LIST ---
    '1. First item',
    '1. First\n2. Second\n3. Third',
    '1. First\n2. Second\n4. Fourth',       # Skipped number (bad)
    '0. Starts at zero (bad)',
    '1. First\n2. Second\nbad item',        # Missing number on last line
    '1.No space (bad)',
    '1. First\n3. Skipped two (bad)',

    # --- PARAGRAPH (fallback) ---
    'Just a plain paragraph.',
    'Two lines\nof a paragraph',
    '',                                     # Empty string
    'Mixed # heading and > quote',
]

for ex in examples:
    print(f"result: {block_to_block_type(ex):<25} block: {repr(ex)}")