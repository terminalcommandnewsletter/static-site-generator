import unittest

from textnode import *
from parser_logic import *


class TestParser(unittest.TestCase):
    def test_split_eq(self):
        node = split_nodes_delimiter([TextNode("This is pretty *coooooool*.", "text", "google.com")], "*", "italic")
        node2 = split_nodes_delimiter([TextNode("This is pretty *coooooool*.", "text", "google.com")], "*", "italic")
        self.assertEqual(node, node2)
    
    def test_split_output_italic(self):
        node = split_nodes_delimiter([TextNode("I like *roaming* soo*oooo* much.", "text", None)], "*", "italic")
        self.assertEqual(node, [TextNode("I like ", "text", None), TextNode("roaming", "italic", None), TextNode(" soo", "text", None), TextNode("oooo", "italic", None), TextNode(" much.", "text", None)])
    
    def test_split_output_bold(self):
        node = split_nodes_delimiter([TextNode("I like **roaming** soo**oooo** much.", "text", None)], "**", "bold")
        self.assertEqual(node, [TextNode("I like ", "text", None), TextNode("roaming", "bold", None), TextNode(" soo", "text", None), TextNode("oooo", "bold", None), TextNode(" much.", "text", None)])
    
    def test_split_output_code(self):
        node = split_nodes_delimiter([TextNode("This is text with a `code block` word", "text")], "`", "code")
        self.assertEqual(node, [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ])
    
    def test_extract_markdown_images(self):
        extracted = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(extracted, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_markdown_links(self):
        extracted = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(extracted, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_extract_markdown_images(self):
        extracted = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(extracted, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_split_nodes_link(self):
        extracted = split_nodes_link([TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")])
        self.assertEqual(extracted, [TextNode("This is text with a link ", "text", None), TextNode("to boot dev", "link", "https://www.boot.dev"), TextNode(" and ", "text", None), TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")])
    
    def test_split_nodes_image(self):
        extracted = split_nodes_image([TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")])
        self.assertEqual(extracted, [TextNode("This is text with a ", "text", None), TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"), TextNode(" and ", "text", None), TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.maxDiff = None
        self.assertEqual(textnodes, [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ])

    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks("""# This is a heading

# This is a paragraph of text. It has some **bold** and *italic* words inside of it.

# * This is the first list item in a list block
# * This is a list item
# * This is another list item""")

        self.assertEqual(blocks, ["# This is a heading", "# This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "# * This is the first list item in a list block\n# * This is a list item\n# * This is another list item"])
    
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# ABC"), "heading-1")
        self.assertEqual(block_to_block_type("### ABC"), "heading-3")
        self.assertEqual(block_to_block_type("####### ABC"), "normal-paragraph")
        self.assertEqual(block_to_block_type("> ABC"), "quote")
        self.assertEqual(block_to_block_type("- ABC"), "unordered-list")
        self.assertEqual(block_to_block_type("* ABC"), "unordered-list")
        self.assertEqual(block_to_block_type("1. ABC"), "ordered-list")
        self.assertEqual(block_to_block_type("2. ABC"), "ordered-list")
        self.assertEqual(block_to_block_type("dsadsasad sadfdsf dsfdsf"), "normal-paragraph")
        self.assertEqual(block_to_block_type("""```
this is some code
```"""), "code")

    def test_markdown_to_html_node(self):
        self.assertEqual(markdown_to_html_node("# Heading\n\n* List\n* List\n\n```\nsome code\n```"), HTMLNode(tag='div', value='', children=[HTMLNode(tag='h1', value='Heading', children=None, props=None), HTMLNode(tag='ul', value='', children=[HTMLNode(tag='li', value='List', children=None, props=None), HTMLNode(tag='li', value='List', children=None, props=None)], props=None), HTMLNode(tag='pre', value=None, children=[HTMLNode(tag='code', value='some code', children=None, props=None)], props=None)], props=None))
    
    def test_extract_title(self):
        self.assertEqual(extract_title("# A Heading\n\nlorem ipsum"), "A Heading")
        self.assertEqual(extract_title("# Some text here\n\n# Some more text here\n\n# Even more"), "Some text here")

if __name__ == "__main__":
    unittest.main()