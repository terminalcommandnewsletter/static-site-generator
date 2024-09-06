import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("This is a Leaf node", "a", {"href": "boot.dev"})
        node2 = LeafNode("This is a Leaf node", "a", {"href": "boot.dev"})
        self.assertEqual(node, node2)
    
    def test_no_tag(self):
        node = LeafNode("This is a Leaf node").to_html()
        self.assertEqual(node, "This is a Leaf node")
        
    def test_no_props(self):
        node = LeafNode("This is a Leaf node", "a").to_html()
        self.assertEqual(node, "<a>This is a Leaf node</a>")

    def test_no_value(self):
        with self.assertRaises(ValueError, msg="No value"):
            node = LeafNode(value=None, tag="a")
    
    def test_basic(self):
        node = LeafNode("boot.dev","p",{"aria-label": "Boot dot dev"}).to_html()
        self.assertEqual(node, '<p aria-label="Boot dot dev">boot.dev</p>')


if __name__ == "__main__":
    unittest.main()