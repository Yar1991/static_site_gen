from unittest import TestCase

from textnode import TextNode
from utils import text_node_to_html_node, split_nodes, markdown_to_blocks, block_type, markdown_to_html, extract_title


class Test(TestCase):
    def test_text_to_html_node(self):
        fail_node = TextNode("lol", "lol")
        with self.assertRaises(ValueError) as err:
            text_node_to_html_node(fail_node)
        self.assertIsInstance(err.exception, ValueError)

        text_node = text_node_to_html_node(TextNode("hello", "text"))
        self.assertEqual(text_node, "LeafNode(hello, None, None)")

        bold_node = text_node_to_html_node(TextNode("bold hello", "bold"))
        self.assertEqual(bold_node, "LeafNode(bold hello, b, None)")

        italic_node = text_node_to_html_node(
            TextNode("italic hello", "italic"))
        self.assertEqual(italic_node, "LeafNode(italic hello, i, None)")

        code_node = text_node_to_html_node(
            TextNode("let greet = 'hello'", "code"))
        self.assertEqual(
            code_node, "LeafNode(let greet = 'hello', code, None)")

        link_node = text_node_to_html_node(
            TextNode("click me", "link", "/home"))
        self.assertEqual(link_node, "LeafNode(click me, a, {'href': '/home'})")

        img_node = text_node_to_html_node(
            TextNode("some image", "image", "/media/image.png"))
        self.assertEqual(
            img_node, "LeafNode(, img, {'src': '/media/image.png', 'alt': 'some image'})")

    def test_split_nodes(self):
        test_text1 = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        test_text2 = "Some *italic text* and some code `let a = 5;` and an image ![nice cat](https://images.com/cats/1) and some **bold text** as well"

        text1_result = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image",
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]

        text2_result = [
            TextNode("Some ", "text"),
            TextNode("italic text", "italic"),
            TextNode(" and some code ", "text"),
            TextNode("let a = 5;", "code"),
            TextNode(" and an image ", "text"),
            TextNode("nice cat", "image", "https://images.com/cats/1"),
            TextNode(" and some ", "text"),
            TextNode("bold text", "bold"),
            TextNode(" as well", "text"),
        ]

        self.assertEqual(split_nodes(test_text1), text1_result)
        self.assertEqual(split_nodes(test_text2), text2_result)

    def test_markdown_to_blocks(self):
        example = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        expected_result = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                           '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        self.assertEqual(markdown_to_blocks(example), expected_result)

    def test_block_type(self):
        example = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item

Another random paragraph with some **bold text**.
And mayve some *italic* text as well.

1. One
2. Two
3. Three

## And one more heading.

> Someone said something interesting
> Like bla bla bla..."""

        expected_result = ["heading 1", "paragraph", "unordered list",
                           "paragraph", "ordered list", "heading 2", "blockquote"]

        split_markdown = markdown_to_blocks(example)
        markdown_types = [block_type(block) for block in split_markdown]
        self.assertEqual(markdown_types, expected_result)

    def test_markdown_to_html(self):

        large_markdown = """# My Markdown Example

## Introduction

This is a simple example of a markdown document. Markdown allows you to format text easily and is often used for writing documentation or README files.

## Features

- Easy to read and write
- Supports multiple formatting options
- Can be converted to HTML

> "Markdown is a lightweight markup language with plain-text formatting syntax." - John Gruber

## Example Code

Here is an example of a simple Python code block:

```python
def greet(name):
    return f"Hello, {name}!"
print(greet("World"))
```
"""

        expected_html = """<div><h1>My Markdown Example</h1><h2>Introduction</h2><p>This is a simple example of a markdown document. Markdown allows you to format text easily and is often used for writing documentation or README files.</p><h2>Features</h2><ul><li>Easy to read and write</li><li>Supports multiple formatting options</li><li>Can be converted to HTML</li></ul><blockquote>"Markdown is a lightweight markup language with plain-text formatting syntax." - John Gruber</blockquote><h2>Example Code</h2><p>Here is an example of a simple Python code block:</p><pre><code>def greet(name):
return f"Hello, {name}!"
print(greet("World"))</code></pre></div>"""

        self.assertEqual(markdown_to_html(
            large_markdown).to_html(), expected_html)

    def test_extract_title(self):
        test_text = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

### Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy"""

        exptected_result = "Tolkien Fan Club"

        self.assertEqual(extract_title(test_text), exptected_result)
