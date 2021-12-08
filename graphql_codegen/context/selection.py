"""The root object given to Mako templates."""
from typing import Iterable
from typing import Optional
from typing import Union

from graphql.language.ast import FieldNode
from graphql.language.ast import FragmentSpreadNode
from graphql.language.ast import SelectionSetNode
from graphql.type import GraphQLNamedType
from graphql.type import GraphQLNonNull
from graphql.type import GraphQLObjectType
from graphql.type import GraphQLScalarType


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
    def name(self) -> str:
        """Return the field selection set."""
        return self._node.name.value

    @property
    def is_scalar(self) -> bool:
        """Return true if the current selection is a scalar field."""
        return isinstance(self._node, FieldNode) and isinstance(self.type, GraphQLScalarType)

    @property
    def is_object(self) -> bool:
        """Return true if the current selection is an object field."""
        return isinstance(self._node, FieldNode) and isinstance(self.type, GraphQLObjectType)

    @property
    def is_fragment(self) -> bool:
        """Check is the current selection is a fragment spread."""
        return isinstance(self._node, FragmentSpreadNode)

    @property
    def is_non_null(self) -> bool:
        """Return true if this field cannot be null."""
        return self._is_non_null

    @property
    def type(self) -> str:
        """Return the type name of the node."""
        assert self._type is not None
        return self._type.name

    @property
    def selection(self) -> Iterable['Selection']:
        """Return selection for this field if it's an object field."""
        assert isinstance(self._node, FieldNode) # TODO : Throw an error
        assert self._node.selection_set is not None # Don't know how it'd be possible
        assert isinstance(self._type, GraphQLObjectType)
        return get_selection(self._node.selection_set, self._type)


def get_selection(selection_set: SelectionSetNode, parent_type: GraphQLObjectType) -> Iterable[Selection]:
    """Return the operation's selection set."""
    for node_it in selection_set.selections:
        if isinstance(node_it, (FieldNode, FragmentSpreadNode)):
            yield Selection(node_it, parent_type)
