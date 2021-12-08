"""The root object given to Mako templates."""
from typing import Iterable

from graphql.language.ast import DocumentNode
from graphql.language.ast import OperationDefinitionNode
from graphql.type import GraphQLSchema

from graphql_codegen.context.operation import Operation


class Root:
    """Root object given to template to render the AST."""

    def __init__(self, ast: DocumentNode, schema: GraphQLSchema):
        """Initialize the root context."""
        self._ast = ast
        self._schema = schema

    @property
    def operations(self) -> Iterable[Operation]:
        """Return all operations defined in the AST."""
        for node_it in self._ast.definitions:
            if isinstance(node_it, OperationDefinitionNode):
                yield Operation(node_it, self._schema)
