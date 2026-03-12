import pytest
from leafnode import LeafNode
from textnode import TextType


class TestLeafNode:
    def test_text(self):
        node = LeafNode(TextType.TEXT, "Hello, world!")
        assert node.to_html() == "Hello, world!"

    def test_bold(self):
        node = LeafNode(TextType.BOLD, "bold text")
        assert node.to_html() == "<strong>bold text</strong>"

    def test_italic(self):
        node = LeafNode(TextType.ITALIC, "italic text")
        assert node.to_html() == "<em>italic text</em>"

    def test_code(self):
        node = LeafNode(TextType.CODE, "print('hi')")
        assert node.to_html() == "<code>print('hi')</code>"

    def test_link(self):
        node = LeafNode(TextType.LINK, "Click me!", {"href": "https://www.google.com"})
        assert node.to_html() == '<a href="https://www.google.com">Click me!</a>'

    def test_image(self):
        node = LeafNode(TextType.IMAGE, "alt text", {"src": "image.png"})
        assert node.to_html() == '<img src="image.png" alt="alt text">'

    def test_link_missing_href_raises(self):
        node = LeafNode(TextType.LINK, "Click me!")
        with pytest.raises(Exception):
            node.to_html()

    def test_image_missing_src_raises(self):
        node = LeafNode(TextType.IMAGE, "alt text")
        with pytest.raises(Exception):
            node.to_html()

    def test_value_none_raises(self):
        node = LeafNode(TextType.TEXT, None)
        with pytest.raises(ValueError):
            node.to_html()

    def test_tag_not_texttype_raises(self):
        with pytest.raises(ValueError):
            LeafNode("p", "Hello, world!")