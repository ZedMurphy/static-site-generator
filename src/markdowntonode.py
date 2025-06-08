
from splitnodes import markdown_to_blocks, text_to_textnodes
from block_management import block_to_block_type, BlockType
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode


def markdown_to_html_node(markdown):
    splitted_blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in splitted_blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            splitted_block = block.split("\n")
            joined_block = " ".join(splitted_block)
            block_as_text_nodes = text_to_textnodes(joined_block)
            collected_nodes = []
            for node in block_as_text_nodes:
                collected_nodes.append(text_node_to_html_node(node))
            block_nodes.append(ParentNode("p", collected_nodes))
        
        elif block_type == BlockType.HEADING:
            count = 0
            for char in block:
                if char == "#":
                    count += 1
                else:
                    break
            new_block = block[count+1:].strip()
            block_as_text_nodes = text_to_textnodes(new_block)
            collected_nodes = []
            for node in block_as_text_nodes:
                collected_nodes.append(text_node_to_html_node(node))
            block_nodes.append(ParentNode(f"h{count}", collected_nodes))

        elif block_type == BlockType.QUOTE:
            block_as_list_of_lines = block.split("\n")
            new_lines = []
            collected_nodes = []
            for line in block_as_list_of_lines:
                new_lines.append(line[2:])
            joined_lines = "<br>".join(new_lines)
            text_nodes = text_to_textnodes(joined_lines)
            for node in text_nodes:
                collected_nodes.append(text_node_to_html_node(node))
            block_nodes.append(ParentNode("blockquote", collected_nodes))
            #    collected_lines = []
            #    line_nodes = text_to_textnodes(new_line)
            #    for text_node in line_nodes:
            #        collected_lines.append(text_node_to_html_node(text_node))
            #    collected_nodes.append(ParentNode("", collected_lines))                        
            #block_as_text_nodes = text_to_textnodes(block)
            #for node in block_as_text_nodes:
            #    collected_nodes.append(text_node_to_html_node(node))
            #block_nodes.append(ParentNode("blockquote", collected_nodes))

        elif block_type == BlockType.UNORDERED_LIST:
            block_as_list_of_lines = block.split("\n")
            collected_nodes = []
            for line in block_as_list_of_lines:
                new_line = line[2:]
                collected_lines = []
                line_nodes = text_to_textnodes(new_line)
                for text_node in line_nodes:
                    collected_lines.append(text_node_to_html_node(text_node))
                collected_nodes.append(ParentNode("li", collected_lines))
            block_nodes.append(ParentNode("ul", collected_nodes))
        
        elif block_type == BlockType.ORDERED_LIST:
            block_as_list_of_lines = block.split("\n")
            collected_nodes = []
            for line in block_as_list_of_lines:
                index_first_space = line.find(". ")
                new_line = line[index_first_space+2:]
                collected_lines = []
                line_nodes = text_to_textnodes(new_line)
                for text_node in line_nodes:
                    collected_lines.append(text_node_to_html_node(text_node))
                collected_nodes.append(ParentNode("li", collected_lines))
            block_nodes.append(ParentNode("ol", collected_nodes))

        elif block_type == BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            text = block[4:-3]
            raw_text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            code = ParentNode("code", [child])
            block_nodes.append(ParentNode("pre", [code]))
            #return ParentNode("pre", [code])
            #splitted_block = block.splitlines()
            #new_block = splitted_block[1:-1]
            #joined_block = "\n".join(new_block)
            #node = TextNode(joined_block, TextType.CODE)
            #html_node = []
            #tml_node.append(text_node_to_html_node(node))
            #block_nodes.append(ParentNode("pre", html_node))

    return ParentNode("div", block_nodes)

        
