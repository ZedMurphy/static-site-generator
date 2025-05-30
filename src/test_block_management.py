import unittest
import textwrap

from block_management import BlockType, block_to_block_type

class TestBlockManagement(unittest.TestCase):

    def test_block_to_block_type(self):
        # Heading
        input1 = "### A heading"
        self.assertEqual(block_to_block_type(input1), BlockType.HEADING)

        # Ordered list
        input2 = textwrap.dedent("""\
            1. apples
            2. bananas
            3. oranges
        """).strip()
        self.assertEqual(block_to_block_type(input2), BlockType.ORDERED_LIST)

        # Unordered list
        input3 = textwrap.dedent("""\
            - item 1
            - item 2
            - item 3
        """).strip()
        self.assertEqual(block_to_block_type(input3), BlockType.UNORDERED_LIST)

        # Badly ordered list (should be paragraph)
        input4 = textwrap.dedent("""\
            1. apples
            3. oranges
            2. bananas
        """).strip()
        self.assertEqual(block_to_block_type(input4), BlockType.PARAGRAPH)

        # Code block
        input5 = "```This is a code block```"
        self.assertEqual(block_to_block_type(input5), BlockType.CODE)

        # Not a code block
        input6 = "```This is not a code block"
        self.assertEqual(block_to_block_type(input6), BlockType.PARAGRAPH)

        # Paragraph
        input7 = "I'm a simple paragraph."
        self.assertEqual(block_to_block_type(input7), BlockType.PARAGRAPH)

        # Quote block
        input8 = textwrap.dedent("""\
            >This is quote
            >definitely
            >a quote
        """).strip()
        self.assertEqual(block_to_block_type(input8), BlockType.QUOTE)

        # Not really a quote (should be paragraph)
        input9 = textwrap.dedent("""\
            >This starts like a quote
            but is none
            >even though it maybe should have been
        """).strip()
        self.assertEqual(block_to_block_type(input9), BlockType.PARAGRAPH)

        # Too many # in a heading block
        input10 = "####### too many"
        self.assertEqual(block_to_block_type(input10), BlockType.PARAGRAPH)

        # No space after heading hashtags
        input11 = "####"
        self.assertEqual(block_to_block_type(input11), BlockType.PARAGRAPH)

        # single backtick, not a code block
        input12 = "`Hi, I don't know what I should have been.`"
        self.assertEqual(block_to_block_type(input12), BlockType.PARAGRAPH)