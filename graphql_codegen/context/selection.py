"""The root object given to Mako templates."""
from typing import Optional
from typing import Union

from graphql.language.ast import FieldNode
from graphql.language.ast import FragmentSpreadNode
from graphql.type import GraphQLNamedType
from graphql.type import GraphQLNonNull
from graphql.type import GraphQLObjectType


class Selection:
    """Context object presenting a GraphQL field definition to the templates."""

    def __init__(self, node: Union[FragmentSpreadNode, FieldNode], parent_type: GraphQLObjectType):
        """Initialize the root context."""
        self._node = node
        self._is_non_null = False
        self._type: Optional[GraphQLNamedType] = None

        if isinstance(node, FieldNode):
            field_name = node.name.value
            field = parent_type.fields.get(field_name)
            assert field is not None # TODO: Raise a GraphQL error here.

            field_type = field.type

            if isinstance(field_type, GraphQLNonNull):
                self._is_non_null = True
                field_type = field_type.of_type

            self._type = field_type

    @property
    def is_fragment(self) -> bool:
        """Check is the current selection is a fragment spread."""
        return isinstance(self._node, FragmentSpreadNode)

    @property
    def is_scalar(self) -> bool:
        """Return true if the current selection is a scalar field."""
        return isinstance(self._node, FieldNode)

    @property
    def is_non_null(self) -> bool:
        """Return true if this field cannot be null."""
        return self._is_non_null

    @property
    def name(self) -> str:
        """Return the field selection set."""
        return self._node.name.value

    @property
    def type(self) -> str:
        """Return the type name of the node."""
        assert self._type is not None
        return self._type.name
