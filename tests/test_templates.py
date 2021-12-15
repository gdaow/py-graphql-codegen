"""Validates the output of the provided templates."""
from pathlib import Path
from graphql.language import parse
from graphql.utilities.concat_ast import concat_ast

from graphql_codegen.codegen import generate


def test_typed_document_node(shared_datadir: Path) -> None:
    """Test the typed-document-node code generation."""
    _test_template(shared_datadir, 'typed-document-node')


def _test_template(datadir: Path, template_name: str) -> None:
    operations_path = datadir / 'operations.graphql'
    with open(operations_path, 'r', encoding='utf-8') as operations_file:
        operations = parse(operations_file.read())

    schema_path = datadir / 'schema.graphql'
    with open(schema_path, 'r', encoding='utf-8') as schema_file:
        schema = parse(schema_file.read())

    ast = concat_ast([operations, schema])
    result = generate(ast, template_name)

    out_path = datadir / 'expected-outputs' / template_name
    with open(out_path, 'r', encoding='utf-8') as out:
        with open('out', 'w') as out_file:
            out_file.write(result)
        expected_output = out.read()
        assert expected_output == result
