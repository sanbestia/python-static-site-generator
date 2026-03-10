class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
        
    def to_html(self):
        raise NotImplementedError("Not implemented in parent class")
    
    
    def props_to_html(self):
        if self.props is None:
            return ""
        sorted_props = sorted(list(self.props.items()))
        return " ".join(f"{key}:{value}" for key, value in sorted_props)
        
        
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'