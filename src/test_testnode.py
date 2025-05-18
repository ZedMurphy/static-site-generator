import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
        node3 = TextNode("I am Groot!", TextType.ITALIC_TEXT, "http://my-site.de")
        node4 = TextNode("I am Groot!", TextType.ITALIC_TEXT)
        self.assertNotEqual(node3, node4)
        node5 = TextNode("Exactly, Watson!", TextType.IMAGE, None)
        node6 = TextNode("Extactly, Watson!", TextType.IMAGE, None)
        self.assertNotEqual(node5, node6)
        node7 = TextNode("Don't panic!", TextType.CODE_TEXT, None)
        node8 = TextNode("Don't panic!", TextType.CODE_TEXT)
        self.assertEqual(node7, node8)
        node9 = TextNode("Hello World!", TextType.NORMAL_TEXT)
        node10 =TextNode("Hello World!", TextType.BOLD_TEXT)
        self.assertNotEqual(node9, node10)


if __name__ == "__main__":
    unittest.main()