from blocktype import BlockType
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextType
from text_functions import text_to_textnodes, extract_title
import os
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.INFO)


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split('\n\n')]

def block_to_block_type(block):
    if re.match(r'^#{1} ', block):
        return BlockType.HEADING_FIRST
    if re.match(r'^#{2} ', block):
        return BlockType.HEADING_SECOND
    if re.match(r'^#{3} ', block):
        return BlockType.HEADING_THIRD
    if re.match(r'^#{4} ', block):
        return BlockType.HEADING_FOURTH
    if re.match(r'^#{5} ', block):
        return BlockType.HEADING_FIFTH
    if re.match(r'^#{6} ', block):
        return BlockType.HEADING_SIXTH
    if re.match(r'`{3}\n(.*?)`{3}', block, re.DOTALL):
        return BlockType.MULTILINE_CODE
    lines = block.split("\n")
    if all(re.match(r'> ?', line) for line in lines):
        return BlockType.QUOTE
    if all(re.match(r'[-+*] ', line) for line in lines):
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


def unordered_list_to_children(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        text = re.sub(r"^- ", "", line)
        li_children = text_to_children(text)
        children.append(ParentNode(BlockType.LIST_ITEM, li_children))
    return children


def ordered_list_to_children(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        text = re.sub(r"^\d+\. ", "", line)
        li_children = text_to_children(text)
        children.append(ParentNode(BlockType.LIST_ITEM, li_children))
    return children


def quote_to_children(block):
    children = []
    lines = block.split("\n")
    cleaned = [re.sub(r'^> ?', '', line) for line in lines]
    text = "\n".join(cleaned)
    return text_to_children(text)


def multiline_code_to_child(block):
    inner = re.sub(r'^```\n?', '', block)
    inner = re.sub(r'\n?```$', '', inner)
    return LeafNode(TextType.TEXT, inner + '\n')


def markdown_to_html_node(markdown):
    subparents = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        children = []
        if block_type == BlockType.UNORDERED_LIST:
            children = unordered_list_to_children(block)
        elif block_type == BlockType.ORDERED_LIST:
            children = ordered_list_to_children(block)
        elif block_type == BlockType.QUOTE:
            children = quote_to_children(block)
        elif block_type == BlockType.MULTILINE_CODE:
            children.append(multiline_code_to_child(block))
        else:
            children = text_to_children(block)
        parentnode = ParentNode(block_type, children)
        subparents.append(parentnode)
    return ParentNode(BlockType.DIV, subparents)


def generate_page(from_path, template_path, dest_path):
    logger.info(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    html_node = markdown_to_html_node(md)
    try:
        html_string = html_node.to_html()
    except Exception as e:
        logger.error(e)
    title = extract_title(md)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html_string)
    dest_parent_path = os.path.dirname(dest_path)
    if not os.path.exists(dest_parent_path) or not os.path.isdir(dest_parent_path):
        os.makedirs(dest_parent_path)
    with open(dest_path, 'w') as f:
        f.write(template)
        
        
def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    pass