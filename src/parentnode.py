from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    
    def to_html(self):
        if self.tag is None:
            raise ValueError('All parent nodes must have a tag')
        if self.children is None:
            raise ValueError('All parent nodes must have children')
        return