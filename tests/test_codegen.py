"""Codegen unit tests."""
from pathlib import Path
from graphql_codegen.codegen import generate
from tests.schema import parse_append_schema


def test_generate_with_path(shared_datadir: Path) -> None:
    """Giving a path to generate should correcly load the mako template."""
    document = parse_append_schema(shared_datadir, """
        query {
            version
        }
    """)
    result = generate(document, shared_datadir / 'test.mako')
    assert result == 'version:String\n'
