import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_raises_not_implemented(self):
        node = HTMLNode("p", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_values(self):
        node = HTMLNode(
            tag="div",
            value="Hello, world!",
            children=None,
            props={"class": "container"},
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "container"})

    def test_repr(self):
        node = HTMLNode("p", "Hello, world!", None, {"class": "primary"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, Hello, world!, None, {'class': 'primary'})",
        )

    def test_children(self):
        child = HTMLNode("span", "child text")
        parent = HTMLNode("div", children=[child])
        self.assertEqual(parent.children, [child])
        assert parent.children is not None
        self.assertEqual(parent.children[0].value, "child text")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_different_tags(self):
        bold_node = LeafNode("b", "Bold text")
        self.assertEqual(bold_node.to_html(), "<b>Bold text</b>")

        heading_node = LeafNode("h1", "Title")
        self.assertEqual(heading_node.to_html(), "<h1>Title</h1>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_no_children(self):
        node_empty = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node_empty.to_html()

        node_none = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node_none.to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_deeply_nested(self):
        level3 = LeafNode("i", "deep")
        level2 = ParentNode("b", [level3])
        level1 = ParentNode("span", [level2])
        root = ParentNode("div", [level1])
        self.assertEqual(
            root.to_html(),
            "<div><span><b><i>deep</i></b></span></div>",
        )

    def test_to_html_mixed_siblings(self):
        child_leaf = LeafNode("span", "leaf sibling")
        child_parent = ParentNode("p", [LeafNode("b", "nested bold")])
        root = ParentNode("div", [child_leaf, child_parent])
        self.assertEqual(
            root.to_html(),
            "<div><span>leaf sibling</span><p><b>nested bold</b></p></div>",
        )


if __name__ == "__main__":
    unittest.main()
