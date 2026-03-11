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
