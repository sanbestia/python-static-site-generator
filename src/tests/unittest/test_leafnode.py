import unittest
from leafnode import LeafNode
from textnode import TextType


class TestLeafNode(unittest.TestCase):
    def test_text(self):
        node = LeafNode(TextType.TEXT, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_bold(self):
        node = LeafNode(TextType.BOLD, "bold text")
        self.assertEqual(node.to_html(), "<b>bold text</b>")

    def test_italic(self):
        node = LeafNode(TextType.ITALIC, "italic text")
        self.assertEqual(node.to_html(), "<i>italic text</i>")

    def test_code(self):
        node = LeafNode(TextType.CODE, "print('hi')")
        self.assertEqual(node.to_html(), "<code>print('hi')</code>")

    def test_link(self):
        node = LeafNode(TextType.LINK, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_image(self):
        node = LeafNode(TextType.IMAGE, "alt text", {"src": "image.png"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="alt text">')

    def test_link_missing_href_raises(self):
        node = LeafNode(TextType.LINK, "Click me!")
        with self.assertRaises(Exception):
            node.to_html()

    def test_image_missing_src_raises(self):
        node = LeafNode(TextType.IMAGE, "alt text")
        with self.assertRaises(Exception):
            node.to_html()

    def test_value_none_raises(self):
        node = LeafNode(TextType.TEXT, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_tag_not_texttype_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", "Hello, world!")


if __name__ == "__main__":
    unittest.main()