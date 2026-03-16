from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    MULTILINE_CODE = "multiline_code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    LIST_ITEM = "list_item"
    HEADING_FIRST = "heading_first"
    HEADING_SECOND = "heading_second"
    HEADING_THIRD = "heading_third"
    HEADING_FOURTH = "heading_fourth"
    HEADING_FIFTH = "heading_fifth"
    HEADING_SIXTH = "heading_sixth"
    DIV = "div"
    
    
