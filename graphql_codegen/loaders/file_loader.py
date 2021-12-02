"""Loader loading GraphQL documents from GraphQL definition files."""
from typing import Iterable

from graphql.language import parse
from graphql.language.ast import DocumentNode

from graphql_codegen.loaders.base import DocumentLoader


class FileDocumentLoader(DocumentLoader):
    """Loader loadng GraphQL documents from GraphQL definition files."""

    def load(self, source: str) -> Iterable[DocumentNode]:
        with open(source, 'r', encoding='utf-8') as source_file:
            file_content = source_file.read()
            yield parse(file_content)
