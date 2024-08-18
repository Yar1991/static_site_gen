from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict | None = None) -> None:
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("The tag is missing")
        if not self.children:
            raise ValueError("Children are missing")

        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()

        return result + f"</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
