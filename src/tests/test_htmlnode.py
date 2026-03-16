import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_raises_notImplementedError(self):
        node = HTMLNode(
            tag="p", 
            value="bold words",
            props={"href": "https://www.google.com",
                   "target": "_blank"}
            )
        with self.assertRaises(NotImplementedError):
            node.to_html()
        
 
    def test_props_to_html(self):
        node = HTMLNode(
            tag="p", 
            value="bold words",
            props={"href": "https://www.google.com",
                   "target": "_blank"}
            )
        html = node.props_to_html()
        self.assertEqual(html, "href:https://www.google.com target:_blank")
        

    def test_repr(self):
        node = HTMLNode(
            tag="p",
            value="bold words",
            props={"href": "https://www.google.com",
                   "target": "_blank"}
            )
        self.assertEqual(str(node),
                         "HTMLNode(tag=p, value=bold words, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})")

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p", value="text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="a", value="link", props={"href": "https://x.com"})
        self.assertEqual(node.props_to_html(), "href:https://x.com")

    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


if __name__ == "__main__":
    unittest.main()