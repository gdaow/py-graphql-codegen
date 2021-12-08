"""Entry point to generate code from GraphQL AST."""
from typing import Optional
from typing import cast

from graphql.language import DocumentNode
from graphql.type import GraphQLSchema
from mako.template import Template

from graphql_codegen.context.root import Root


def generate(ast: DocumentNode, template: Template, schema: Optional[GraphQLSchema] = None) -> str:
    """Generate code from the given GraphQL AST, using the given template."""
    root = Root(ast, schema)
    return cast(str, template.render(root=root))
