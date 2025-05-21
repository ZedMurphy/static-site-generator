import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("I am Groot!", TextType.ITALIC, "http://my-site.com")
        node4 = TextNode("I am Groot!", TextType.ITALIC)
        self.assertNotEqual(node3, node4)
        node5 = TextNode("Exactly, Watson!", TextType.IMAGE, None)
        node6 = TextNode("Extactly, Watson!", TextType.IMAGE, None)
        self.assertNotEqual(node5, node6)
        node7 = TextNode("Don't panic!", TextType.CODE, None)
        node8 = TextNode("Don't panic!", TextType.CODE)
        self.assertEqual(node7, node8)
        node9 = TextNode("Hello World!", TextType.TEXT)
        node10 =TextNode("Hello World!", TextType.BOLD)
        self.assertNotEqual(node9, node10)

    def test_txt_node_to_html_node(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        html_node1 = text_node_to_html_node(node1)
        self.assertEqual(html_node1.tag, None)
        self.assertEqual(html_node1.value, "This is a text node")
        node2 = TextNode("This is a pretty image.", TextType.IMAGE, "https://my_image.com")
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "img")
        self.assertEqual(html_node2.value, "")
        self.assertEqual(html_node2.props, {"src": "https://my_image.com", "alt": "This is a pretty image."})
        node3 = TextNode("Click me!", TextType.LINK, "https://my_site.com")
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node3.tag, "a")
        self.assertEqual(html_node3.value, "Click me!")
        self.assertEqual(html_node3.props, {"href": "https://my_site.com"})

if __name__ == "__main__":
    unittest.main()