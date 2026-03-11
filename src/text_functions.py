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
        pattern=fr'({re.escape(delimiter)}.*?{re.escape(delimiter)})',
        make_node=lambda m: TextNode(m.group(1), text_type),  # group(1) = full match with delimiters
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
    print(lst)
    by_link = split_nodes_link(lst)
    print(by_link)
    by_image_link = split_nodes_image(by_link)
    print(by_image_link)
    by_image_link_bold = split_nodes_delimiter(by_image_link, "**", TextType.BOLD)
    print(by_image_link_bold)
    by_image_link_bold_italic = split_nodes_delimiter(by_image_link_bold, "_", TextType.ITALIC)
    print(by_image_link_bold_italic)
    by_image_link_bold_italic_code = split_nodes_delimiter(by_image_link_bold_italic, "`", TextType.CODE)
    return by_image_link_bold_italic_code


def extract_markdown_images(text):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)


def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text)


def raw_to_html_paragraph(text):
    return f"<p>{text}</p>"

def raw_to_html_heading(text, level):
    if level < 1 or level > 6:
        raise ValueError('Heading level must be between 1 and 6')
    return f'<h{level}>text</h{level}>'

def raw_to_html_bold(text):
    return f'<b>{text}</b>'

def raw_to_html_italic(text).
    return f'<i>{text}</i>'

def raw_to_html_link(text, link):
    return f'<a href="{link}">{text}</a>'

def raw_to_html_image(text, link):
    return f'<img src="{link}" alt="{text}" />'

def raw_to_html_unordered_list(text_lines):
    return f'<ul>\n{"".join('<li>' + text + '</li>\n' for text in text_lines)}</ul>'

def raw_to_html_ordered_list(text_lines):
    return f'<ol>\n{"".join('<li>' + text + '</li>\n' for text in text_lines)}</ol>'

def raw_to_html_quote(text_lines):
    return f'<blockquote>{"".join('<p>' + text + '</p>\n' for text in text_lines)}</blockquote>'
    
def raw_to_html_code(text_lines):
    return f'<pre><code>{"".join(text + '\n' for text in text_lines)}</code></pre>'
