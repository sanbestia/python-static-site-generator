from src.textnode import TextType, TextNode


def create_text_node(text, text_type, url):
    return TextNode(text, text_type, url)


def main():
    text = "I'm some dummy anchor text"
    text_type = TextType.LINK
    url = "dummysite.com"
    text_node = create_text_node(text, text_type, url)
    print(text_node)
    
    
if __name__ == '__main__':
    main()