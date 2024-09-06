import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode([LeafNode("text","h1"),LeafNode("this is some text","p")], "body", {"class": "dark"})
        node2 = ParentNode([LeafNode("text","h1"),LeafNode("this is some text","p")], "body", {"class": "dark"})
        self.assertEqual(node, node2)
    
    def test_no_children(self):
        with self.assertRaises(ValueError, msg="No children"):
            node = ParentNode()
    
    def test_no_tag(self):
        with self.assertRaises(ValueError, msg="No tag"):
            node = ParentNode()
        
    def test_html_output(self):
        node = ParentNode([LeafNode("text","h1"),LeafNode("this is some text","p")], "body", {"class": "dark"}).to_html()
        self.assertEqual(node, '<body class="dark"><h1>text</h1><p>this is some text</p></body>')
    
    def test_nested_html_output(self):
        node = ParentNode([LeafNode("text","h1"),LeafNode("this is some text","p"), ParentNode([LeafNode("text","h1"),LeafNode("this is some text","p")], "div")], "body", {"class": "dark"}).to_html()
        self.assertEqual(node, '<body class="dark"><h1>text</h1><p>this is some text</p><div><h1>text</h1><p>this is some text</p></div></body>')

    # def test_no_value(self):
    #     with self.assertRaises(ValueError):
    #         node = ParentNode(value=None, tag="a")
    #     with self.assertRaises(ValueError):
    #         node = ParentNode(value=None, tag="a").to_html()
    
    # def test_basic(self):
    #     node = ParentNode("boot.dev","p",{"aria-label": "Boot dot dev"}).to_html()
    #     self.assertEqual(node, '<p aria-label="Boot dot dev">boot.dev</p>')


if __name__ == "__main__":
    unittest.main()