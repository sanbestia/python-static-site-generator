import re
import pytest
from enum import Enum
from textnode import TextNode, TextType
from text_functions import split_nodes_delimiter, split_nodes_image, split_nodes_link


# ── helpers ──────────────────────────────────────────────────────────────────

def T(text, tt=TextType.TEXT, url=None):
    """Shorthand TextNode constructor."""
    return TextNode(text, tt, url)


# ════════════════════════════════════════════════════════════════════════════
#  split_nodes_delimiter
# ════════════════════════════════════════════════════════════════════════════

class TestSplitNodesDelimiterValidation:

    def test_raises_on_text_type(self):
        with pytest.raises(ValueError, match="Invalid text type"):
            split_nodes_delimiter([T("hi")], "**", TextType.TEXT)

    def test_raises_on_link_type(self):
        with pytest.raises(ValueError):
            split_nodes_delimiter([T("hi")], "[", TextType.LINK)

    def test_raises_on_image_type(self):
        with pytest.raises(ValueError):
            split_nodes_delimiter([T("hi")], "!", TextType.IMAGE)

    def test_accepts_bold(self):
        result = split_nodes_delimiter([T("**b**")], "**", TextType.BOLD)
        assert any(n.text_type == TextType.BOLD for n in result)

    def test_accepts_italic(self):
        result = split_nodes_delimiter([T("_i_")], "_", TextType.ITALIC)
        assert any(n.text_type == TextType.ITALIC for n in result)

    def test_accepts_code(self):
        result = split_nodes_delimiter([T("`c`")], "`", TextType.CODE)
        assert any(n.text_type == TextType.CODE for n in result)


class TestSplitNodesDelimiterEmptyAndTrivial:

    def test_empty_list(self):
        assert split_nodes_delimiter([], "`", TextType.CODE) == []

    def test_plain_text_no_delimiter(self):
        node   = T("hello world")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [T("hello world")]

    def test_empty_string_node(self):
        node   = T("")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == []

    def test_only_delimiter_pair(self):
        node   = T("``")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [T("", TextType.CODE)]


class TestSplitNodesDelimiterCodeBasic:

    def test_single_code_span_middle(self):
        node   = T("hello `world` today")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [
            T("hello "),
            T("world", TextType.CODE),
            T(" today"),
        ]

    def test_code_at_start(self):
        node   = T("`code` after")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [
            T("code", TextType.CODE),
            T(" after"),
        ]

    def test_code_at_end(self):
        node   = T("before `code`")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [
            T("before "),
            T("code", TextType.CODE),
        ]

    def test_code_only(self):
        node   = T("`onlycode`")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [T("onlycode", TextType.CODE)]

    def test_multiple_code_spans(self):
        node   = T("`a` and `b`")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [
            T("a", TextType.CODE),
            T(" and "),
            T("b", TextType.CODE),
        ]

    def test_adjacent_code_spans(self):
        node   = T("`a``b`")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [
            T("a", TextType.CODE),
            T("b", TextType.CODE),
        ]


class TestSplitNodesDelimiterBold:

    def test_bold_basic(self):
        node   = T("this is **bold** text")
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert result == [
            T("this is "),
            T("bold", TextType.BOLD),
            T(" text"),
        ]

    def test_multiple_bold(self):
        node   = T("**a** and **b**")
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert result == [
            T("a", TextType.BOLD),
            T(" and "),
            T("b", TextType.BOLD),
        ]


class TestSplitNodesDelimiterItalic:

    def test_italic_basic(self):
        node   = T("this is _italic_ text")
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        assert result == [
            T("this is "),
            T("italic", TextType.ITALIC),
            T(" text"),
        ]

    def test_multiple_italic(self):
        node   = T("_a_ mid _b_")
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        assert result == [
            T("a", TextType.ITALIC),
            T(" mid "),
            T("b", TextType.ITALIC),
        ]


class TestSplitNodesDelimiterNonTextNodes:

    def test_non_text_node_is_passed_through(self):
        bold_node = T("already bold", TextType.BOLD)
        result    = split_nodes_delimiter([bold_node], "`", TextType.CODE)
        assert T("already bold", TextType.BOLD) in result

    def test_mixed_text_and_non_text(self):
        nodes  = [T("hello `x`"), T("img", TextType.IMAGE, "u.png")]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert T("hello ") in result
        assert T("x", TextType.CODE) in result
        assert T("img", TextType.IMAGE, "u.png") in result

    def test_multiple_plain_nodes(self):
        nodes  = [T("one `a` two"), T("three `b` four")]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert T("a", TextType.CODE) in result
        assert T("b", TextType.CODE) in result


class TestSplitNodesDelimiterEdgeCases:

    def test_whitespace_inside_delimiter(self):
        node   = T("` code `")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [T(" code ", TextType.CODE)]

    def test_delimiter_content_with_special_chars(self):
        node   = T("`x + y`")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [T("x + y", TextType.CODE)]

    def test_unmatched_delimiter_treated_as_plain(self):
        node   = T("hello `world")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert result == [T("hello `world")]

    def test_three_delimiters_first_pair_matches(self):
        node   = T("`a``b`")
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        assert T("a", TextType.CODE) in result
        assert T("b", TextType.CODE) in result


# ════════════════════════════════════════════════════════════════════════════
#  split_nodes_image
# ════════════════════════════════════════════════════════════════════════════

class TestSplitNodesImageEmptyAndTrivial:

    def test_empty_list(self):
        assert split_nodes_image([]) == []

    def test_no_image_in_text(self):
        assert split_nodes_image([T("plain text")]) == [T("plain text")]

    def test_empty_string(self):
        result = split_nodes_image([T("")])
        assert result == []


class TestSplitNodesImageBasic:

    def test_single_image_only(self):
        node   = T("![alt](url.png)")
        result = split_nodes_image([node])
        assert result == [T("alt", TextType.IMAGE, "url.png")]

    def test_image_in_middle(self):
        node   = T("before ![alt](url.png) after")
        result = split_nodes_image([node])
        assert result == [
            T("before "),
            T("alt", TextType.IMAGE, "url.png"),
            T(" after"),
        ]

    def test_image_at_start(self):
        node   = T("![alt](url.png) after")
        result = split_nodes_image([node])
        assert result == [
            T("alt", TextType.IMAGE, "url.png"),
            T(" after"),
        ]

    def test_image_at_end(self):
        node   = T("before ![alt](url.png)")
        result = split_nodes_image([node])
        assert result == [
            T("before "),
            T("alt", TextType.IMAGE, "url.png"),
        ]

    def test_multiple_images(self):
        node   = T("![a](a.png) and ![b](b.png)")
        result = split_nodes_image([node])
        assert result == [
            T("a", TextType.IMAGE, "a.png"),
            T(" and "),
            T("b", TextType.IMAGE, "b.png"),
        ]

    def test_adjacent_images(self):
        node   = T("![a](a.png)![b](b.png)")
        result = split_nodes_image([node])
        assert result == [
            T("a", TextType.IMAGE, "a.png"),
            T("b", TextType.IMAGE, "b.png"),
        ]


class TestSplitNodesImageAltAndUrl:

    def test_empty_alt_text(self):
        node   = T("![](url.png)")
        result = split_nodes_image([node])
        assert result == [T("", TextType.IMAGE, "url.png")]

    def test_empty_url(self):
        node   = T("![alt]()")
        result = split_nodes_image([node])
        assert result == [T("alt", TextType.IMAGE, "")]

    def test_alt_with_spaces(self):
        node   = T("![my photo](photo.jpg)")
        result = split_nodes_image([node])
        assert result == [T("my photo", TextType.IMAGE, "photo.jpg")]

    def test_url_with_query_string(self):
        node   = T("![alt](https://example.com/img?w=100&h=100)")
        result = split_nodes_image([node])
        assert result == [T("alt", TextType.IMAGE, "https://example.com/img?w=100&h=100")]

    def test_url_with_path(self):
        node   = T("![logo](/assets/images/logo.svg)")
        result = split_nodes_image([node])
        assert result == [T("logo", TextType.IMAGE, "/assets/images/logo.svg")]


class TestSplitNodesImageNonTextNodes:

    def test_non_text_node_passthrough(self):
        link_node = T("click", TextType.LINK, "http://x.com")
        result    = split_nodes_image([link_node])
        assert T("click", TextType.LINK, "http://x.com") in result

    def test_mixed_nodes(self):
        nodes  = [T("![a](a.png)"), T("bold", TextType.BOLD)]
        result = split_nodes_image(nodes)
        assert T("a", TextType.IMAGE, "a.png") in result
        assert T("bold", TextType.BOLD) in result

    def test_image_node_text_not_re_parsed(self):
        """An IMAGE node whose .text looks like markdown should NOT be re-split."""
        img_node = T("![not](reparsed.png)", TextType.IMAGE, "original.png")
        result   = split_nodes_image([img_node])
        assert T("![not](reparsed.png)", TextType.IMAGE, "original.png") in result


class TestSplitNodesImageEdgeCases:

    def test_link_without_bang_not_matched(self):
        node   = T("[not an image](url.png)")
        result = split_nodes_image([node])
        assert result == [T("[not an image](url.png)")]

    def test_image_followed_by_link(self):
        node   = T("![img](i.png)[link](l.com)")
        result = split_nodes_image([node])
        assert T("img", TextType.IMAGE, "i.png") in result
        assert T("[link](l.com)") in result

    def test_multiple_nodes_each_with_image(self):
        nodes  = [T("![a](a.png)"), T("![b](b.png)")]
        result = split_nodes_image(nodes)
        assert result == [
            T("a", TextType.IMAGE, "a.png"),
            T("b", TextType.IMAGE, "b.png"),
        ]

    def test_text_only_no_mutation(self):
        node   = T("just text")
        result = split_nodes_image([node])
        assert result == [T("just text")]
        assert result[0] is not node


# ════════════════════════════════════════════════════════════════════════════
#  split_nodes_link
# ════════════════════════════════════════════════════════════════════════════

class TestSplitNodesLinkEmptyAndTrivial:

    def test_empty_list(self):
        assert split_nodes_link([]) == []

    def test_no_link_in_text(self):
        assert split_nodes_link([T("plain text")]) == [T("plain text")]

    def test_empty_string(self):
        result = split_nodes_link([T("")])
        assert result == []


class TestSplitNodesLinkBasic:

    def test_single_link_only(self):
        node   = T("[click](http://x.com)")
        result = split_nodes_link([node])
        assert result == [T("click", TextType.LINK, "http://x.com")]

    def test_link_in_middle(self):
        node   = T("before [click](http://x.com) after")
        result = split_nodes_link([node])
        assert result == [
            T("before "),
            T("click", TextType.LINK, "http://x.com"),
            T(" after"),
        ]

    def test_link_at_start(self):
        node   = T("[link](url) after")
        result = split_nodes_link([node])
        assert result == [
            T("link", TextType.LINK, "url"),
            T(" after"),
        ]

    def test_link_at_end(self):
        node   = T("before [link](url)")
        result = split_nodes_link([node])
        assert result == [
            T("before "),
            T("link", TextType.LINK, "url"),
        ]

    def test_multiple_links(self):
        node   = T("[a](u1) and [b](u2)")
        result = split_nodes_link([node])
        assert result == [
            T("a", TextType.LINK, "u1"),
            T(" and "),
            T("b", TextType.LINK, "u2"),
        ]

    def test_adjacent_links(self):
        node   = T("[a](u1)[b](u2)")
        result = split_nodes_link([node])
        assert result == [
            T("a", TextType.LINK, "u1"),
            T("b", TextType.LINK, "u2"),
        ]


class TestSplitNodesLinkTextAndUrl:

    def test_empty_link_text(self):
        node   = T("[](url)")
        result = split_nodes_link([node])
        assert result == [T("", TextType.LINK, "url")]

    def test_empty_url(self):
        node   = T("[text]()")
        result = split_nodes_link([node])
        assert result == [T("text", TextType.LINK, "")]

    def test_link_text_with_spaces(self):
        node   = T("[click here](http://x.com)")
        result = split_nodes_link([node])
        assert result == [T("click here", TextType.LINK, "http://x.com")]

    def test_url_with_query_string(self):
        node   = T("[search](https://g.com?q=python)")
        result = split_nodes_link([node])
        assert result == [T("search", TextType.LINK, "https://g.com?q=python")]

    def test_url_with_fragment(self):
        node   = T("[section](#intro)")
        result = split_nodes_link([node])
        assert result == [T("section", TextType.LINK, "#intro")]


class TestSplitNodesLinkImageExclusion:

    def test_image_syntax_not_matched_as_link(self):
        node   = T("![alt](img.png)")
        result = split_nodes_link([node])
        assert result == [T("![alt](img.png)")]

    def test_image_and_link_together(self):
        node   = T("![img](i.png) [link](l.com)")
        result = split_nodes_link([node])
        assert T("link", TextType.LINK, "l.com") in result
        assert T("![img](i.png) ") in result

    def test_link_immediately_after_image(self):
        node   = T("![img](i.png)[link](l.com)")
        result = split_nodes_link([node])
        assert T("link", TextType.LINK, "l.com") in result


class TestSplitNodesLinkNonTextNodes:

    def test_non_text_node_passthrough(self):
        img_node = T("photo", TextType.IMAGE, "p.png")
        result   = split_nodes_link([img_node])
        assert T("photo", TextType.IMAGE, "p.png") in result

    def test_link_node_not_re_parsed(self):
        link_node = T("[not](reparsed)", TextType.LINK, "original")
        result    = split_nodes_link([link_node])
        assert T("[not](reparsed)", TextType.LINK, "original") in result

    def test_mixed_nodes(self):
        nodes  = [T("[a](u1)"), T("bold", TextType.BOLD)]
        result = split_nodes_link(nodes)
        assert T("a", TextType.LINK, "u1") in result
        assert T("bold", TextType.BOLD) in result


class TestSplitNodesLinkEdgeCases:

    def test_multiple_nodes_each_with_link(self):
        nodes  = [T("[a](u1)"), T("[b](u2)")]
        result = split_nodes_link(nodes)
        assert result == [
            T("a", TextType.LINK, "u1"),
            T("b", TextType.LINK, "u2"),
        ]

    def test_text_only_no_mutation(self):
        node   = T("just text")
        result = split_nodes_link([node])
        assert result == [T("just text")]

    def test_nested_brackets_outermost_match(self):
        node   = T("[a [b]](url)")
        result = split_nodes_link([node])
        assert any(n.text_type == TextType.LINK for n in result)


# ════════════════════════════════════════════════════════════════════════════
#  Cross-function integration tests
# ════════════════════════════════════════════════════════════════════════════

class TestCrossFunctionIntegration:

    def test_delimiter_then_image(self):
        nodes  = [T("Use `code` and ![pic](p.png) done")]
        after_delim = split_nodes_delimiter(nodes, "`", TextType.CODE)
        after_image = split_nodes_image(after_delim)
        types = [n.text_type for n in after_image]
        assert TextType.CODE  in types
        assert TextType.IMAGE in types
        assert TextType.TEXT  in types

    def test_delimiter_then_link(self):
        nodes  = [T("Click [here](u) or use `code`")]
        after_delim = split_nodes_delimiter(nodes, "`", TextType.CODE)
        after_link  = split_nodes_link(after_delim)
        types = [n.text_type for n in after_link]
        assert TextType.CODE in types
        assert TextType.LINK in types

    def test_image_and_link_pipeline(self):
        nodes  = [T("![img](i.png) [link](l.com) tail")]
        after_image = split_nodes_image(nodes)
        after_link  = split_nodes_link(after_image)
        assert T("img", TextType.IMAGE, "i.png") in after_link
        assert T("link", TextType.LINK, "l.com") in after_link

    def test_full_pipeline(self):
        nodes = [T("**bold** `code` ![pic](p.png) [link](l.com)")]
        step1 = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        step2 = split_nodes_delimiter(step1, "`", TextType.CODE)
        step3 = split_nodes_image(step2)
        step4 = split_nodes_link(step3)
        types = {n.text_type for n in step4}
        assert TextType.BOLD  in types
        assert TextType.CODE  in types
        assert TextType.IMAGE in types
        assert TextType.LINK  in types