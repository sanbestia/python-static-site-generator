from textnode import TextNode, TextType
from htmlnode import HTMLNode
import re


def text_node_to_html_node(text_node):
    pass



def _split_nodes(old_nodes, pattern, make_node):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        prev_end = 0
        for m in re.finditer(pattern, text):
            if m.start() > prev_end:
                new_nodes.append(TextNode(text[prev_end:m.start()], TextType.TEXT))
            new_nodes.append(make_node(m))
            prev_end = m.end()
        if prev_end < len(text):
            new_nodes.append(TextNode(text[prev_end:], TextType.TEXT))
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type not in (TextType.BOLD, TextType.ITALIC, TextType.CODE):
        raise ValueError('Error: Invalid text type')
    return _split_nodes(
        old_nodes,
        pattern=fr'{re.escape(delimiter)}(.*?){re.escape(delimiter)}',
        make_node=lambda m: TextNode(m.group(1), text_type),
    )


def split_nodes_image(old_nodes):
    return _split_nodes(
        old_nodes,
        pattern=r'!\[(.*?)\]\((.*?)\)',
        make_node=lambda m: TextNode(text=m.group(1), text_type=TextType.IMAGE, url=m.group(2)),
    )


def split_nodes_link(old_nodes):
    return _split_nodes(
        old_nodes,
        pattern=r'(?<!!)\[(.*?)\]\((.*?)\)',
        make_node=lambda m: TextNode(text=m.group(1), text_type=TextType.LINK, url=m.group(2)),
    )
 
 
def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    lst = [text_node]
    by_link = split_nodes_link(lst)
    by_image_link = split_nodes_image(by_link)
    by_image_link_bold = split_nodes_delimiter(by_image_link, "**", TextType.BOLD)
    by_image_link_bold_italic = split_nodes_delimiter(by_image_link_bold, "_", TextType.ITALIC)
    by_image_link_bold_italic_code = split_nodes_delimiter(by_image_link_bold_italic, "`", TextType.CODE)
    return by_image_link_bold_italic_code


def extract_markdown_images(text):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)


def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)

