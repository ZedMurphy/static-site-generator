import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node1 = HTMLNode("a", "This is a link to Google.", None, {"href": "https://www.google.com"})
        output1 = ' href="https://www.google.com"'
        self.assertEqual(node1.props_to_html(), output1)

        node2 = HTMLNode("p", "This is a paragraph.", node1, None)
        output2 = None
        self.assertNotEqual(node2.props_to_html(), output2)

        node3 = HTMLNode("h1", "This is a heading.", node2, {"style": "text-align:right"})
        output3 = ' style="text-align:right"'
        self.assertEqual(node3.props_to_html(), output3)

        node4 = HTMLNode("p", "Some text.", None, {})
        node5 = HTMLNode("p", "Some text.")
        self.assertEqual(node4.props_to_html(), node5.props_to_html())

        node6 = HTMLNode("a", "Don't panic!", None, {"href": "https://www.google.com", "style": "font-weight: bold;"})
        self.assertEqual(node6.props_to_html(), ' href="https://www.google.com" style="font-weight: bold;"')


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        leaf_node1 = LeafNode("p", "Hello, world!")
        self.assertEqual(leaf_node1.to_html(), "<p>Hello, world!</p>")

        leaf_node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf_node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

        leaf_node3 = LeafNode("h1", "First heading")
        self.assertEqual(leaf_node3.to_html(), "<h1>First heading</h1>")

        leaf_node4 = LeafNode(None, "my value")
        self.assertEqual(leaf_node4.to_html(), "my value")

        with self.assertRaises(ValueError) as context:
            leaf_node5 = LeafNode(None, "")
            leaf_node5.to_html()
        self.assertEqual(str(context.exception), "Nothing to print (no value given).")


if __name__ == "__main__":
    unittest.main()