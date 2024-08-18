from re import findall, search
from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode


search_patterns = {
    "bold": r"(\*\*(?!\*)(.*?)\*\*)",
    "italic": r"(?<!\*)(\*(?!\*)(.*?)\*)(?!\*)",
    "code": r"\`.+?\`",
    "image": r"\!\[.*?\]\(.+?\)",
    "link": r"(?<!\!)\[.*\]\(.*\)"
}

delimiters = {
    "bold": "**",
    "italic": "*",
    "code": "`",
    "image": "![",
    "link": "["
}

punctuations = [
    ".", ",", "!", "?", ":", ";", "'", '"', "-", "...", "/", "&", "@", "$", "%", "^"
]


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case "text":
            return LeafNode(text_node.text)
        case "bold":
            return LeafNode(text_node.text, "b")
        case "italic":
            return LeafNode(text_node.text, "i")
        case "code":
            return LeafNode(text_node.text, "code")
        case "link":
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case "image":
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Matching value not found")


def split_nodes(text: str) -> list[TextNode]:
    new_nodes = []
    match_count = 0
    for val in search_patterns.values():
        find_match = findall(val, text)
        if find_match:
            match_count += 1
            pattern = find_match[0][0] if isinstance(
                find_match[0], tuple) else find_match[0]
            text = replace_pattern(text, pattern)

    if not match_count:
        new_nodes.append(TextNode(text, "text"))
    else:
        split_text = text.split("$$")
        for item in split_text:
            if item:
                if item.startswith(" ") or item.endswith(" ") or len(item) == 1 or (item[0] in punctuations and item[1] == " "):
                    new_nodes.append(TextNode(f"{item}", "text"))
                else:
                    args = item.split(", ")
                    new_nodes.append(TextNode(*args))

    return new_nodes


def replace_pattern(text: str, pattern: str) -> str:
    if pattern.startswith("**"):
        text = text.replace(
            pattern, f'$${pattern.replace("**", "")}, bold$$')
    elif pattern.startswith("*"):
        text = text.replace(
            pattern, f'$${pattern.replace("*", "")}, italic$$')
    elif pattern.startswith('`'):
        text = text.replace(
            pattern, f'$${pattern.replace("`", "")}, code$$')
    elif pattern.startswith('!['):
        alt, url = pattern.split("]")
        text = text.replace(
            pattern, f'$${alt[2:]}, image, {url[1:-1]}$$')
    elif pattern.startswith("["):
        link_text, url = pattern.split("]")
        text = text.replace(
            pattern, f'$${link_text[1:]}, link, {url[1:-1]}$$')
    else:
        return text

    return text


def markdown_to_blocks(text: str) -> list[str]:
    list_of_blocks = []
    if "```" in text:
        split_text = text.split("\n")
        filtered_blocks = []
        for i in range(len(split_text)):
            if (i + 1) <= len(split_text) - 1 and split_text[i].startswith("```") and split_text[i + 1]:
                filtered_blocks.append(split_text[i].replace("```", "```$"))
            else:
                filtered_blocks.append(split_text[i])
        text = "\n".join(filtered_blocks)
        code_block_count = text.count("```")
        blocks = text.split("```", code_block_count)
        blocks = [f"```{block.replace("$", "")}```" if block.startswith("$") else block for block in blocks]
        for block in blocks:
            if not block.startswith("```"):
                list_of_blocks.extend(block.split("\n\n"))
            else:
                list_of_blocks.append(block)
    else:
        list_of_blocks = text.split("\n\n")

    return [block for block in list_of_blocks if block]


def block_type(text: str) -> str:
    block_type = ""
    if text.startswith("#"):
        heading_type = text.count("#")
        block_type = f"heading {heading_type}"
    elif text.startswith("```"):
        block_type = "code"
    elif text.startswith(">"):
        block_type = "blockquote"
    elif text.startswith("* ") or text.startswith("- "):
        block_type = "unordered list"
    elif text[0].isdigit() and text[1] == ".":
        block_type = "ordered list"
    elif text.startswith("!["):
        block_type = "image"
    elif text.startswith("["):
        block_type = "link"
    else:
        block_type = "paragraph"

    return block_type


def markdown_to_html(markdown: str) -> HTMLNode:
    main_parent = None
    children = []
    split_markdown = markdown_to_blocks(markdown.strip())
    block_types = [block_type(block) for block in split_markdown]
    for i in range(len(block_types)):
        new_html_node = create_html_node(split_markdown[i], block_types[i])
        children.append(new_html_node)

    main_parent = ParentNode("div", children)

    return main_parent


def create_html_node(text: str, node_type: str) -> HTMLNode:
    children = []
    new_html_node = None
    if "heading" in node_type:
        text = text.replace("#", "").strip()
        get_children = split_nodes(text)
        children = [text_node_to_html_node(
            node) for node in get_children]
        new_html_node = ParentNode(f"h{node_type[-1]}", children)
    elif node_type == "paragraph":
        text_lines = text.split("\n")
        text_lines = [line.strip() for line in text_lines]
        all_lines = " ".join(text_lines)
        get_children = split_nodes(all_lines)
        children = [text_node_to_html_node(
            node) for node in get_children]
        new_html_node = ParentNode("p", children)
    elif node_type == "unordered list":
        list_items = text.split("\n")
        list_items = [item.replace("-", "").strip() if item.startswith(
            "-") else item.replace("*", "").strip() for item in list_items]
        for item in list_items:
            get_children = split_nodes(item)
            li_children = [text_node_to_html_node(
                node) for node in get_children]
            li_node = ParentNode("li", li_children)
            children.append(li_node)
        new_html_node = ParentNode("ul", children)
    elif node_type == "ordered list":
        list_items = text.split("\n")
        list_items = [list_items[i].replace(
            f"{i + 1}.", "").strip() for i in range(len(list_items))]

        for item in list_items:
            get_children = split_nodes(item)
            li_children = [text_node_to_html_node(
                node) for node in get_children]
            li_node = ParentNode("li", li_children)
            children.append(li_node)
        new_html_node = ParentNode("ol", children)

    elif node_type == "blockquote":
        lines = text.split("\n")
        lines = [line.replace(">", "").strip() for line in lines]
        all_lines = " ".join(lines)
        get_children = split_nodes(all_lines)
        children = [text_node_to_html_node(
            node) for node in get_children]
        new_html_node = ParentNode("blockquote", children)

    elif node_type == "code":
        code_lines = text.split("\n")
        code_lines = [line.replace("```", "").strip()
                      for line in code_lines[1:]]
        all_code = "\n".join(code_lines).strip()
        get_children = split_nodes(all_code)
        children = [text_node_to_html_node(
            node) for node in get_children]
        code_element = ParentNode("code", children)
        new_html_node = ParentNode("pre", [code_element])

    elif node_type == "image":
        get_image = replace_pattern(text, text)
        get_image = get_image.replace("$$", "").split(",")
        new_html_node = LeafNode("", "img", {"src": get_image[2], "alt": get_image[0]})

    elif node_type == "link":
        get_link = replace_pattern(text, text)
        get_link = get_link.replace("$$", "").split(",")
        new_html_node = LeafNode(get_link[0], "a", {"href": get_link[2]})

    else:
        raise ValueError("Usupported node type is provided")

    return new_html_node


def extract_title(text: str) -> str:
    heading_pattern = r"(?<!#)#{1}(\s.+?)\n"
    find_heading = search(heading_pattern, text)
    if not find_heading:
        raise ValueError("The element is missing! Cannot extract heading!")
    return find_heading.group().replace("#", "").strip()





text = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty)

> All that is gold does not glitter

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney *didn't ruin it*
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Hello, World!")
}
```
"""

text2 = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty)

> All that is gold does not glitter

## Reasons I like Tolkien"""

# print(markdown_to_html(text))
