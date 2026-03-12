import unittest
from blocktype import BlockType
from html_functions import block_to_block_type, text_to_children, markdown_to_html_node
from textnode import TextType


# ── HEADING ──────────────────────────────────────────────────────────────────

class TestHeading(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(block_to_block_type('# Heading'), BlockType.HEADING_FIRST)

    def test_h2(self):
        self.assertEqual(block_to_block_type('## Another heading'), BlockType.HEADING_SECOND)

    def test_h3(self):
        self.assertEqual(block_to_block_type('### Another nother heading'), BlockType.HEADING_THIRD)

    def test_h4(self):
        self.assertEqual(block_to_block_type('#### Fourth heading'), BlockType.HEADING_FOURTH)

    def test_h5(self):
        self.assertEqual(block_to_block_type('##### Fifth heading'), BlockType.HEADING_FIFTH)

    def test_h6_max_valid(self):
        self.assertEqual(block_to_block_type('###### Max level heading'), BlockType.HEADING_SIXTH)

    def test_h7_too_many_hashes(self):
        self.assertEqual(block_to_block_type('####### Too many hashes'), BlockType.PARAGRAPH)

    def test_no_space_after_hash(self):
        self.assertEqual(block_to_block_type('#No space heading'), BlockType.PARAGRAPH)

    def test_hash_not_at_start(self):
        self.assertEqual(block_to_block_type('a # Trailing char heading'), BlockType.PARAGRAPH)


# ── MULTILINE CODE ────────────────────────────────────────────────────────────

class TestMultilineCode(unittest.TestCase):
    def test_basic_code_block(self):
        self.assertEqual(block_to_block_type('```\nThis is code\n```'), BlockType.MULTILINE_CODE)

    def test_multiline_code_block(self):
        self.assertEqual(block_to_block_type('```\nline1\nline2\nline3\n```'), BlockType.MULTILINE_CODE)

    def test_empty_code_block(self):
        self.assertEqual(block_to_block_type('```\n```'), BlockType.MULTILINE_CODE)

    def test_closing_backticks_no_newline(self):
        self.assertEqual(block_to_block_type('```\nThis is also code```'), BlockType.MULTILINE_CODE)

    def test_opening_backticks_no_newline(self):
        self.assertEqual(block_to_block_type('```This is not code\n```'), BlockType.PARAGRAPH)


# ── QUOTE ─────────────────────────────────────────────────────────────────────

class TestQuote(unittest.TestCase):
    def test_single_line_no_space(self):
        self.assertEqual(block_to_block_type('>single line quote'), BlockType.QUOTE)

    def test_single_line_with_space(self):
        self.assertEqual(block_to_block_type('> single line quote with space'), BlockType.QUOTE)

    def test_multiline_no_spaces(self):
        self.assertEqual(block_to_block_type('>line one\n>line two\n>line three'), BlockType.QUOTE)

    def test_multiline_with_spaces(self):
        self.assertEqual(block_to_block_type('> line one\n> line two\n> line three'), BlockType.QUOTE)

    def test_multiline_mixed_spacing(self):
        self.assertEqual(block_to_block_type('>line one\n> line two\n>line three'), BlockType.QUOTE)

    def test_line_missing_arrow(self):
        self.assertEqual(block_to_block_type('>line one\nline two'), BlockType.PARAGRAPH)

    def test_no_arrow_at_all(self):
        self.assertEqual(block_to_block_type('no arrow'), BlockType.PARAGRAPH)

    def test_space_before_arrow(self):
        self.assertEqual(block_to_block_type('>line one\n >indented arrow'), BlockType.PARAGRAPH)


# ── UNORDERED LIST ────────────────────────────────────────────────────────────

class TestUnorderedList(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(block_to_block_type('- item one'), BlockType.UNORDERED_LIST)

    def test_multiple_items(self):
        self.assertEqual(block_to_block_type('- item one\n- item two\n- item three'), BlockType.UNORDERED_LIST)

    def test_line_missing_dash(self):
        self.assertEqual(block_to_block_type('- item one\n- item two\nbad item'), BlockType.PARAGRAPH)

    def test_no_space_after_dash(self):
        self.assertEqual(block_to_block_type('-no space'), BlockType.PARAGRAPH)

    def test_indented_dash(self):
        self.assertEqual(block_to_block_type('- item\n -indented dash'), BlockType.PARAGRAPH)


# ── ORDERED LIST ──────────────────────────────────────────────────────────────

class TestOrderedList(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(block_to_block_type('1. First item'), BlockType.ORDERED_LIST)

    def test_multiple_items(self):
        self.assertEqual(block_to_block_type('1. First\n2. Second\n3. Third'), BlockType.ORDERED_LIST)

    def test_skipped_number(self):
        self.assertEqual(block_to_block_type('1. First\n2. Second\n4. Fourth'), BlockType.PARAGRAPH)

    def test_starts_at_zero(self):
        self.assertEqual(block_to_block_type('0. Starts at zero'), BlockType.PARAGRAPH)

    def test_line_missing_number(self):
        self.assertEqual(block_to_block_type('1. First\n2. Second\nbad item'), BlockType.PARAGRAPH)

    def test_no_space_after_period(self):
        self.assertEqual(block_to_block_type('1.No space'), BlockType.PARAGRAPH)

    def test_starts_at_two(self):
        self.assertEqual(block_to_block_type('2. Starts at two\n3. Third'), BlockType.PARAGRAPH)


# ── PARAGRAPH ─────────────────────────────────────────────────────────────────

class TestParagraph(unittest.TestCase):
    def test_plain_text(self):
        self.assertEqual(block_to_block_type('Just a plain paragraph.'), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        self.assertEqual(block_to_block_type('Two lines\nof a paragraph'), BlockType.PARAGRAPH)

    def test_empty_string(self):
        self.assertEqual(block_to_block_type(''), BlockType.PARAGRAPH)

    def test_mixed_markers(self):
        self.assertEqual(block_to_block_type('Mixed # heading and > quote'), BlockType.PARAGRAPH)


# ── TEXT TO CHILDREN ──────────────────────────────────────────────────────────

class TestTextToChildren(unittest.TestCase):
    def test_plain_text(self):
        children = text_to_children("hello world")
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].value, "hello world")
        self.assertEqual(children[0].tag, TextType.TEXT)

    def test_bold(self):
        children = text_to_children("this is **bold** text")
        types = [c.tag for c in children]
        self.assertIn(TextType.BOLD, types)
        bold = next(c for c in children if c.tag == TextType.BOLD)
        self.assertEqual(bold.value, "bold")

    def test_italic(self):
        children = text_to_children("this is _italic_ text")
        types = [c.tag for c in children]
        self.assertIn(TextType.ITALIC, types)
        italic = next(c for c in children if c.tag == TextType.ITALIC)
        self.assertEqual(italic.value, "italic")

    def test_inline_code(self):
        children = text_to_children("use `print()` here")
        types = [c.tag for c in children]
        self.assertIn(TextType.CODE, types)
        code = next(c for c in children if c.tag == TextType.CODE)
        self.assertEqual(code.value, "print()")

    def test_link(self):
        children = text_to_children("[click](http://x.com)")
        link = next(c for c in children if c.tag == TextType.LINK)
        self.assertEqual(link.value, "click")
        self.assertEqual(link.props, {"href": "http://x.com"})

    def test_image(self):
        children = text_to_children("![alt](img.png)")
        img = next(c for c in children if c.tag == TextType.IMAGE)
        self.assertEqual(img.value, "alt")
        self.assertEqual(img.props, {"src": "img.png"})

    def test_mixed_inline(self):
        children = text_to_children("**bold** and _italic_ and `code`")
        types = {c.tag for c in children}
        self.assertIn(TextType.BOLD,   types)
        self.assertIn(TextType.ITALIC, types)
        self.assertIn(TextType.CODE,   types)

    def test_empty_string(self):
        self.assertEqual(text_to_children(""), [])


# ── MARKDOWN TO HTML NODE ─────────────────────────────────────────────────────

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_simple_paragraph(self):
        html = markdown_to_html_node("Hello world").to_html()
        self.assertIn("<p>", html)
        self.assertIn("Hello world", html)
        self.assertTrue(html.startswith("<div>"))

    def test_bold_in_paragraph(self):
        html = markdown_to_html_node("this is **bold** text").to_html()
        self.assertIn("<strong>bold</strong>", html)

    def test_italic_in_paragraph(self):
        html = markdown_to_html_node("this is _italic_ text").to_html()
        self.assertIn("<em>italic</em>", html)

    def test_inline_code_in_paragraph(self):
        html = markdown_to_html_node("use `print()` here").to_html()
        self.assertIn("<code>print()</code>", html)

    def test_code_block_raw(self):
        md   = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<pre><code>", html)
        self.assertIn("_should_", html)
        self.assertIn("**same**", html)
        self.assertNotIn("<em>", html)
        self.assertNotIn("<strong>", html)

    def test_code_block_no_extra_backticks(self):
        html = markdown_to_html_node("```\nsome code\n```").to_html()
        self.assertNotIn("```", html)

    def test_heading_h1(self):
        html = markdown_to_html_node("# Title").to_html()
        self.assertIn("<h1>", html)
        self.assertIn("Title", html)

    def test_heading_h2(self):
        html = markdown_to_html_node("## Subtitle").to_html()
        self.assertIn("<h2>", html)

    def test_unordered_list(self):
        html = markdown_to_html_node("- one\n- two\n- three").to_html()
        self.assertIn("<ul>", html)

    def test_ordered_list(self):
        html = markdown_to_html_node("1. first\n2. second").to_html()
        self.assertIn("<ol>", html)

    def test_quote(self):
        html = markdown_to_html_node("> a quote").to_html()
        self.assertIn("<blockquote>", html)

    def test_multiple_blocks(self):
        md   = "# Heading\n\nA paragraph\n\n```\ncode\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<h1>", html)
        self.assertIn("<p>", html)
        self.assertIn("<pre><code>", html)

    def test_wrapped_in_div(self):
        html = markdown_to_html_node("hello").to_html()
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))


if __name__ == "__main__":
    unittest.main()