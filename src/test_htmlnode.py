import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self) -> None:
        node1 = HTMLNode("p", "some text", props={"class": "text"})
        node2 = HTMLNode("p", "some text", props={"class": "text"})
        node3 = HTMLNode()

        self.assertEqual(node1, node2)
        self.assertEqual(node3, "HTMLNode(None, None, None, None)")

    def test_not_eq(self) -> None:
        node1 = HTMLNode("h1", "hello", props={"class": "heading"})
        node2 = HTMLNode("p", "some text", props={"class": "text"})

        self.assertNotEqual(node1, node2)

    def test_to_html(self) -> None:
        node = HTMLNode("p", "some text", props={"class": "text"})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props(self) -> None:
        node1 = HTMLNode("p", "some text", props={"class": "text"})
        node2 = HTMLNode("a", "click me", props={"href": "/home", "target": "_blank" ,"class": "link"})

        self.assertEqual(node1.props_to_html(), " class='text'")
        self.assertEqual(node2.props_to_html(), " href='/home' target='_blank' class='link'")
