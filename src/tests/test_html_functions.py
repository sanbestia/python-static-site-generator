import re
import pytest
from enum import Enum
from blocktype import BlockType
from html_functions import (
    block_to_block_type, text_to_children, markdown_to_html_node,
    markdown_to_blocks,
    unordered_list_to_children, ordered_list_to_children,
    quote_to_children, multiline_code_to_child,
)
from textnode import TextType


# ── HEADING ──────────────────────────────────────────────────────────────────

class TestHeading:
    def test_h1(self):
        assert block_to_block_type('# Heading') == BlockType.HEADING_FIRST

    def test_h2(self):
        assert block_to_block_type('## Another heading') == BlockType.HEADING_SECOND

    def test_h3(self):
        assert block_to_block_type('### Another nother heading') == BlockType.HEADING_THIRD

    def test_h4(self):
        assert block_to_block_type('#### Fourth heading') == BlockType.HEADING_FOURTH

    def test_h5(self):
        assert block_to_block_type('##### Fifth heading') == BlockType.HEADING_FIFTH

    def test_h6_max_valid(self):
        assert block_to_block_type('###### Max level heading') == BlockType.HEADING_SIXTH

    def test_h7_too_many_hashes(self):
        assert block_to_block_type('####### Too many hashes') == BlockType.PARAGRAPH

    def test_no_space_after_hash(self):
        assert block_to_block_type('#No space heading') == BlockType.PARAGRAPH

    def test_hash_not_at_start(self):
        assert block_to_block_type('a # Trailing char heading') == BlockType.PARAGRAPH


# ── MULTILINE CODE ────────────────────────────────────────────────────────────

class TestMultilineCode:
    def test_basic_code_block(self):
        assert block_to_block_type('```\nThis is code\n```') == BlockType.MULTILINE_CODE

    def test_multiline_code_block(self):
        assert block_to_block_type('```\nline1\nline2\nline3\n```') == BlockType.MULTILINE_CODE

    def test_empty_code_block(self):
        assert block_to_block_type('```\n```') == BlockType.MULTILINE_CODE

    def test_closing_backticks_no_newline(self):
        assert block_to_block_type('```\nThis is also code```') == BlockType.MULTILINE_CODE

    def test_opening_backticks_no_newline(self):
        assert block_to_block_type('```This is not code\n```') == BlockType.PARAGRAPH


# ── QUOTE ─────────────────────────────────────────────────────────────────────

class TestQuote:
    def test_single_line_no_space(self):
        assert block_to_block_type('>single line quote') == BlockType.QUOTE

    def test_single_line_with_space(self):
        assert block_to_block_type('> single line quote with space') == BlockType.QUOTE

    def test_multiline_no_spaces(self):
        assert block_to_block_type('>line one\n>line two\n>line three') == BlockType.QUOTE

    def test_multiline_with_spaces(self):
        assert block_to_block_type('> line one\n> line two\n> line three') == BlockType.QUOTE

    def test_multiline_mixed_spacing(self):
        assert block_to_block_type('>line one\n> line two\n>line three') == BlockType.QUOTE

    def test_line_missing_arrow(self):
        assert block_to_block_type('>line one\nline two') == BlockType.PARAGRAPH

    def test_no_arrow_at_all(self):
        assert block_to_block_type('no arrow') == BlockType.PARAGRAPH

    def test_space_before_arrow(self):
        assert block_to_block_type('>line one\n >indented arrow') == BlockType.PARAGRAPH


# ── UNORDERED LIST ────────────────────────────────────────────────────────────

class TestUnorderedList:
    def test_single_item(self):
        assert block_to_block_type('- item one') == BlockType.UNORDERED_LIST

    def test_multiple_items(self):
        assert block_to_block_type('- item one\n- item two\n- item three') == BlockType.UNORDERED_LIST

    def test_line_missing_dash(self):
        assert block_to_block_type('- item one\n- item two\nbad item') == BlockType.PARAGRAPH

    def test_no_space_after_dash(self):
        assert block_to_block_type('-no space') == BlockType.PARAGRAPH

    def test_indented_dash(self):
        assert block_to_block_type('- item\n -indented dash') == BlockType.PARAGRAPH


# ── ORDERED LIST ──────────────────────────────────────────────────────────────

class TestOrderedList:
    def test_single_item(self):
        assert block_to_block_type('1. First item') == BlockType.ORDERED_LIST

    def test_multiple_items(self):
        assert block_to_block_type('1. First\n2. Second\n3. Third') == BlockType.ORDERED_LIST

    def test_skipped_number(self):
        assert block_to_block_type('1. First\n2. Second\n4. Fourth') == BlockType.PARAGRAPH

    def test_starts_at_zero(self):
        assert block_to_block_type('0. Starts at zero') == BlockType.PARAGRAPH

    def test_line_missing_number(self):
        assert block_to_block_type('1. First\n2. Second\nbad item') == BlockType.PARAGRAPH

    def test_no_space_after_period(self):
        assert block_to_block_type('1.No space') == BlockType.PARAGRAPH

    def test_starts_at_two(self):
        assert block_to_block_type('2. Starts at two\n3. Third') == BlockType.PARAGRAPH


# ── PARAGRAPH ─────────────────────────────────────────────────────────────────

class TestParagraph:
    def test_plain_text(self):
        assert block_to_block_type('Just a plain paragraph.') == BlockType.PARAGRAPH

    def test_multiline_paragraph(self):
        assert block_to_block_type('Two lines\nof a paragraph') == BlockType.PARAGRAPH

    def test_empty_string(self):
        assert block_to_block_type('') == BlockType.PARAGRAPH

    def test_mixed_markers(self):
        assert block_to_block_type('Mixed # heading and > quote') == BlockType.PARAGRAPH


# ── TEXT TO CHILDREN ──────────────────────────────────────────────────────────

class TestTextToChildren:
    def test_plain_text(self):
        children = text_to_children("hello world")
        assert len(children) == 1
        assert children[0].value == "hello world"
        assert children[0].tag == TextType.TEXT

    def test_bold(self):
        children = text_to_children("this is **bold** text")
        types = [c.tag for c in children]
        assert TextType.BOLD in types
        bold = next(c for c in children if c.tag == TextType.BOLD)
        assert bold.value == "bold"

    def test_italic(self):
        children = text_to_children("this is _italic_ text")
        types = [c.tag for c in children]
        assert TextType.ITALIC in types
        italic = next(c for c in children if c.tag == TextType.ITALIC)
        assert italic.value == "italic"

    def test_inline_code(self):
        children = text_to_children("use `print()` here")
        types = [c.tag for c in children]
        assert TextType.CODE in types
        code = next(c for c in children if c.tag == TextType.CODE)
        assert code.value == "print()"

    def test_link(self):
        children = text_to_children("[click](http://x.com)")
        link = next(c for c in children if c.tag == TextType.LINK)
        assert link.value == "click"
        assert link.props == {"href": "http://x.com"}

    def test_image(self):
        children = text_to_children("![alt](img.png)")
        img = next(c for c in children if c.tag == TextType.IMAGE)
        assert img.value == "alt"
        assert img.props == {"src": "img.png"}

    def test_mixed_inline(self):
        children = text_to_children("**bold** and _italic_ and `code`")
        types = {c.tag for c in children}
        assert TextType.BOLD   in types
        assert TextType.ITALIC in types
        assert TextType.CODE   in types

    def test_empty_string(self):
        children = text_to_children("")
        assert children == []


# ── MARKDOWN TO HTML NODE ─────────────────────────────────────────────────────

class TestMarkdownToHtmlNode:
    def test_simple_paragraph(self):
        html = markdown_to_html_node("Hello world").to_html()
        assert "<p>" in html
        assert "Hello world" in html
        assert html.startswith("<div>")

    def test_bold_in_paragraph(self):
        html = markdown_to_html_node("this is **bold** text").to_html()
        assert "<b>bold</b>" in html

    def test_italic_in_paragraph(self):
        html = markdown_to_html_node("this is _italic_ text").to_html()
        assert "<i>italic</i>" in html

    def test_inline_code_in_paragraph(self):
        html = markdown_to_html_node("use `print()` here").to_html()
        assert "<code>print()</code>" in html

    def test_code_block_raw(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        html = markdown_to_html_node(md).to_html()
        assert "<pre><code>" in html
        assert "_should_" in html
        assert "**same**" in html
        assert "<em>" not in html
        assert "<strong>" not in html

    def test_code_block_no_extra_backticks(self):
        md = "```\nsome code\n```"
        html = markdown_to_html_node(md).to_html()
        assert "```" not in html

    def test_heading_h1(self):
        html = markdown_to_html_node("# Title").to_html()
        assert "<h1>" in html
        assert "Title" in html

    def test_heading_h2(self):
        html = markdown_to_html_node("## Subtitle").to_html()
        assert "<h2>" in html

    def test_unordered_list(self):
        html = markdown_to_html_node("- one\n- two\n- three").to_html()
        assert "<ul>" in html

    def test_ordered_list(self):
        html = markdown_to_html_node("1. first\n2. second").to_html()
        assert "<ol>" in html

    def test_quote(self):
        html = markdown_to_html_node("> a quote").to_html()
        assert "<blockquote>" in html

    def test_multiple_blocks(self):
        md = "# Heading\n\nA paragraph\n\n```\ncode\n```"
        html = markdown_to_html_node(md).to_html()
        assert "<h1>" in html
        assert "<p>" in html
        assert "<pre><code>" in html

    def test_wrapped_in_div(self):
        html = markdown_to_html_node("hello").to_html()
        assert html.startswith("<div>")
        assert html.endswith("</div>")


# ── MARKDOWN TO BLOCKS ────────────────────────────────────────────────────────

class TestMarkdownToBlocks:

    def test_single_block(self):
        assert markdown_to_blocks("hello world") == ["hello world"]

    def test_two_blocks(self):
        assert markdown_to_blocks("block one\n\nblock two") == ["block one", "block two"]

    def test_three_blocks(self):
        result = markdown_to_blocks("a\n\nb\n\nc")
        assert result == ["a", "b", "c"]

    def test_strips_surrounding_whitespace(self):
        result = markdown_to_blocks("  hello  \n\n  world  ")
        assert result == ["hello", "world"]

    def test_preserves_internal_newlines(self):
        result = markdown_to_blocks("line1\nline2\n\nother")
        assert result[0] == "line1\nline2"

    def test_empty_string_gives_one_empty_block(self):
        assert markdown_to_blocks("") == [""]


# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────

class TestUnorderedListToChildren:

    def test_single_item(self):
        children = unordered_list_to_children("- item one")
        assert len(children) == 1
        assert children[0].to_html() == "<li>item one</li>"

    def test_multiple_items(self):
        children = unordered_list_to_children("- one\n- two\n- three")
        assert len(children) == 3
        assert children[1].to_html() == "<li>two</li>"

    def test_inline_formatting_preserved(self):
        children = unordered_list_to_children("- **bold** item")
        html = children[0].to_html()
        assert "<b>bold</b>" in html


class TestOrderedListToChildren:

    def test_single_item(self):
        children = ordered_list_to_children("1. first")
        assert len(children) == 1
        assert children[0].to_html() == "<li>first</li>"

    def test_multiple_items(self):
        children = ordered_list_to_children("1. one\n2. two\n3. three")
        assert len(children) == 3
        assert children[2].to_html() == "<li>three</li>"

    def test_strips_numbering(self):
        children = ordered_list_to_children("1. item")
        assert "1." not in children[0].to_html()


class TestQuoteToChildren:

    def test_single_line(self):
        children = quote_to_children("> quoted text")
        assert len(children) == 1
        assert children[0].value == "quoted text"

    def test_multiline_joined(self):
        children = quote_to_children("> line one\n> line two")
        combined = "".join(c.to_html() for c in children)
        assert "line one" in combined
        assert "line two" in combined

    def test_strips_arrow_prefix(self):
        children = quote_to_children(">no space")
        assert children[0].value == "no space"


class TestMultilineCodeToChild:

    def test_basic(self):
        node = multiline_code_to_child("```\nsome code\n```")
        assert node.value == "some code\n"

    def test_multiline_code(self):
        node = multiline_code_to_child("```\nline1\nline2\n```")
        assert node.value == "line1\nline2\n"

    def test_backticks_stripped(self):
        node = multiline_code_to_child("```\ncode\n```")
        assert "```" not in node.value