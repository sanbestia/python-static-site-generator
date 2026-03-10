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
        print(str(node))
        self.assertEqual(str(node), 
                         "HTMLNode(tag=p, value=bold words, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})")


if __name__ == "__main__":
    unittest.main()