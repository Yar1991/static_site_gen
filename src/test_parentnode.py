import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        paragraph_node = LeafNode("some text", "p", {"class": "text"})
        link_node = LeafNode("click me", "a", {"class": "link", "href": "/home"})
        div_node = ParentNode("div", [paragraph_node, link_node], {"class": "block"})

        noprops_parent = ParentNode("ul", [LeafNode("one", "li"), LeafNode("two", "li"), LeafNode("three", "li")])

        self.assertEqual(div_node, "ParentNode(div, [LeafNode(some text, p, {'class': 'text'}), LeafNode(click me, a, {'class': 'link', 'href': '/home'})], {'class': 'block'})")
        self.assertEqual(noprops_parent, "ParentNode(ul, [LeafNode(one, li, None), LeafNode(two, li, None), LeafNode(three, li, None)], None)")


    def test_no_tag(self):
        node = ParentNode("", [LeafNode("one", "li"), LeafNode("two", "li"), LeafNode("three", "li")])
        self.assertRaises(ValueError, node.to_html)

    def test_no_children(self):
        node = ParentNode("div", [], {"class": "box"})
        self.assertRaises(ValueError, node.to_html)

    def test_to_html(self):
        paragraph_node = LeafNode("some text", "p", {"class": "text"})
        link_node = LeafNode("click me", "a", {"class": "link", "href": "/home"})
        div_node = ParentNode("div", [paragraph_node, link_node], {"class": "block"})
        result_str1 = "<div class='block'><p class='text'>some text</p><a class='link' href='/home'>click me</a></div>"
        self.assertEqual(div_node.to_html(), result_str1.strip())

        ul_node = ParentNode("ul", [LeafNode("one", "li"), LeafNode("two", "li"), LeafNode("three", "li")], {"class": "list"})
        btn_node = LeafNode("Submit", "button", {"class": "btn", "type": "button"})
        div_child_node = ParentNode("div", [ul_node, btn_node], {"class": "box"})

        div_parent_node = ParentNode("div", [div_node, div_child_node], {"class": "main-box"})
        result_str2 = "<div class='main-box'><div class='block'><p class='text'>some text</p><a class='link' href='/home'>click me</a></div><div class='box'><ul class='list'><li>one</li><li>two</li><li>three</li></ul><button class='btn' type='button'>Submit</button></div></div>"

        self.assertEqual(div_parent_node.to_html(), result_str2.strip())
