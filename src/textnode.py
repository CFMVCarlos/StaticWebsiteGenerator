"""Inline text representation and conversion to HTML leaf nodes."""

from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    """Enumeration of supported inline text formats."""

    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:
    """Represents an inline text chunk with formatting type and optional URL.

    Parameters
    ----------
    text : str
        The raw text content.
    text_type : TextType
        The inline text formatting type.
    url : str | None, default=None
        Target URL for links or image source URLs.

    Attributes
    ----------
    text : str
        The raw text content.
    text_type : TextType
        The inline text formatting type.
    url : str | None
        Target URL for links or image source URLs.
    """

    text: str
    text_type: TextType
    url: str | None

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object, /) -> bool:
        """Check equality between this TextNode and another object.

        Parameters
        ----------
        value : object
            Object to compare against.

        Returns
        -------
        bool
            True if value is a TextNode with matching attributes, False otherwise.
        """
        if not isinstance(value, TextNode):
            return False
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        """Return the string representation of the TextNode.

        Returns
        -------
        str
            Formatted representation string.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Convert an inline TextNode to its corresponding HTML LeafNode.

    Parameters
    ----------
    text_node : TextNode
        Input TextNode to convert.

    Returns
    -------
    LeafNode
        Renderable HTML LeafNode with appropriate tag and attributes.

    Raises
    ------
    ValueError
        If the TextNode has an unrecognized text_type.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url or ""})
        case TextType.IMAGE:
            return LeafNode(
                "img", "", {"src": text_node.url or "", "alt": text_node.text}
            )
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")
