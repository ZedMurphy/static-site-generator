
from textnode import TextType, TextNode

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