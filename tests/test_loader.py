"""Unit tests for loaders."""

from pathlib import Path

from graphql.language.ast import DocumentNode

from graphql_codegen.loaders.file_loader import FileDocumentLoader


def test_file_loader(shared_datadir: Path) -> None:
    """File loader should correctly load graphql files from the filesystem."""
    loader = FileDocumentLoader()
    documents = list(loader.load(shared_datadir / 'schema.graphql'))
    assert len(documents) == 1
    assert isinstance(documents[0], DocumentNode)
