"""Unit tests for context."""

from mako.template import Template
from tests.schema import parse_append_schema

from graphql_codegen.codegen import generate


def test_gen_scalar_field() -> None:
    """Context should return operations defined in the documents."""
    result = _generate(
        """
            query getVersion {
            version
            }
        """,
        '%for operation in root.operations:',
        '${operation.name}',
        '%   for selection in operation.selection:',
        '${selection.name}:${selection.type}',
        '%   endfor',
        '%endfor',
    )

    assert result == (
        'getVersion\n'
        'version:String\n'
    )


def _generate(document_string: str, *template_lines: str) -> str:
    template_string = '\n'.join(template_lines)
    document = parse_append_schema(document_string)
    template = Template(template_string)
    return generate(document, template)
