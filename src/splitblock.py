"""Block-level markdown parsing and HTML AST generation."""

from enum import Enum

from htmlnode import HTMLNode, ParentNode
from splitnode import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    """Enumeration of supported markdown block types."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Split a markdown document into distinct blocks separated by blank lines.

    Parameters
    ----------
    markdown : str
        Raw markdown document text.

    Returns
    -------
    list[str]
        List of trimmed block strings with empty blocks filtered out.
    """
    blocks = markdown.split("\n\n")
    filtered_blocks: list[str] = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            filtered_blocks.append(stripped)
    return filtered_blocks


def block_to_block_type(block: str) -> BlockType:
    """Determine the block type of a single markdown block.

    Parameters
    ----------
    block : str
        A single stripped markdown block string.

    Returns
    -------
    BlockType
        The identified BlockType enum variant for the block.
    """
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```") and len(block) >= 7:
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    """Convert an inline markdown string into a list of HTMLNode objects.

    Parameters
    ----------
    text : str
        Inline markdown text to convert into child HTML nodes.

    Returns
    -------
    list[HTMLNode]
        List of rendered HTMLNode instances representing inline formatting.
    """
    text_nodes = text_to_textnodes(text)
    children: list[HTMLNode] = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    """Convert a paragraph markdown block into a 'p' ParentNode.

    Parameters
    ----------
    block : str
        Markdown paragraph block string.

    Returns
    -------
    ParentNode
        Rendered 'p' HTML ParentNode containing inline children.
    """
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    """Convert a heading markdown block into an 'h1'-'h6' ParentNode.

    Parameters
    ----------
    block : str
        Markdown heading block string.

    Returns
    -------
    ParentNode
        Rendered 'h1' through 'h6' HTML ParentNode.

    Raises
    ------
    ValueError
        If the heading level is not between 1 and 6, or syntax is invalid.
    """
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level < 1 or level > 6 or len(block) < level + 1 or block[level] != " ":
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    """Convert a code markdown block into a 'pre' and 'code' ParentNode.

    Parameters
    ----------
    block : str
        Markdown code block enclosed in triple backticks.

    Returns
    -------
    ParentNode
        Rendered 'pre' node containing a child 'code' node.

    Raises
    ------
    ValueError
        If the block is not properly enclosed in triple backticks.
    """
    if not block.startswith("```\n") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block: str) -> ParentNode:
    """Convert a blockquote markdown block into a 'blockquote' ParentNode.

    Parameters
    ----------
    block : str
        Markdown blockquote block string where each line starts with '>'.

    Returns
    -------
    ParentNode
        Rendered 'blockquote' HTML ParentNode.

    Raises
    ------
    ValueError
        If any line does not start with '>'.
    """
    lines = block.split("\n")
    new_lines: list[str] = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block: str) -> ParentNode:
    """Convert an unordered list markdown block into a 'ul' ParentNode.

    Parameters
    ----------
    block : str
        Markdown unordered list block where each line starts with '- '.

    Returns
    -------
    ParentNode
        Rendered 'ul' HTML ParentNode containing 'li' child nodes.

    Raises
    ------
    ValueError
        If any line does not start with '- '.
    """
    lines = block.split("\n")
    items: list[HTMLNode] = []
    for line in lines:
        if not line.startswith("- "):
            raise ValueError("Invalid unordered list item")
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)


def olist_to_html_node(block: str) -> ParentNode:
    """Convert an ordered list markdown block into an 'ol' ParentNode.

    Parameters
    ----------
    block : str
        Markdown ordered list block where each line starts with sequential numbers.

    Returns
    -------
    ParentNode
        Rendered 'ol' HTML ParentNode containing 'li' child nodes.

    Raises
    ------
    ValueError
        If any line does not match the expected sequential 'N. ' prefix.
    """
    lines = block.split("\n")
    items: list[HTMLNode] = []
    for i, line in enumerate(lines, start=1):
        prefix = f"{i}. "
        if not line.startswith(prefix):
            raise ValueError(f"Invalid ordered list item: expected '{prefix}'")
        text = line[len(prefix) :]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)


def block_to_html_node(block: str) -> ParentNode:
    """Dispatch a markdown block to its corresponding HTML ParentNode converter.

    Parameters
    ----------
    block : str
        A single markdown block string.

    Returns
    -------
    ParentNode
        Corresponding HTML ParentNode representation.

    Raises
    ------
    ValueError
        If the block type is invalid or unsupported.
    """
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
        case _:
            raise ValueError(f"Invalid block type: {block_type}")


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Convert a full markdown document string into a root 'div' ParentNode.

    Parameters
    ----------
    markdown : str
        Full raw markdown document string.

    Returns
    -------
    ParentNode
        Root 'div' ParentNode containing all parsed block HTML nodes.
    """
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def extract_title(markdown: str) -> str:
    """Extract the primary H1 header title from a markdown document.

    Parameters
    ----------
    markdown : str
        Markdown document string containing an H1 header.

    Returns
    -------
    str
        Extracted H1 header title text with leading/trailing whitespace removed.

    Raises
    ------
    ValueError
        If no line starting with '# ' is found in the markdown document.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")
