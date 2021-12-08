"""Unit tests for context."""

from tests.schema import parse_append_schema

from graphql_codegen.context.root import Root
from graphql_codegen.context.operation import Operation


def test_scalar_field() -> None:
    """Context should correctly expose fields."""
    operation = _get_operation('query { version }')

    fields = list(operation.selection)
    assert len(fields) == 1
    field = fields[0]
    assert field.name == 'version'
    assert not field.is_non_null
    assert field.is_scalar
    assert not field.is_fragment
    assert not field.is_object
    assert field.type == 'String'


def test_non_null_field() -> None:
    """Context should correctly expose non-null fields."""
    operation = _get_operation('query { status }')

    fields = list(operation.selection)
    assert len(fields) == 1
    field = fields[0]
    assert field.name == 'status'
    assert field.is_non_null
    assert field.is_scalar
    assert not field.is_fragment
    assert not field.is_object
    assert field.type == 'String'


def test_object_field() -> None:
    """Context should correctly expose non-null object fields."""
    operation = _get_operation('query { users { id, username, } }')

    fields = list(operation.selection)
    assert len(fields) == 1
    field = fields[0]
    assert field.name == 'users'
    assert field.type == 'User'
    assert field.is_object
    assert not field.is_fragment
    assert not field.is_scalar

    fields = list(field.selection)
    assert len(fields) == 2
    id_field = fields[0]

    assert id_field.name == 'id'
    assert id_field.type == 'ID'

    username_field = fields[1]
    assert username_field.name == 'username'
    assert username_field.type == 'String'


def _get_root(document_string: str) -> Root:
    document = parse_append_schema(document_string)
    return Root(document)


def _get_operation(document_string: str) -> Operation:
    root = _get_root(document_string)
    operations = list(root.operations)
    assert len(operations) == 1
    return operations[0]
