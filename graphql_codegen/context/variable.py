"""The variable object given to Mako templates."""
from graphql.language.ast import VariableDefinitionNode
from graphql.language.ast import NonNullTypeNode
from graphql.language.ast import ListTypeNode
from graphql.language.ast import NamedTypeNode


class Variable:
    """Context object presenting a GraphQL variable definition."""

    def __init__(self, node: VariableDefinitionNode):
        """Initialize the root context."""
        self._node = node
        self._is_non_null = False
        self._is_list = False
        self._type_name: str

        field_type = node.type

        if isinstance(field_type, NonNullTypeNode):
            self._is_non_null = True
            field_type = field_type.type

        if isinstance(field_type, ListTypeNode):
            self._is_list = True
            field_type = field_type.type

        assert isinstance(field_type, NamedTypeNode)
        self._type_name = field_type.name.value

    @property
    def name(self) -> str:
        """Return the field selection set."""
        return self._node.variable.name.value

    @property
    def is_non_null(self) -> bool:
        """Return true if this field cannot be null."""
        return self._is_non_null

    @property
    def is_list(self) -> bool:
        """Return true if this field cannot be null."""
        return self._is_list

    @property
    def type_name(self) -> str:
        """Return the type name of the node."""
        return self._type_name
