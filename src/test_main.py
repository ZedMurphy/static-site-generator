import unittest

from main import extract_title

class TestMain(unittest.TestCase):

    def test_extract_title(self):
        markdown1 = """
# My heading is this
        
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        output1 = "My heading is this"
        self.assertEqual(extract_title(markdown1), output1)

        markdown2 = """
Some leading text that nobody needs at this point.

# Hey, there's a title!

### Some h3 to go here.

"""
        output2 = "Hey, there's a title!"
        self.assertEqual(extract_title(markdown2), output2)

        markdown3 = """
## Some leading h2 that would drive any screen reader crazy.

# Lookie, there's a title!

### Some h3 to go here.

"""
        output3 = "Lookie, there's a title!"
        self.assertEqual(extract_title(markdown3), output3)

        markdown4 = """
## Another one
        
Another moment in time.
Another selfless crime.
Another day comes to an end.
Another wound time needs to mend.
"""
        with self.assertRaises(Exception):
            extract_title(markdown4)