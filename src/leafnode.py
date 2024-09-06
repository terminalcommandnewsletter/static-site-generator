from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value=None, tag=None, props=None):
        if value is None: raise ValueError("No value")
        self.tag = tag
        self.value = value
        # self.children = children
        self.props = props
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        # if self.value is None: raise ValueError
        if self.tag is not None and len(self.tag) > 0: return f"<{self.tag}{' ' if (self.props is not None and len(self.props) > 1) else ''}{self.props_to_html()}>{self.value}</{self.tag}>"
        return self.value
    
    # def props_to_html(self):
    #     if self.props is not None and len(self.props) > 0:
    #         return " " + " ".join(map(lambda x: x + '="' + self.props[x].replace('"','\\"') + '"', self.props.keys()))
    #     else: return ""
    
    def __repr__(self):
        return f"{self.tag=} {self.value=} {self.props=} {self.props_to_html()}"