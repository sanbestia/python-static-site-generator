from blocktype import BlockType
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextType
from text_functions import text_to_textnodes
import re


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split('\n\n')]

def block_to_block_type(block):
    if re.match(r'#{1} ', block):
        return BlockType.HEADING_FIRST
    if re.match(r'#{2} ', block):
        return BlockType.HEADING_SECOND
    if re.match(r'#{3} ', block):
        return BlockType.HEADING_THIRD
    if re.match(r'#{4} ', block):
        return BlockType.HEADING_FOURTH
    if re.match(r'#{5} ', block):
        return BlockType.HEADING_FIFTH
    if re.match(r'#{6} ', block):
        return BlockType.HEADING_SIXTH
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


def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = []
    for textnode in textnodes:
        text_type = textnode.text_type
        text = textnode.text
        url = textnode.url
        props = {}
        if url is not None:
            if text_type == TextType.LINK:
                props['href'] = url
            if text_type == TextType.IMAGE:
                props['src'] = url
        children.append(LeafNode(text_type, text, props))
    return children



def markdown_to_html_node(markdown):
    subparents = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        textnodes = text_to_textnodes(block)
        children = []
        if block_type == BlockType.MULTILINE_CODE:
            inner = re.sub(r'^```\n?', '', block)
            inner = re.sub(r'\n?```$', '', inner)
            children = [LeafNode(TextType.TEXT, inner + '\n')]
        else:
            children = text_to_children(block)
        parentnode = ParentNode(block_type, children)
        subparents.append(parentnode)
    return ParentNode(BlockType.DIV, subparents)


