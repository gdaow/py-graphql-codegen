"""Common schema used for tests."""

from graphql.language import parse
from graphql.language.ast import DocumentNode
from graphql.utilities.concat_ast import concat_ast


def parse_append_schema(document_string: str) -> DocumentNode:
    """Parse the given string and append the schema definition to the resulting document."""
    documents = [
        parse(document_string),
        get_schema_document()
    ]

    return concat_ast(documents)


def get_schema_document() -> DocumentNode:
    """Get a document containing the test schema definitions."""
    return parse(_SCHEMA)


_SCHEMA = """
type User {
    id: ID!
    username: String
    first_name: String
    last_name: String
    deprecated_name: String @deprecated
}

type Query {
    users: User
}
"""
