"""Operation object given to mako template."""
from graphql.language.ast import FragmentDefinitionNode
from graphql.type import GraphQLObjectType
from graphql.type import GraphQLSchema

from graphql_codegen.context.executable_definition import ExecutableDefinition


def _get_type(node: FragmentDefinitionNode, schema: GraphQLSchema) -> GraphQLObjectType:
    type_name = node.type_condition.name.value
    graphql_type = schema.get_type(type_name)
    assert graphql_type is not None
    assert isinstance(graphql_type, GraphQLObjectType)
    return graphql_type


class Fragment(ExecutableDefinition):
    """Context object presenting a GraphQL operation definition to the templates."""

    def __init__(self, node: FragmentDefinitionNode, schema: GraphQLSchema):
        """Initialize the root context."""
        super().__init__(
            graphql_type=_get_type(node, schema),
            node=node,
            schema=schema
        )
