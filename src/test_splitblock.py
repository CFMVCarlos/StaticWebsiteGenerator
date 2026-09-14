import unittest

from splitblock import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestSplitBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = "\n\n\n\nBlock 1\n\n\n\n\nBlock 2\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_whitespace_lines(self):
        md = "  Block 1  \n\n   \n\n  Block 2  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single block of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single block of text."])

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_headings_invalid(self):
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ndef hello():\n    print('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)

    def test_code_block_invalid(self):
        self.assertEqual(block_to_block_type("```inline```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\nunclosed"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> This is a quote\n> with multiple lines\n> and words"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block_no_space = ">line 1\n>line 2"
        self.assertEqual(block_to_block_type(block_no_space), BlockType.QUOTE)

    def test_quote_block_invalid(self):
        block = "> line 1\nline 2 without quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- single item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid(self):
        self.assertEqual(
            block_to_block_type("-item without space"), BlockType.PARAGRAPH
        )
        self.assertEqual(block_to_block_type("- item 1\nitem 2"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. single item"), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid(self):
        self.assertEqual(
            block_to_block_type("2. starts at 2\n3. third"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("1. first\n3. skipped 2"), BlockType.PARAGRAPH
        )
        self.assertEqual(block_to_block_type("1.no space"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "Just a normal paragraph with some text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2 with **bold**

### Heading 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h3>Heading 3</h3></div>",
        )

    def test_blockquote(self):
        md = """
> This is a quote
> with **bold** text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First item
- Second item with _italic_
- Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <i>italic</i></li><li>Third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with `code`
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <code>code</code></li><li>Third item</li></ol></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# Hello")
        self.assertEqual(title, "Hello")

    def test_extract_title_with_whitespace(self):
        title = extract_title("#   Tolkien Fan Club   ")
        self.assertEqual(title, "Tolkien Fan Club")

    def test_extract_title_multiline(self):
        md = "Introductory text\n\n# The Fellowship\n\nMore paragraphs"
        title = extract_title(md)
        self.assertEqual(title, "The Fellowship")

    def test_extract_title_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## H2 only\n\nNo h1 here")

    def test_extract_title_no_header_raises(self):
        with self.assertRaises(ValueError):
            extract_title("Just plain text with no headings.")


if __name__ == "__main__":
    unittest.main()
