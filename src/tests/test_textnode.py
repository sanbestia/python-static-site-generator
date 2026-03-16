import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        
    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)
        
        
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is another node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)
        
    
    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)
        
        
    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://shoe.dev")
        self.assertNotEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("hello", TextType.BOLD, "https://example.com")
        self.assertEqual(repr(node), "TextNode(hello, bold, https://example.com)")

    def test_repr_without_url(self):
        node = TextNode("hello", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(hello, text, None)")


if __name__ == "__main__":
    unittest.main()