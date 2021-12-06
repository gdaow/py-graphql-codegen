"""Objects presenting parsed GraphQL in an easy way to be processed by code templates."""
from typing import Iterable
from typing import Optional

from graphql.language.ast import DocumentNode
from graphql.language.ast import FieldNode
from graphql.language.ast import OperationDefinitionNode
from graphql.type import GraphQLSchema
from graphql.utilities.build_ast_schema import build_ast_schema
from graphql.utilities.concat_ast import concat_ast


class Field:
    """A field."""

    def __init__(self, field: FieldNode, schema: GraphQLSchema) -> None:
        """Initialize field."""
        self._field = field
        self._schema = schema


class Operation:
    """An operation."""

    def __init__(self, definition: OperationDefinitionNode, schema: GraphQLSchema):
        """Initialize operation."""
        self._definition = definition
        self._schema = schema

    @property
    def name(self) -> str:
        """Name of this operation."""
        assert self._definition.name is not None
        return self._definition.name.value

    @property
    def fields(self) -> Iterable[Field]:
        """Return the list of fields of this operation."""
        for selection_it in self._definition.selection_set.selections:
            if isinstance(selection_it, FieldNode):
                yield Field(selection_it, self._schema)


class Context:
    """The generation context.

    Root object passed to templates, allows to easily access fields, operations... for templates
    to generate code from it.
    """

    def __init__(self, documents: Iterable[DocumentNode], schema: Optional[GraphQLSchema] = None):
        """Initialize the context."""
        self._document = concat_ast(list(documents))
        self._schema = schema or build_ast_schema(self._document)

    @property
    def operations(self) -> Iterable[Operation]:
        """Get all operations defined."""
        for definition in self._document.definitions:
            if isinstance(definition, OperationDefinitionNode):
                yield Operation(definition, self._schema)
