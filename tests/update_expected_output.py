"""Updates expected output files."""
from pathlib import Path

from graphql import parse
from graphql.utilities.concat_ast import concat_ast
from graphql_codegen.codegen import generate


def _update_expected_output() -> None:
    current_dir = Path(__file__).parent
    data_dir = current_dir / 'data'
    with open(data_dir / 'schema.graphql', encoding='utf-8') as schema_file:
        schema_document = parse(schema_file.read())

    with open(data_dir / 'operations.graphql', encoding='utf-8') as operations_file:
        operations_document = parse(operations_file.read())

    ast = concat_ast([operations_document, schema_document])

    output_dir = data_dir / 'expected-outputs'
    for file_it in output_dir.iterdir():
        output = generate(ast, file_it.name)
        with open(file_it, 'w', encoding='utf-8') as output_file:
            output_file.write(output)


_update_expected_output()
