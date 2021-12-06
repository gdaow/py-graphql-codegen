"""Unit tests for context."""

from graphql_codegen.generation.context import Context
from tests.schema import parse_append_schema


def test_context_operations() -> None:
    """Context should return operations defined in the documents."""
    context = _get_context("""
        query getUsers {
           users {
               name
           }
        }
    """)

    operations = list(context.operations)
    assert len(operations) == 1

    operation = operations[0]
    assert operation.name == 'getUsers'
    fields = list(operation.fields)
    assert len(fields) == 1


def test_operation_fields() -> None:
    """Context should return fields defined on operations."""
    context = _get_context("""
        query getUsers {
           users {
               name
           }
        }
    """)

    operations = list(context.operations)
    assert len(operations) == 1

    operation = operations[0]
    assert operation.name == 'getUsers'
    fields = list(operation.fields)
    assert len(fields) == 1


def _get_context(document_string: str) -> Context:
    document = parse_append_schema(document_string)
    return Context([document])
