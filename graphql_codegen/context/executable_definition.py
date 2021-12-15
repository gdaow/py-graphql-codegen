"""Operation object given to mako template."""
from typing import Iterable
from typing import Optional

from graphql.language.ast import ExecutableDefinitionNode
from graphql.type import GraphQLSchema
from graphql.type import GraphQLObjectType

from graphql_codegen.context.selection import Selection
from graphql_codegen.context.selection import get_selection


class ExecutableDefinition:
    """Base class for fragment definition nodes."""

    def __init__(
        self,
        graphql_type: GraphQLObjectType,
        node: ExecutableDefinitionNode,
        schema: GraphQLSchema
    ):
        """Initialize the root context."""
        self._node = node
        self._type = graphql_type
        self._schema = schema

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
        assert self._type is not None
        return get_selection(self._node.selection_set, self._type)
