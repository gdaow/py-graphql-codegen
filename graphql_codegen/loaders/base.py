"""Document loader base class."""
from abc import abstractmethod
from abc import ABC
from typing import Iterable

from graphql.language.ast import DocumentNode


class Loader(ABC):
    """Base class for loaders parsing GraphQL document from arbitrary source."""

    @abstractmethod
    def load(self, source: str) -> Iterable[DocumentNode]:
        """Load the given source into GraphQL documents."""
