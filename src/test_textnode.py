import unittest

from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node1 = TextNode("hello", "regular")
        node2 = TextNode("hello", "regular")
        node3 = TextNode("lol", "italic", "/home/bla")
        node4 = TextNode("sup", "bold")
        self.assertEqual(node1, node2)
        self.assertNotEqual(node3, node4)

    def test_repr(self) -> None:
        node_without_url = TextNode("hello", "regular")
        node_with_url = TextNode("click me", "bold", "https://bla.com")
        self.assertEqual(node_without_url, "TextNode(hello, regular, None)")
        self.assertEqual(node_with_url, "TextNode(click me, bold, https://bla.com)")


if __name__ == "__main__":
    unittest.main()
