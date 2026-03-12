import unittest
from textnode import TextNode, TextType
from text_functions import split_nodes_delimiter, split_nodes_image, split_nodes_link


def T(text, tt=TextType.TEXT, url=None):
    return TextNode(text, tt, url)


# ════════════════════════════════════════════════════════════════════════════
#  split_nodes_delimiter
# ════════════════════════════════════════════════════════════════════════════

class TestSplitNodesDelimiterValidation(unittest.TestCase):
    def test_raises_on_text_type(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([T("hi")], "**", TextType.TEXT)

    def test_raises_on_link_type(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([T("hi")], "[", TextType.LINK)

    def test_raises_on_image_type(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter([T("hi")], "!", TextType.IMAGE)

    def test_accepts_bold(self):
        result = split_nodes_delimiter([T("**b**")], "**", TextType.BOLD)
        self.assertTrue(any(n.text_type == TextType.BOLD for n in result))

    def test_accepts_italic(self):
        result = split_nodes_delimiter([T("_i_")], "_", TextType.ITALIC)
        self.assertTrue(any(n.text_type == TextType.ITALIC for n in result))

    def test_accepts_code(self):
        result = split_nodes_delimiter([T("`c`")], "`", TextType.CODE)
        self.assertTrue(any(n.text_type == TextType.CODE for n in result))


class TestSplitNodesDelimiterEmptyAndTrivial(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_plain_text_no_delimiter(self):
        result = split_nodes_delimiter([T("hello world")], "`", TextType.CODE)
        self.assertEqual(result, [T("hello world")])

    def test_empty_string_node(self):
        result = split_nodes_delimiter([T("")], "`", TextType.CODE)
        self.assertEqual(result, [])

    def test_only_delimiter_pair(self):
        result = split_nodes_delimiter([T("``")], "`", TextType.CODE)
        self.assertEqual(result, [T("", TextType.CODE)])


class TestSplitNodesDelimiterCodeBasic(unittest.TestCase):
    def test_single_code_span_middle(self):
        result = split_nodes_delimiter([T("hello `world` today")], "`", TextType.CODE)
        self.assertEqual(result, [T("hello "), T("world", TextType.CODE), T(" today")])

    def test_code_at_start(self):
        result = split_nodes_delimiter([T("`code` after")], "`", TextType.CODE)
        self.assertEqual(result, [T("code", TextType.CODE), T(" after")])

    def test_code_at_end(self):
        result = split_nodes_delimiter([T("before `code`")], "`", TextType.CODE)
        self.assertEqual(result, [T("before "), T("code", TextType.CODE)])

    def test_code_only(self):
        result = split_nodes_delimiter([T("`onlycode`")], "`", TextType.CODE)
        self.assertEqual(result, [T("onlycode", TextType.CODE)])

    def test_multiple_code_spans(self):
        result = split_nodes_delimiter([T("`a` and `b`")], "`", TextType.CODE)
        self.assertEqual(result, [T("a", TextType.CODE), T(" and "), T("b", TextType.CODE)])

    def test_adjacent_code_spans(self):
        result = split_nodes_delimiter([T("`a``b`")], "`", TextType.CODE)
        self.assertEqual(result, [T("a", TextType.CODE), T("b", TextType.CODE)])


class TestSplitNodesDelimiterBold(unittest.TestCase):
    def test_bold_basic(self):
        result = split_nodes_delimiter([T("this is **bold** text")], "**", TextType.BOLD)
        self.assertEqual(result, [T("this is "), T("bold", TextType.BOLD), T(" text")])

    def test_multiple_bold(self):
        result = split_nodes_delimiter([T("**a** and **b**")], "**", TextType.BOLD)
        self.assertEqual(result, [T("a", TextType.BOLD), T(" and "), T("b", TextType.BOLD)])


class TestSplitNodesDelimiterItalic(unittest.TestCase):
    def test_italic_basic(self):
        result = split_nodes_delimiter([T("this is _italic_ text")], "_", TextType.ITALIC)
        self.assertEqual(result, [T("this is "), T("italic", TextType.ITALIC), T(" text")])

    def test_multiple_italic(self):
        result = split_nodes_delimiter([T("_a_ mid _b_")], "_", TextType.ITALIC)
        self.assertEqual(result, [T("a", TextType.ITALIC), T(" mid "), T("b", TextType.ITALIC)])


class TestSplitNodesDelimiterNonTextNodes(unittest.TestCase):
    def test_non_text_node_is_passed_through(self):
        result = split_nodes_delimiter([T("already bold", TextType.BOLD)], "`", TextType.CODE)
        self.assertIn(T("already bold", TextType.BOLD), result)

    def test_mixed_text_and_non_text(self):
        nodes  = [T("hello `x`"), T("img", TextType.IMAGE, "u.png")]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertIn(T("hello "), result)
        self.assertIn(T("x", TextType.CODE), result)
        self.assertIn(T("img", TextType.IMAGE, "u.png"), result)

    def test_multiple_plain_nodes(self):
        nodes  = [T("one `a` two"), T("three `b` four")]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertIn(T("a", TextType.CODE), result)
        self.assertIn(T("b", TextType.CODE), result)


class TestSplitNodesDelimiterEdgeCases(unittest.TestCase):
    def test_whitespace_inside_delimiter(self):
        result = split_nodes_delimiter([T("` code `")], "`", TextType.CODE)
        self.assertEqual(result, [T(" code ", TextType.CODE)])

    def test_delimiter_content_with_special_chars(self):
        result = split_nodes_delimiter([T("`x + y`")], "`", TextType.CODE)
        self.assertEqual(result, [T("x + y", TextType.CODE)])

    def test_unmatched_delimiter_treated_as_plain(self):
        result = split_nodes_delimiter([T("hello `world")], "`", TextType.CODE)
        self.assertEqual(result, [T("hello `world")])

    def test_three_delimiters_first_pair_matches(self):
        result = split_nodes_delimiter([T("`a``b`")], "`", TextType.CODE)
        self.assertIn(T("a", TextType.CODE), result)
        self.assertIn(T("b", TextType.CODE), result)


# ════════════════════════════════════════════════════════════════════════════
#  split_nodes_image
# ════════════════════════════════════════════════════════════════════════════

class TestSplitNodesImageEmptyAndTrivial(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_no_image_in_text(self):
        self.assertEqual(split_nodes_image([T("plain text")]), [T("plain text")])

    def test_empty_string(self):
        self.assertEqual(split_nodes_image([T("")]), [])


class TestSplitNodesImageBasic(unittest.TestCase):
    def test_single_image_only(self):
        result = split_nodes_image([T("![alt](url.png)")])
        self.assertEqual(result, [T("alt", TextType.IMAGE, "url.png")])

    def test_image_in_middle(self):
        result = split_nodes_image([T("before ![alt](url.png) after")])
        self.assertEqual(result, [T("before "), T("alt", TextType.IMAGE, "url.png"), T(" after")])

    def test_image_at_start(self):
        result = split_nodes_image([T("![alt](url.png) after")])
        self.assertEqual(result, [T("alt", TextType.IMAGE, "url.png"), T(" after")])

    def test_image_at_end(self):
        result = split_nodes_image([T("before ![alt](url.png)")])
        self.assertEqual(result, [T("before "), T("alt", TextType.IMAGE, "url.png")])

    def test_multiple_images(self):
        result = split_nodes_image([T("![a](a.png) and ![b](b.png)")])
        self.assertEqual(result, [T("a", TextType.IMAGE, "a.png"), T(" and "), T("b", TextType.IMAGE, "b.png")])

    def test_adjacent_images(self):
        result = split_nodes_image([T("![a](a.png)![b](b.png)")])
        self.assertEqual(result, [T("a", TextType.IMAGE, "a.png"), T("b", TextType.IMAGE, "b.png")])


class TestSplitNodesImageAltAndUrl(unittest.TestCase):
    def test_empty_alt_text(self):
        result = split_nodes_image([T("![](url.png)")])
        self.assertEqual(result, [T("", TextType.IMAGE, "url.png")])

    def test_empty_url(self):
        result = split_nodes_image([T("![alt]()")])
        self.assertEqual(result, [T("alt", TextType.IMAGE, "")])

    def test_alt_with_spaces(self):
        result = split_nodes_image([T("![my photo](photo.jpg)")])
        self.assertEqual(result, [T("my photo", TextType.IMAGE, "photo.jpg")])

    def test_url_with_query_string(self):
        result = split_nodes_image([T("![alt](https://example.com/img?w=100&h=100)")])
        self.assertEqual(result, [T("alt", TextType.IMAGE, "https://example.com/img?w=100&h=100")])

    def test_url_with_path(self):
        result = split_nodes_image([T("![logo](/assets/images/logo.svg)")])
        self.assertEqual(result, [T("logo", TextType.IMAGE, "/assets/images/logo.svg")])


class TestSplitNodesImageNonTextNodes(unittest.TestCase):
    def test_non_text_node_passthrough(self):
        result = split_nodes_image([T("click", TextType.LINK, "http://x.com")])
        self.assertIn(T("click", TextType.LINK, "http://x.com"), result)

    def test_mixed_nodes(self):
        result = split_nodes_image([T("![a](a.png)"), T("bold", TextType.BOLD)])
        self.assertIn(T("a", TextType.IMAGE, "a.png"), result)
        self.assertIn(T("bold", TextType.BOLD), result)

    def test_image_node_text_not_re_parsed(self):
        img_node = T("![not](reparsed.png)", TextType.IMAGE, "original.png")
        result   = split_nodes_image([img_node])
        self.assertIn(T("![not](reparsed.png)", TextType.IMAGE, "original.png"), result)


class TestSplitNodesImageEdgeCases(unittest.TestCase):
    def test_link_without_bang_not_matched(self):
        result = split_nodes_image([T("[not an image](url.png)")])
        self.assertEqual(result, [T("[not an image](url.png)")])

    def test_image_followed_by_link(self):
        result = split_nodes_image([T("![img](i.png)[link](l.com)")])
        self.assertIn(T("img", TextType.IMAGE, "i.png"), result)
        self.assertIn(T("[link](l.com)"), result)

    def test_multiple_nodes_each_with_image(self):
        result = split_nodes_image([T("![a](a.png)"), T("![b](b.png)")])
        self.assertEqual(result, [T("a", TextType.IMAGE, "a.png"), T("b", TextType.IMAGE, "b.png")])

    def test_text_only_no_mutation(self):
        node   = T("just text")
        result = split_nodes_image([node])
        self.assertEqual(result, [T("just text")])
        self.assertIsNot(result[0], node)


# ════════════════════════════════════════════════════════════════════════════
#  split_nodes_link
# ════════════════════════════════════════════════════════════════════════════

class TestSplitNodesLinkEmptyAndTrivial(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(split_nodes_link([]), [])

    def test_no_link_in_text(self):
        self.assertEqual(split_nodes_link([T("plain text")]), [T("plain text")])

    def test_empty_string(self):
        self.assertEqual(split_nodes_link([T("")]), [])


class TestSplitNodesLinkBasic(unittest.TestCase):
    def test_single_link_only(self):
        result = split_nodes_link([T("[click](http://x.com)")])
        self.assertEqual(result, [T("click", TextType.LINK, "http://x.com")])

    def test_link_in_middle(self):
        result = split_nodes_link([T("before [click](http://x.com) after")])
        self.assertEqual(result, [T("before "), T("click", TextType.LINK, "http://x.com"), T(" after")])

    def test_link_at_start(self):
        result = split_nodes_link([T("[link](url) after")])
        self.assertEqual(result, [T("link", TextType.LINK, "url"), T(" after")])

    def test_link_at_end(self):
        result = split_nodes_link([T("before [link](url)")])
        self.assertEqual(result, [T("before "), T("link", TextType.LINK, "url")])

    def test_multiple_links(self):
        result = split_nodes_link([T("[a](u1) and [b](u2)")])
        self.assertEqual(result, [T("a", TextType.LINK, "u1"), T(" and "), T("b", TextType.LINK, "u2")])

    def test_adjacent_links(self):
        result = split_nodes_link([T("[a](u1)[b](u2)")])
        self.assertEqual(result, [T("a", TextType.LINK, "u1"), T("b", TextType.LINK, "u2")])


class TestSplitNodesLinkTextAndUrl(unittest.TestCase):
    def test_empty_link_text(self):
        result = split_nodes_link([T("[](url)")])
        self.assertEqual(result, [T("", TextType.LINK, "url")])

    def test_empty_url(self):
        result = split_nodes_link([T("[text]()")])
        self.assertEqual(result, [T("text", TextType.LINK, "")])

    def test_link_text_with_spaces(self):
        result = split_nodes_link([T("[click here](http://x.com)")])
        self.assertEqual(result, [T("click here", TextType.LINK, "http://x.com")])

    def test_url_with_query_string(self):
        result = split_nodes_link([T("[search](https://g.com?q=python)")])
        self.assertEqual(result, [T("search", TextType.LINK, "https://g.com?q=python")])

    def test_url_with_fragment(self):
        result = split_nodes_link([T("[section](#intro)")])
        self.assertEqual(result, [T("section", TextType.LINK, "#intro")])


class TestSplitNodesLinkImageExclusion(unittest.TestCase):
    def test_image_syntax_not_matched_as_link(self):
        result = split_nodes_link([T("![alt](img.png)")])
        self.assertEqual(result, [T("![alt](img.png)")])

    def test_image_and_link_together(self):
        result = split_nodes_link([T("![img](i.png) [link](l.com)")])
        self.assertIn(T("link", TextType.LINK, "l.com"), result)
        self.assertIn(T("![img](i.png) "), result)

    def test_link_immediately_after_image(self):
        result = split_nodes_link([T("![img](i.png)[link](l.com)")])
        self.assertIn(T("link", TextType.LINK, "l.com"), result)


class TestSplitNodesLinkNonTextNodes(unittest.TestCase):
    def test_non_text_node_passthrough(self):
        result = split_nodes_link([T("photo", TextType.IMAGE, "p.png")])
        self.assertIn(T("photo", TextType.IMAGE, "p.png"), result)

    def test_link_node_not_re_parsed(self):
        result = split_nodes_link([T("[not](reparsed)", TextType.LINK, "original")])
        self.assertIn(T("[not](reparsed)", TextType.LINK, "original"), result)

    def test_mixed_nodes(self):
        result = split_nodes_link([T("[a](u1)"), T("bold", TextType.BOLD)])
        self.assertIn(T("a", TextType.LINK, "u1"), result)
        self.assertIn(T("bold", TextType.BOLD), result)


class TestSplitNodesLinkEdgeCases(unittest.TestCase):
    def test_multiple_nodes_each_with_link(self):
        result = split_nodes_link([T("[a](u1)"), T("[b](u2)")])
        self.assertEqual(result, [T("a", TextType.LINK, "u1"), T("b", TextType.LINK, "u2")])

    def test_text_only_no_mutation(self):
        result = split_nodes_link([T("just text")])
        self.assertEqual(result, [T("just text")])

    def test_nested_brackets_outermost_match(self):
        result = split_nodes_link([T("[a [b]](url)")])
        self.assertTrue(any(n.text_type == TextType.LINK for n in result))


# ════════════════════════════════════════════════════════════════════════════
#  Cross-function integration tests
# ════════════════════════════════════════════════════════════════════════════

class TestCrossFunctionIntegration(unittest.TestCase):
    def test_delimiter_then_image(self):
        nodes       = [T("Use `code` and ![pic](p.png) done")]
        after_delim = split_nodes_delimiter(nodes, "`", TextType.CODE)
        after_image = split_nodes_image(after_delim)
        types = [n.text_type for n in after_image]
        self.assertIn(TextType.CODE,  types)
        self.assertIn(TextType.IMAGE, types)
        self.assertIn(TextType.TEXT,  types)

    def test_delimiter_then_link(self):
        nodes       = [T("Click [here](u) or use `code`")]
        after_delim = split_nodes_delimiter(nodes, "`", TextType.CODE)
        after_link  = split_nodes_link(after_delim)
        types = [n.text_type for n in after_link]
        self.assertIn(TextType.CODE, types)
        self.assertIn(TextType.LINK, types)

    def test_image_and_link_pipeline(self):
        nodes       = [T("![img](i.png) [link](l.com) tail")]
        after_image = split_nodes_image(nodes)
        after_link  = split_nodes_link(after_image)
        self.assertIn(T("img",  TextType.IMAGE, "i.png"),  after_link)
        self.assertIn(T("link", TextType.LINK,  "l.com"),  after_link)

    def test_full_pipeline(self):
        nodes = [T("**bold** `code` ![pic](p.png) [link](l.com)")]
        step1 = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        step2 = split_nodes_delimiter(step1, "`",  TextType.CODE)
        step3 = split_nodes_image(step2)
        step4 = split_nodes_link(step3)
        types = {n.text_type for n in step4}
        self.assertIn(TextType.BOLD,  types)
        self.assertIn(TextType.CODE,  types)
        self.assertIn(TextType.IMAGE, types)
        self.assertIn(TextType.LINK,  types)


if __name__ == "__main__":
    unittest.main()