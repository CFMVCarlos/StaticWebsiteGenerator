"""Inline markdown parsing and text node splitting utilities."""

import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Split text nodes containing markdown delimiters into multiple text nodes.

    Parameters
    ----------
    old_nodes : list[TextNode]
        List of TextNode objects to inspect and split.
    delimiter : str
        Delimiter string marking formatted text (e.g., '`', '**', '*').
    text_type : TextType
        Target TextType for text found within delimiter pairs.

    Returns
    -------
    list[TextNode]
        New list of TextNode objects with delimited sections converted.

    Raises
    ------
    ValueError
        If a closing delimiter is missing in a formatted text section.
    """
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes: list[TextNode] = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown syntax: formatted section not closed for delimiter '{delimiter}'"
            )
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extract markdown image alt-texts and URLs from raw text.

    Parameters
    ----------
    text : str
        Raw markdown string containing potential image syntax.

    Returns
    -------
    list[tuple[str, str]]
        List of tuples containing (alt_text, url) pairs for each markdown image.
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extract markdown link texts and target URLs from raw text.

    Parameters
    ----------
    text : str
        Raw markdown string containing potential link syntax.

    Returns
    -------
    list[tuple[str, str]]
        List of tuples containing (anchor_text, url) pairs for each markdown link.
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split text nodes containing markdown images into TEXT and IMAGE nodes.

    Parameters
    ----------
    old_nodes : list[TextNode]
        List of TextNode objects to inspect for markdown images.

    Returns
    -------
    list[TextNode]
        New list of TextNode objects with markdown images converted into IMAGE nodes.

    Raises
    ------
    ValueError
        If an extracted markdown image cannot be found during string splitting.
    """
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            sections = remaining_text.split(image_markdown, 1)
            if len(sections) != 2:
                raise ValueError(
                    f"Invalid markdown: image ![{image_alt}]({image_url}) not found in text"
                )
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split text nodes containing markdown links into TEXT and LINK nodes.

    Parameters
    ----------
    old_nodes : list[TextNode]
        List of TextNode objects to inspect for markdown links.

    Returns
    -------
    list[TextNode]
        New list of TextNode objects with markdown links converted into LINK nodes.

    Raises
    ------
    ValueError
        If an extracted markdown link cannot be found during string splitting.
    """
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            sections = remaining_text.split(link_markdown, 1)
            if len(sections) != 2:
                raise ValueError(
                    f"Invalid markdown: link [{link_text}]({link_url}) not found in text"
                )
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    """Convert a raw markdown string into a list of parsed TextNode objects.

    Parameters
    ----------
    text : str
        Raw markdown text to tokenize into inline text nodes.

    Returns
    -------
    list[TextNode]
        List of parsed TextNode objects covering all supported inline formats.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes
