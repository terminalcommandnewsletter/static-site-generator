import unittest

from textnode import *
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "google.com")
        node2 = TextNode("This is a text node", "bold", "google.com")
        self.assertEqual(node, node2)
    
    def test_different_url(self):
        node = TextNode("This is a text node", "bold", "google.com")
        node2 = TextNode("This is a text node", "bold", "notgoogle.com")
        self.assertNotEqual(node, node2)
    
    def test_no_url(self):
        node = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node2)

    def test_text_node_to_html_node_text(self):
        node = text_node_to_html_node(TextNode("This is a text node", "text", None))
        self.assertEqual(node, LeafNode("This is a text node"))
    
    def test_text_node_to_html_node_bold(self):
        node = text_node_to_html_node(TextNode("This is a text node", "bold", None))
        self.assertEqual(node, LeafNode("This is a text node", "b"))
    
    def test_text_node_to_html_node_italic(self):
        node = text_node_to_html_node(TextNode("This is a text node", "italic", None))
        self.assertEqual(node, LeafNode("This is a text node", "i"))
    
    def test_text_node_to_html_node_code(self):
        node = text_node_to_html_node(TextNode("This is a text node", "code", None))
        self.assertEqual(node, LeafNode("This is a text node", "code"))
    
    def test_text_node_to_html_node_link(self):
        node = text_node_to_html_node(TextNode("This is a text node", "link", "https://boot.dev"))
        self.assertEqual(node, LeafNode("This is a text node", "a", {"href": "https://boot.dev"}))
    
    def test_text_node_to_html_node_image(self):
        node = text_node_to_html_node(TextNode("This is a text node", "image", "https://boot.dev"))
        self.assertEqual(node, LeafNode("", "img", {"src": "https://boot.dev", "alt": "This is a text node"}))
    
    def test_text_node_to_html_node_invalid(self):
        with self.assertRaises(ValueError, msg="Invalid text type"):
            node = text_node_to_html_node(TextNode("This is a text node", "testtest", "https://boot.dev"))

if __name__ == "__main__":
    unittest.main()