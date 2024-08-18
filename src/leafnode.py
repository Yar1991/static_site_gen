from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str | None = None, props: dict | None = None) -> None:
        super().__init__(value = value, tag = tag, props = props)

    def to_html(self) -> str:
        if not self.value and not self.tag == "img":
            raise ValueError("The value is missing")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.value}, {self.tag}, {self.props})"
