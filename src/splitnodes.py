
from textnode import TextType, TextNode
from markdownextraction import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []
    
    for old_node in old_nodes:
        # Only attempt to split TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Look for the first occurrence of the delimiter
        text = old_node.text
        first_index = text.find(delimiter)
        
        # If not found, keep the node as is
        if first_index == -1:
            new_nodes.append(old_node)
            continue
            
        # Look for the closing delimiter
        second_index = text.find(delimiter, first_index + len(delimiter))
        
        # If no closing delimiter found, that's invalid markdown
        if second_index == -1:
            raise Exception(f"No closing delimiter found for {delimiter}")
            
        # Now you can split into three parts...
        # Extract the three parts
        before_text = text[:first_index]
        between_text = text[first_index + len(delimiter):second_index]
        after_text = text[second_index + len(delimiter):]

        # Create nodes for each part (if they have content)
        if before_text:
            new_nodes.append(TextNode(before_text, TextType.TEXT))
            
        new_nodes.append(TextNode(between_text, text_type))

        # What about the after_text? It might contain more delimiter pairs!
        if after_text:
            # We need to process this text for more potential pairs
            # This is where recursion or additional processing would help
            remaining_node = TextNode(after_text, TextType.TEXT)
            result_nodes = split_nodes_delimiter([remaining_node], delimiter, text_type)
            new_nodes.extend(result_nodes)
        
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    initial_text = []
    initial_text.append(TextNode(text, TextType.TEXT))
    outputs1 = split_nodes_image(initial_text)
    outputs2 = split_nodes_link(outputs1)
    outputs3 = split_nodes_delimiter(outputs2, "`", TextType.CODE)
    outputs4 = split_nodes_delimiter(outputs3, "**", TextType.BOLD)
    outputs5 = split_nodes_delimiter(outputs4, "_", TextType.ITALIC)
    return outputs5


def markdown_to_blocks(markdown):
    if not markdown:
        raise Exception("No markdown text given.")    
    splitted_markdown = markdown.split("\n\n")
    clean_blocks = []
    for block in splitted_markdown:
        if block.strip() != "":
            clean_blocks.append(block.strip())
    return clean_blocks