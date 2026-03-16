import pytest
from raw_to_html_functions import (
    raw_to_html_paragraph,
    raw_to_html_heading,
    raw_to_html_bold,
    raw_to_html_italic,
    raw_to_html_link,
    raw_to_html_image,
    raw_to_html_unordered_list,
    raw_to_html_ordered_list,
    raw_to_html_list_item,
    raw_to_html_quote,
    raw_to_html_code_oneliner,
    raw_to_html_codeblock,
    raw_to_html_div,
    raw_to_html_span,
)


class TestParagraph:
    def test_basic(self):
        assert raw_to_html_paragraph("Hello, world!") == "<p>Hello, world!</p>"

    def test_newlines_replaced_with_spaces(self):
        assert raw_to_html_paragraph("line one\nline two") == "<p>line one line two</p>"

    def test_multiple_newlines(self):
        assert raw_to_html_paragraph("a\nb\nc") == "<p>a b c</p>"

    def test_empty_string(self):
        assert raw_to_html_paragraph("") == "<p></p>"


class TestHeading:
    def test_h1(self):
        assert raw_to_html_heading("# Hello", 1) == "<h1>Hello</h1>"

    def test_h2(self):
        assert raw_to_html_heading("## Hello", 2) == "<h2>Hello</h2>"

    def test_h3(self):
        assert raw_to_html_heading("### Hello", 3) == "<h3>Hello</h3>"

    def test_h4(self):
        assert raw_to_html_heading("#### Hello", 4) == "<h4>Hello</h4>"

    def test_h5(self):
        assert raw_to_html_heading("##### Hello", 5) == "<h5>Hello</h5>"

    def test_h6(self):
        assert raw_to_html_heading("###### Hello", 6) == "<h6>Hello</h6>"

    def test_level_zero_raises(self):
        with pytest.raises(ValueError):
            raw_to_html_heading("Hello", 0)

    def test_level_seven_raises(self):
        with pytest.raises(ValueError):
            raw_to_html_heading("Hello", 7)

    def test_negative_level_raises(self):
        with pytest.raises(ValueError):
            raw_to_html_heading("Hello", -1)


class TestBold:
    def test_basic(self):
        assert raw_to_html_bold("bold text") == "<b>bold text</b>"

    def test_empty_string(self):
        assert raw_to_html_bold("") == "<b></b>"


class TestItalic:
    def test_basic(self):
        assert raw_to_html_italic("italic text") == "<i>italic text</i>"

    def test_empty_string(self):
        assert raw_to_html_italic("") == "<i></i>"


class TestLink:
    def test_basic(self):
        assert raw_to_html_link("Click me", "https://example.com") == '<a href="https://example.com">Click me</a>'

    def test_empty_text(self):
        assert raw_to_html_link("", "https://example.com") == '<a href="https://example.com"></a>'

    def test_empty_href(self):
        assert raw_to_html_link("Click me", "") == '<a href="">Click me</a>'


class TestImage:
    def test_basic(self):
        assert raw_to_html_image("alt text", "image.png") == '<img src="image.png" alt="alt text">'

    def test_empty_alt(self):
        assert raw_to_html_image("", "image.png") == '<img src="image.png" alt="">'

    def test_empty_src(self):
        assert raw_to_html_image("alt text", "") == '<img src="" alt="alt text">'


class TestUnorderedList:
    def test_basic(self):
        assert raw_to_html_unordered_list("<li>item</li>") == "<ul>\n<li>item</li></ul>"

    def test_multiple_items(self):
        inner = "<li>one</li><li>two</li>"
        assert raw_to_html_unordered_list(inner) == f"<ul>\n{inner}</ul>"

    def test_empty(self):
        assert raw_to_html_unordered_list("") == "<ul>\n</ul>"


class TestOrderedList:
    def test_basic(self):
        assert raw_to_html_ordered_list("<li>item</li>") == "<ol>\n<li>item</li></ol>"

    def test_multiple_items(self):
        inner = "<li>one</li><li>two</li>"
        assert raw_to_html_ordered_list(inner) == f"<ol>\n{inner}</ol>"

    def test_empty(self):
        assert raw_to_html_ordered_list("") == "<ol>\n</ol>"


class TestListItem:
    def test_basic(self):
        assert raw_to_html_list_item("item text") == "<li>item text</li>"

    def test_empty(self):
        assert raw_to_html_list_item("") == "<li></li>"


class TestQuote:
    def test_basic(self):
        assert raw_to_html_quote("quoted text") == "<blockquote>quoted text</blockquote>"

    def test_empty(self):
        assert raw_to_html_quote("") == "<blockquote></blockquote>"


class TestCodeOneliner:
    def test_basic(self):
        assert raw_to_html_code_oneliner("x = 1") == "<code>x = 1</code>"

    def test_empty(self):
        assert raw_to_html_code_oneliner("") == "<code></code>"


class TestCodeblock:
    def test_basic(self):
        assert raw_to_html_codeblock("x = 1") == "<pre><code>x = 1</code></pre>"

    def test_multiline(self):
        code = "x = 1\ny = 2"
        assert raw_to_html_codeblock(code) == f"<pre><code>{code}</code></pre>"

    def test_empty(self):
        assert raw_to_html_codeblock("") == "<pre><code></code></pre>"


class TestDiv:
    def test_basic(self):
        assert raw_to_html_div("content") == "<div>content</div>"

    def test_empty(self):
        assert raw_to_html_div("") == "<div></div>"

    def test_nested(self):
        assert raw_to_html_div("<p>inner</p>") == "<div><p>inner</p></div>"


class TestSpan:
    def test_basic(self):
        assert raw_to_html_span("text") == "<span>text</span>"

    def test_empty(self):
        assert raw_to_html_span("") == "<span></span>"
