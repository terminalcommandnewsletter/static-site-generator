import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_link(self):
        node = HTMLNode("a","Boot",props={"href": "boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Boot")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="boot.dev"')
    
    def test_quotes_in_prop(self):
        node = HTMLNode("h1","Boot.dev",props={"aria-label": '"Boot" "dot" "dev"'})
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "Boot.dev")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"aria-label": '"Boot" "dot" "dev"'})
        self.assertEqual(node.props_to_html(), ' aria-label="\\"Boot\\" \\"dot\\" \\"dev\\""')
    
    def test_multiple_props(self):
        node = HTMLNode("a","Boot",props={"href": "boot.dev", "data-heading": "true"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Boot")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "boot.dev", "data-heading": "true"})
        self.assertEqual(node.props_to_html(), ' href="boot.dev" data-heading="true"')


if __name__ == "__main__":
    unittest.main()