from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, children=None, tag=None, props=None):
        if children is None: raise ValueError("No children")
        if tag is None: raise ValueError("No tag")
        self.tag = tag
        self.children = children
        self.props = props
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        return f"<{self.tag}{' ' if (self.props is not None and len(self.props) > 1) else ''}{self.props_to_html()}>{''.join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"
    
    # def props_to_html(self):
    #     if self.props is not None and len(self.props) > 0:
    #         return " " + " ".join(map(lambda x: x + '="' + self.props[x].replace('"','\\"') + '"', self.props.keys()))
    #     else: return ""
    
    # def __repr__(self):
    #     return f"{self.tag=} {self.value=} {self.children=} {self.props=} {self.props_to_html()}"