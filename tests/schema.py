"""Common schema used for tests."""
from pathlib import Path

from graphql.language import parse
from graphql.language.ast import DocumentNode
from graphql.utilities.concat_ast import concat_ast


def parse_append_schema(datadir: Path, document_string: str) -> DocumentNode:
    """Parse the given string and append the schema definition to the resulting document."""
    with open(datadir / 'schema.graphql', 'r', encoding='utf-8') as schema_file:
        schema_document = parse(schema_file.read())

    documents = [
        parse(document_string),
        schema_document
    ]

    return concat_ast(documents)
