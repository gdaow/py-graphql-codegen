"""Unit tests for loaders."""

from pathlib import Path

from graphql.language.ast import DocumentNode

from graphql_codegen.loaders.file_loader import FileLoader
from graphql_codegen.loaders.code_loader import CodeLoader


def test_file_loader(shared_datadir: Path) -> None:
    """File loader should correctly load graphql files from the filesystem."""
    loader = FileLoader()
    document_path = str(shared_datadir / 'schema.graphql')
    documents = list(loader.load(document_path))
    assert len(documents) == 1
    assert isinstance(documents[0], DocumentNode)


def test_code_loader(shared_datadir: Path) -> None:
    """Code loader should correctly load graphql document from embedded queries."""
    loader = CodeLoader()
    document_path = f'{shared_datadir}/sources/**/*.ts'
    documents = list(loader.load(document_path))
    assert len(documents) == 2
    assert isinstance(documents[0], DocumentNode)
    assert isinstance(documents[1], DocumentNode)
