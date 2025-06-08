from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


def block_to_block_type(markdown_block):

    if markdown_block.startswith("#"):
        count = 0
        for char in markdown_block:
            if char == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and len(markdown_block) > count and markdown_block[count] == " ":
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH

    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    
    elif markdown_block.startswith(">"):
        splitted_block = markdown_block.split("\n")
        for line in splitted_block:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE           
        
    elif markdown_block.startswith("- "):
        splitted_block = markdown_block.split("\n")
        for line in splitted_block:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    elif markdown_block.startswith("* "):
        splitted_block = markdown_block.split("\n")
        for line in splitted_block:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST               
        
    elif markdown_block.startswith("1. "):
        splitted_block = markdown_block.split("\n")
        for i in range(len(splitted_block)):
            line = splitted_block[i]
            if not line.startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST      
        
    else:
        return BlockType.PARAGRAPH