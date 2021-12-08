"""Unit tests for context."""

from tests.schema import parse_append_schema

from graphql_codegen.context.root import Root


def test_scalar_field() -> None:
    """Context should return operations defined in the documents."""
    root = _get_root("""
        query getVersion {
            version
        }
    """)

    operations = list(root.operations)
    assert len(operations) == 1
    operation = operations[0]
    assert operation.name == 'getVersion'
    fields = list(operation.selection)
    assert len(fields) == 1
    field = fields[0]
    assert field.name == 'version'
    assert field.type == 'String'


def _get_root(document_string: str) -> Root:
    document = parse_append_schema(document_string)
    return Root(document)
