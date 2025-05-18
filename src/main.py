#print("hello world")

from textnode import *


def main():
    text = "hello world"
    text_type = TextType.IMAGE  # Use the full enum class name
    url = "https://my_url.de"

    dummy = TextNode(text, text_type, url)
    print(dummy)


main()