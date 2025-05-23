import unittest

from markdownextraction import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches1 = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches1)

        matches2 = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ![second image](https://my_image.com) and some trailing text."
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("second image", "https://my_image.com")], matches2)

    def test_extract_markdown_links(self):
        matches1 = extract_markdown_links(
            "This is a text with a [link](https://google.com)."
        )
        self.assertListEqual([("link", "https://google.com")], matches1)

        matches2 = extract_markdown_links(
            "This is a text with a [link](https://google.com) and a [second link](https://bing.com) and some trailing text."
        )
        self.assertListEqual([("link", "https://google.com"), ("second link", "https://bing.com")], matches2)