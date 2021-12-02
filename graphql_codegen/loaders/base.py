"""Document loader base class."""
from abc import abstractmethod
from abc import ABC
from typing import Iterable

from graphql.language.ast import DocumentNode


class DocumentLoader(ABC):
    """Base class for document loader."""

    @abstractmethod
    def load(self, source: str) -> Iterable[DocumentNode]:
        """Load the given source into GraphQL documents."""
