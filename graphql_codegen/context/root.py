"""The root object given to Mako templates."""
from typing import Iterable
from typing import Optional

from graphql.language.ast import DocumentNode
from graphql.language.ast import FragmentDefinitionNode
from graphql.language.ast import OperationDefinitionNode
from graphql.language.ast import OperationType
from graphql.type import GraphQLSchema
from graphql.utilities.build_ast_schema import build_ast_schema

from graphql_codegen.context.fragment import Fragment
from graphql_codegen.context.operation import Operation


class Root:
    """Root object given to template to render the AST."""

    def __init__(self, ast: DocumentNode, schema: Optional[GraphQLSchema] = None):
        """Initialize the root context."""
        if schema is None:
            schema = build_ast_schema(ast)
        self._ast = ast
        self._schema = schema

    @property
    def queries(self) -> Iterable[Operation]:
        """Return all operations defined in the AST."""
        return self._get_operations(OperationType.QUERY)

    @property
    def mutations(self) -> Iterable[Operation]:
        """Return all operations defined in the AST."""
        return self._get_operations(OperationType.MUTATION)

    @property
    def subscriptions(self) -> Iterable[Operation]:
        """Return all operations defined in the AST."""
        return self._get_operations(OperationType.SUBSCRIPTION)

    @property
    def fragments(self) -> Iterable[Fragment]:
        """Return all operations defined in the AST."""
        return self._get_fragments()

    def _get_operations(self, operation_type: OperationType) -> Iterable[Operation]:
        for node_it in self._ast.definitions:
            if isinstance(node_it, OperationDefinitionNode) and node_it.operation == operation_type:
                yield Operation(node_it, self._schema)

    def _get_fragments(self) -> Iterable[Fragment]:
        for node_it in self._ast.definitions:
            if isinstance(node_it, FragmentDefinitionNode):
                yield Fragment(node_it, self._schema)
