import unittest

from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from markdownextraction import extract_markdown_images, extract_markdown_links
from textnode import TextType, TextNode


class TestSplitNodes(unittest.TestCase):

    def test_split_nodes_delimiter_with_code(self):
        old_nodes = [
            TextNode("Hi, my name is Fred. `This is some code.` And that is George `and his code.`", TextType.TEXT), 
            TextNode("This is a paragraph.", TextType.TEXT), 
            TextNode("Here be some code.", TextType.CODE)
        ]
        
        expected_nodes = [
            TextNode("Hi, my name is Fred. ", TextType.TEXT), 
            TextNode("This is some code.", TextType.CODE), 
            TextNode(" And that is George ", TextType.TEXT),
            TextNode("and his code.", TextType.CODE),
            TextNode("This is a paragraph.", TextType.TEXT),
            TextNode("Here be some code.", TextType.CODE)
        ]
        
        result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        
        # Compare each node's properties
        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected_nodes[i].text)
            self.assertEqual(result[i].text_type, expected_nodes[i].text_type)


    def test_split_nodes_delimiter_with_bold(self):
        old_nodes = [
            TextNode("Hi, my name is Fred. **Sometimes I like to emphasise things.** And that is George **and his emphasised message.**", TextType.TEXT), 
            TextNode("This is a paragraph.", TextType.TEXT), 
            TextNode("Here be another emphasis.", TextType.BOLD)
        ]
        
        expected_nodes = [
            TextNode("Hi, my name is Fred. ", TextType.TEXT), 
            TextNode("Sometimes I like to emphasise things.", TextType.BOLD), 
            TextNode(" And that is George ", TextType.TEXT),
            TextNode("and his emphasised message.", TextType.BOLD),
            TextNode("This is a paragraph.", TextType.TEXT),
            TextNode("Here be another emphasis.", TextType.BOLD)
        ]
        
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        
        # Compare each node's properties
        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected_nodes[i].text)
            self.assertEqual(result[i].text_type, expected_nodes[i].text_type)

    
    def test_split_nodes_delimiter_with_italic(self):
        old_nodes = [
            TextNode("Hi, my name is Fred. _Sometimes I like to emphasise things._ And that is George _and his emphasised message._", TextType.TEXT), 
            TextNode("This is a paragraph.", TextType.TEXT), 
            TextNode("Here be another emphasis.", TextType.ITALIC)
        ]
        
        expected_nodes = [
            TextNode("Hi, my name is Fred. ", TextType.TEXT), 
            TextNode("Sometimes I like to emphasise things.", TextType.ITALIC), 
            TextNode(" And that is George ", TextType.TEXT),
            TextNode("and his emphasised message.", TextType.ITALIC),
            TextNode("This is a paragraph.", TextType.TEXT),
            TextNode("Here be another emphasis.", TextType.ITALIC)
        ]
        
        result = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        
        # Compare each node's properties
        self.assertEqual(len(result), len(expected_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected_nodes[i].text)
            self.assertEqual(result[i].text_type, expected_nodes[i].text_type)


    def test_no_delimiters(self):
        # Test when there are no delimiters to be found
        old_nodes = [
            TextNode("This text has no delimiters at all", TextType.TEXT)
        ]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This text has no delimiters at all")
        self.assertEqual(result[0].text_type, TextType.TEXT)


    def test_missing_closing_delimiter(self):
        # Test that an exception is raised for unclosed delimiters
        old_nodes = [
            TextNode("This text has an unclosed **delimiter", TextType.TEXT)
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)


    def test_delim_code(self):
            node = TextNode("This is text with a `code block` word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                ],
                new_nodes,
            )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    
    def test_text_to_textnodes(self):
        input1 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)."
        expected_output1 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(".", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(input1), expected_output1)
        input2 = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev). Also another _sentence_ with [some link](https://google.com) and some **emphasis** on a `longer code block` that is followed by a ![second image](https://my_image.com) and some trailing text."
        expected_output2 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(". Also another ", TextType.TEXT),
            TextNode("sentence", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("some link", TextType.LINK, "https://google.com"),
            TextNode(" and some ", TextType.TEXT),
            TextNode("emphasis", TextType.BOLD),
            TextNode(" on a ", TextType.TEXT),
            TextNode("longer code block", TextType.CODE),
            TextNode(" that is followed by a ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://my_image.com"),
            TextNode(" and some trailing text.", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(input2), expected_output2)