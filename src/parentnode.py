from htmlnode import HTMLNode
from leafnode import LeafNode
from blocktype import BlockType
from raw_to_html_functions import *


class ParentNode(HTMLNode):
    def __init__(self, tag: BlockType, children, props=None):
        if not isinstance(tag, BlockType):
            raise ValueError('ParentNode tag must be BlockType')
        super().__init__(tag, None, children, props)
        
    
    def to_html(self):
        if self.tag is None:
            raise ValueError('All parent nodes must have a tag')
        if self.children is None:
            raise ValueError('All parent nodes must have children')
        parsed_children = "".join(child.to_html() for child in self.children)
        match self.tag:
            case BlockType.HEADING_FIRST:
                return raw_to_html_heading(parsed_children, 1)
            case BlockType.HEADING_SECOND:
                return raw_to_html_heading(parsed_children, 2)
            case BlockType.HEADING_THIRD:
                return raw_to_html_heading(parsed_children, 3)
            case BlockType.HEADING_FOURTH:
                return raw_to_html_heading(parsed_children, 4)
            case BlockType.HEADING_FIFTH:
                return raw_to_html_heading(parsed_children, 5)
            case BlockType.HEADING_SIXTH:
                return raw_to_html_heading(parsed_children, 6)
            case BlockType.PARAGRAPH:
                return raw_to_html_paragraph(parsed_children)
            case BlockType.UNORDERED_LIST:
                return raw_to_html_unordered_list(parsed_children)   
            case BlockType.ORDERED_LIST:
                return raw_to_html_ordered_list(parsed_children)
            case BlockType.LIST_ITEM:
                return raw_to_html_list_item(parsed_children)
            case BlockType.QUOTE:
                return raw_to_html_quote(parsed_children)
            case BlockType.MULTILINE_CODE:
                return raw_to_html_codeblock(parsed_children)
            case BlockType.DIV:
                return raw_to_html_div(parsed_children)
        raise ValueError('Error: Block Type not found')
        
        