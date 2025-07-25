

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        output = ""
        for prop in self.props:
            output += f' {prop}="{str(self.props[prop])}"'
        return output

    def __repr__(self):
        print(f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}")


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None and self.tag:
            # Self-closing tag
            return f"<{self.tag}{self.props_to_html()}>"
        elif not self.value:
            raise ValueError("Nothing to print (no value given).")
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag provided.")
        elif not self.children:
            raise ValueError("No children provided.")
        else:
            output = ""
            for child in self.children:
                output += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{output}</{self.tag}>"
                