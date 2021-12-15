"""Entry point to generate code from GraphQL AST."""
from typing import Generator
from typing import Optional
from typing import Union
from typing import cast

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from graphql.language import DocumentNode
from graphql.type import GraphQLSchema
from mako.lookup import TemplateLookup
from mako.template import Template

from graphql_codegen.context.root import Root
from graphql_codegen.context.filters import camel


def generate(
    ast: DocumentNode,
    template: Union[Template, str, Path],
    schema: Optional[GraphQLSchema] = None,
) -> str:
    """Generate code from the given GraphQL AST, using the given template.

    Args:
        ast:      The parsed GraphQL AST
        template: Either the name without the extension of a template to load from provided templates (i.e
                  for example 'typed-document-node'), a Path object to a template on disk, or directly a
                  Mako Template.
        schema:   Optional, a GraphQLSchema to use to interpret the operations defined in the AST. If none
                  is provided, the schema will be loaded from the provided ast.

    Return:
        The generated code.

    """
    root = Root(ast, schema)
    with _get_template(template) as mako_template:
        return cast(str, mako_template.render(
            root=root,
            camel=camel
        ))


@contextmanager
def _get_template(template: Union[Template, str, Path]) -> Generator[Template, None, None]:
    if isinstance(template, Template):
        yield template
    elif isinstance(template, Path):
        yield Template(filename=str(template))
    else:
        with TemporaryDirectory() as module_directory:
            template_directory = Path(__file__).parent / 'templates'
            directories = [str(template_directory)]
            lookup = TemplateLookup(
                directories=directories,
                module_directory=str(module_directory)
            )

            yield lookup.get_template(template + '.mako')
