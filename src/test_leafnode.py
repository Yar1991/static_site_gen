import unittest

from leafnode import LeafNode
from htmlnode import HTMLNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("hello", "h1", {"class": "heading"})
        node2 = LeafNode("hello", "h1", {"class": "heading"})
        node3 = LeafNode("some text", "p")

        self.assertEqual(node1, node2)
        self.assertEqual(node3, "LeafNode(some text, p, None)")

    def test_to_html(self):
        node1 = LeafNode("hello", "h1", {"class": "heading"})
        node2 = LeafNode("some text", "p")
        node3 = LeafNode("bla bla")

        self.assertEqual(node1.to_html(), "<h1 class='heading'>hello</h1>")
        self.assertEqual(node2.to_html(), "<p>some text</p>")
        self.assertEqual(node3.to_html(), "bla bla")

    def test_no_value(self):
        node1 = LeafNode("", "h1", {"class": "heading"})
        self.assertRaises(ValueError, node1.to_html)
