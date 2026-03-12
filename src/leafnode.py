from htmlnode import HTMLNode
from textnode import TextType, TextNode
from raw_to_html_functions import * 

class LeafNode(HTMLNode):
    def __init__(self, tag: TextType, value, props=None):
        if not isinstance(tag, TextType):
            raise ValueError('LeafNode tag must be of type TextType')
        super().__init__(tag, value, None, props)
        
    
    def to_html(self):
        if self.value is None:
            raise ValueError('All leaf nodes must have a value')
        match self.tag:
            case TextType.TEXT:
                return self.value
            case TextType.BOLD:
                return raw_to_html_bold(self.value)
            case TextType.ITALIC:
                return raw_to_html_italic(self.value)
            case TextType.LINK:
                if not self.props or 'href' not in self.props:
                    raise Exception('href needed for link parsing')
                return raw_to_html_link(self.value, self.props['href'])
            case TextType.IMAGE:
                if not self.props or 'src' not in self.props:
                    raise Exception('src needed for image parsing')
                return raw_to_html_image(self.value, self.props['src'])
            case TextType.CODE:
                return raw_to_html_code_oneliner(self.value)
            
            
    
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, props={self.props})'