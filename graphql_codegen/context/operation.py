"""The root object given to Mako templates."""
from typing import Iterable
from typing import Optional

from graphql.language.ast import OperationDefinitionNode
from graphql.language.ast import OperationType
from graphql.type import GraphQLSchema

from graphql_codegen.context.selection import Selection
from graphql_codegen.context.selection import get_selection


class Operation:
    """Context object presenting a GraphQL operation definition to the templates."""

    def __init__(self, node: OperationDefinitionNode, schema: GraphQLSchema):
        """Initialize the root context."""
        self._node = node
        self._schema = schema
        if node.operation == OperationType.QUERY:
            self._type = schema.query_type
        elif node.operation == OperationType.MUTATION:
            self._type = schema.mutation_type
        else:
            self._type = schema.mutation_type

        assert self._type is not None

    @property
    def name(self) -> Optional[str]:
        """Get the name of this operation, or None if it hasn't none."""
        name_node = self._node.name
        if name_node is None:
            return None
        return name_node.value

    @property
    def type(self) -> str:
        """Return the type Query / Mutation / Subscription of the operation."""
        operation_type = self._node.operation
        if operation_type == OperationType.QUERY:
            return 'Query'
        if operation_type == OperationType.MUTATION:
            return 'Mutation'
        assert operation_type == OperationType.SUBSCRIPTION
        return 'Subscription'

    @property
    def selection(self) -> Iterable[Selection]:
        """Return the operation's selection set."""
        assert self._type is not None
        return get_selection(self._node.selection_set, self._type)
