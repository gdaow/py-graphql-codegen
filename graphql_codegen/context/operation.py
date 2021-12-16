"""Operation object given to mako template."""
from graphql.language.ast import OperationDefinitionNode
from graphql.language.ast import OperationType
from graphql.type import GraphQLObjectType
from graphql.type import GraphQLSchema

from graphql_codegen.context.executable_definition import ExecutableDefinition


def _get_type(node: OperationDefinitionNode, schema: GraphQLSchema) -> GraphQLObjectType:
    if node.operation == OperationType.QUERY:
        assert schema.query_type is not None
        return schema.query_type
    if node.operation == OperationType.MUTATION:
        assert schema.mutation_type is not None
        return schema.mutation_type

    assert schema.subscription_type is not None
    return schema.subscription_type


class Operation(ExecutableDefinition):
    """Context object presenting a GraphQL operation definition to the templates."""

    def __init__(self, node: OperationDefinitionNode, schema: GraphQLSchema):
        """Initialize the root context."""
        super().__init__(
            graphql_type=_get_type(node, schema),
            node=node,
            schema=schema
        )
