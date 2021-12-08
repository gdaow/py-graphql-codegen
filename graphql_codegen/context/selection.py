"""The root object given to Mako templates."""
from typing import Union
from typing import cast

from graphql.language.ast import FragmentSpreadNode
from graphql.language.ast import FieldNode
from graphql.type import GraphQLObjectType


class Selection:
    """Context object presenting a GraphQL field definition to the templates."""

    def __init__(self, node: Union[FragmentSpreadNode, FieldNode], parent_type: GraphQLObjectType):
        """Initialize the root context."""
        self._node = node
        if isinstance(node, FieldNode):
            field_name = node.name.value
            self._field = parent_type.fields.get(field_name)
            assert self._field is not None # TODO: Raise a GraphQL error here.

    def is_fragment(self) -> bool:
        """Check is the current selection is a fragment spread."""
        return isinstance(self._node, FragmentSpreadNode)

    def is_scalar(self) -> bool:
        """Return true if the current selection is a scalar field."""
        return isinstance(self._node, FieldNode)

    @property
    def name(self) -> str:
        """Return the field selection set."""
        return self._node.name.value

    @property
    def type(self) -> str:
        """Return the type name of the node."""
        assert self._field is not None
        return cast(str, self._field.type.name)
