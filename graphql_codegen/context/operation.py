"""The root object given to Mako templates."""
from typing import Iterable
from typing import Optional

from graphql.language.ast import OperationDefinitionNode
from graphql.type import GraphQLSchema

from graphql_codegen.context.selection import Selection
from graphql_codegen.context.selection import get_selection


class Operation:
    """Context object presenting a GraphQL operation definition to the templates."""

    def __init__(self, node: OperationDefinitionNode, schema: GraphQLSchema):
        """Initialize the root context."""
        self._node = node
        self._schema = schema
        assert schema.query_type is not None # TODO: Raise error instead
        self._type = schema.query_type

    @property
    def name(self) -> Optional[str]:
        """Get the name of this operation, or None if it hasn't none."""
        name_node = self._node.name
        if name_node is None:
            return None
        return name_node.value

    @property
    def selection(self) -> Iterable[Selection]:
        """Return the operation's selection set."""
        return get_selection(self._node.selection_set, self._type)
