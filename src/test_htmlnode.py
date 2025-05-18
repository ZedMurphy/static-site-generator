import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode("<a>", "This is a link to Google.", None, {"href": "https://www.google.com"})
        output1 = ' href="https://www.google.com"'
        self.assertEqual(node1.props_to_html(), output1)
        node2 = HTMLNode("<p>", "This is a paragraph.", node1, None)
        output2 = None
        self.assertNotEqual(node2.props_to_html(), output2)
        node3 = HTMLNode("<h1>", "This is a heading.", node2, {"style": "text-align:right"})
        output3 = ' style="text-align:right"'
        self.assertEqual(node3.props_to_html(), output3)

if __name__ == "__main__":
    unittest.main()