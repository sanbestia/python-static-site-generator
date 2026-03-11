from htmlnode import HTMLNode
from text_functions import raw_to_link, raw_to_paragraph

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    
    def to_html(self):
        if self.value is None:
            raise ValueError('All leaf nodes must have a value')
        if self.tag is None:
            return self.value
        if self.tag == 'p':
            return raw_to_paragraph(self.value)
        if self.tag == 'a':
            if not self.props or 'href' not in self.props:
                raise Exception('href needed for link parsing')
            return raw_to_link(self.value, self.props['href'])
    
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, props={self.props})'