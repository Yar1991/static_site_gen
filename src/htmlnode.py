class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None,
                children: list | None = None, props: dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        attrs = ""
        if not self.props:
            return ""
        for key, val in self.props.items():
            attrs += f" {key}='{val}'"
        return attrs


    def __eq__(self, value: object) -> bool:
        return str(self) == str(value)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
