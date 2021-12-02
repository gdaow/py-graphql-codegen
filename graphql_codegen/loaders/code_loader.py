"""Loader extracting GraphQL documents from source code.

Based on a /* GraphQL */ comment tag, so this is only reliable for languages accepting
this kind of comment, and should be extended otherwise, don't hesitate to make a pull
request.
"""
from typing import Iterable
from re import compile as re_compile
from glob import iglob

from graphql.language import parse
from graphql.language.ast import DocumentNode

from graphql_codegen.loaders.base import Loader


class CodeLoader(Loader):
    """Loader loadng GraphQL documents from GraphQL definition files."""

    _PATTERN = re_compile('\\/\\* GraphQL \\*\\/\\s*`(?P<query_string>[^`]*)`')

    def load(self, source: str) -> Iterable[DocumentNode]:
        for source_file_name in iglob(source, recursive=True):
            with open(source_file_name, 'r', encoding='utf-8') as source_file:
                file_content = source_file.read()
                for match in self._PATTERN.findall(file_content):
                    yield parse(match)
