class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is not None and len(self.props) > 0:
            return " " + " ".join(map(lambda x: x + '="' + self.props[x].replace('"','\\"') + '"', self.props.keys()))
        else: return ""
    
    def __repr__(self):
        return f"{self.tag=} {self.value=} {self.children=} {self.props=} {self.props_to_html()}"
    
    def __eq__(self, o):
        return self.tag == o.tag and self.value == o.value and self.children == o.children and self.props == o.props