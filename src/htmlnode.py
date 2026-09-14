"""HTML node representations for rendering abstract syntax trees into HTML."""


class HTMLNode:
    """Base class representing an HTML node in a document tree.

    Parameters
    ----------
    tag : str | None
        HTML tag name (e.g., 'p', 'div', 'a'), by default None.
    value : str | None
        Text content of the node, by default None.
    children : list[HTMLNode] | None
        Nested child HTML nodes, by default None.
    props : dict[str, str] | None
        Key-value attribute pairs (e.g., {'href': 'https://example.com'}),
        by default None.

    Attributes
    ----------
    tag : str | None
        HTML tag name.
    value : str | None
        Text content of the node.
    children : list[HTMLNode] | None
        Child HTML nodes.
    props : dict[str, str] | None
        Dictionary of HTML element attributes.
    """

    tag: str | None
    value: str | None
    children: list["HTMLNode"] | None
    props: dict[str, str] | None

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """Render the HTML node and its subtree as an HTML string.

        Returns
        -------
        str
            Rendered HTML string.

        Raises
        ------
        NotImplementedError
            Always raised by the base class.
        """
        raise NotImplementedError()

    def props_to_html(self) -> str:
        """Format the node's properties dictionary as an HTML attribute string.

        Returns
        -------
        str
            Space-prefixed HTML attributes string.
        """
        if not self.props:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self) -> str:
        """Return the string representation of the HTMLNode.

        Returns
        -------
        str
            String representation showing tag, value, children, and props.
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """HTML node that does not contain child nodes.

    Parameters
    ----------
    tag : str | None
        HTML tag name, or None for raw text.
    value : str | None
        Text content of the leaf node.
    props : dict[str, str] | None
        Key-value attribute pairs, by default None.
    """

    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        """Render the leaf node as an HTML string.

        Returns
        -------
        str
            Rendered HTML or raw text.

        Raises
        ------
        ValueError
            If value is None.
        """
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        """Return the string representation of the LeafNode.

        Returns
        -------
        str
            String representation showing tag, value, and props.
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """HTML node that contains one or more child nodes.

    Parameters
    ----------
    tag : str | None
        HTML tag name.
    children : list["HTMLNode"] | None
        Non-empty list of child HTML nodes.
    props : dict[str, str] | None
        Key-value attribute pairs, by default None.
    """

    def __init__(
        self,
        tag: str | None,
        children: list["HTMLNode"] | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        """Render the parent node and all its children as an HTML string.

        Returns
        -------
        str
            Rendered HTML tag enclosing all rendered children.

        Raises
        ------
        ValueError
            If tag is None or children is empty/None.
        """
        if not self.tag:
            raise ValueError("ParentNode must have a tag")

        if not self.children:
            raise ValueError("ParentNode must have children")

        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
