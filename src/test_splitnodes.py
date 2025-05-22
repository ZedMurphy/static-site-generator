import unittest

from splitnodes import split_nodes_delimiter
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