import pytest
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextType
from blocktype import BlockType


def text_leaf(text):
    return LeafNode(TextType.TEXT, text)


class TestParentNodeConstruction:
    def test_valid_construction(self):
        node = ParentNode(BlockType.PARAGRAPH, [text_leaf("hello")])
        assert node.tag == BlockType.PARAGRAPH

    def test_invalid_tag_raises(self):
        with pytest.raises(ValueError):
            ParentNode("p", [text_leaf("hello")])

    def test_invalid_tag_none_raises(self):
        with pytest.raises(ValueError):
            ParentNode(None, [text_leaf("hello")])


class TestParentNodeToHtml:
    def test_paragraph(self):
        node = ParentNode(BlockType.PARAGRAPH, [text_leaf("Hello world")])
        assert node.to_html() == "<p>Hello world</p>"

    def test_paragraph_newline_replaced(self):
        node = ParentNode(BlockType.PARAGRAPH, [text_leaf("line one\nline two")])
        assert node.to_html() == "<p>line one line two</p>"

    def test_heading_first(self):
        node = ParentNode(BlockType.HEADING_FIRST, [text_leaf("# Title")])
        assert node.to_html() == "<h1>Title</h1>"

    def test_heading_second(self):
        node = ParentNode(BlockType.HEADING_SECOND, [text_leaf("## Title")])
        assert node.to_html() == "<h2>Title</h2>"

    def test_heading_third(self):
        node = ParentNode(BlockType.HEADING_THIRD, [text_leaf("### Title")])
        assert node.to_html() == "<h3>Title</h3>"

    def test_heading_fourth(self):
        node = ParentNode(BlockType.HEADING_FOURTH, [text_leaf("#### Title")])
        assert node.to_html() == "<h4>Title</h4>"

    def test_heading_fifth(self):
        node = ParentNode(BlockType.HEADING_FIFTH, [text_leaf("##### Title")])
        assert node.to_html() == "<h5>Title</h5>"

    def test_heading_sixth(self):
        node = ParentNode(BlockType.HEADING_SIXTH, [text_leaf("###### Title")])
        assert node.to_html() == "<h6>Title</h6>"

    def test_unordered_list(self):
        item = ParentNode(BlockType.LIST_ITEM, [text_leaf("item")])
        node = ParentNode(BlockType.UNORDERED_LIST, [item])
        assert node.to_html() == "<ul>\n<li>item</li></ul>"

    def test_ordered_list(self):
        item = ParentNode(BlockType.LIST_ITEM, [text_leaf("item")])
        node = ParentNode(BlockType.ORDERED_LIST, [item])
        assert node.to_html() == "<ol>\n<li>item</li></ol>"

    def test_list_item(self):
        node = ParentNode(BlockType.LIST_ITEM, [text_leaf("item text")])
        assert node.to_html() == "<li>item text</li>"

    def test_quote(self):
        node = ParentNode(BlockType.QUOTE, [text_leaf("quoted")])
        assert node.to_html() == "<blockquote>quoted</blockquote>"

    def test_multiline_code(self):
        node = ParentNode(BlockType.MULTILINE_CODE, [text_leaf("x = 1\n")])
        assert node.to_html() == "<pre><code>x = 1\n</code></pre>"

    def test_div(self):
        inner = ParentNode(BlockType.PARAGRAPH, [text_leaf("hello")])
        node = ParentNode(BlockType.DIV, [inner])
        assert node.to_html() == "<div><p>hello</p></div>"

    def test_multiple_children_concatenated(self):
        node = ParentNode(BlockType.PARAGRAPH, [text_leaf("Hello "), text_leaf("world")])
        assert node.to_html() == "<p>Hello world</p>"

    def test_nested_children(self):
        bold = LeafNode(TextType.BOLD, "bold")
        node = ParentNode(BlockType.PARAGRAPH, [text_leaf("Text: "), bold])
        assert node.to_html() == "<p>Text: <b>bold</b></p>"

    def test_no_children_raises(self):
        node = ParentNode(BlockType.PARAGRAPH, None)
        with pytest.raises(ValueError):
            node.to_html()

    def test_unordered_list_multiple_items(self):
        items = [
            ParentNode(BlockType.LIST_ITEM, [text_leaf("one")]),
            ParentNode(BlockType.LIST_ITEM, [text_leaf("two")]),
            ParentNode(BlockType.LIST_ITEM, [text_leaf("three")]),
        ]
        node = ParentNode(BlockType.UNORDERED_LIST, items)
        assert node.to_html() == "<ul>\n<li>one</li><li>two</li><li>three</li></ul>"
