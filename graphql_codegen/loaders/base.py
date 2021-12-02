"""Document loader base class."""
from abc import abstractmethod
from abc import ABC
from typing import Iterable

from pathlib import Path

from graphql.language.ast import DocumentNode


class DocumentLoader(ABC):
    """Base class for document loader."""

    @abstractmethod
    def load(self, source: Path) -> Iterable[DocumentNode]:
        """Load the given source into GraphQL documents."""
