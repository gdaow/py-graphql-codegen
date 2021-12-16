"""Unit tests for context."""
from pathlib import Path

from tests.schema import parse_append_schema

from graphql_codegen.context.root import Root
from graphql_codegen.context.operation import Operation


def test_scalar_field(shared_datadir: Path) -> None:
    """Context should correctly expose fields."""
    operation = _get_query(shared_datadir, 'query { version }')

    fields = list(operation.selection)
    assert len(fields) == 1
    field = fields[0]
    assert field.name == 'version'
    assert not field.is_non_null
    assert field.is_scalar
    assert not field.is_fragment
    assert not field.is_object
    assert field.type == 'String'


def test_non_null_field(shared_datadir: Path) -> None:
    """Context should correctly expose non-null fields."""
    operation = _get_query(shared_datadir, 'query { status }')

    fields = list(operation.selection)
    assert len(fields) == 1
    field = fields[0]
    assert field.name == 'status'
    assert field.is_non_null
    assert field.is_scalar
    assert not field.is_fragment
    assert not field.is_object
    assert field.type == 'String'


def test_object_field(shared_datadir: Path) -> None:
    """Context should correctly expose non-null object fields."""
    operation = _get_query(shared_datadir, 'query { users { id, username, } }')

    fields = list(operation.selection)
    assert len(fields) == 1
    field = fields[0]
    assert field.name == 'users'
    assert field.type == 'User'
    assert field.is_object
    assert not field.is_fragment
    assert not field.is_scalar

    fields = list(field.selection)
    assert len(fields) == 2
    id_field = fields[0]

    assert id_field.name == 'id'
    assert id_field.type == 'ID'

    username_field = fields[1]
    assert username_field.name == 'username'
    assert username_field.type == 'String'


def test_operations(shared_datadir: Path) -> None:
    """Context should correctly return all kinds of operations."""
    query = _get_query(shared_datadir, 'query testQuery { users { id, username, } }')
    assert query.name == 'testQuery'

    mutation = _get_mutation(shared_datadir, 'mutation testMutation { setStatus(status: "new_status") }')
    assert mutation.name == 'testMutation'


def test_fragments(shared_datadir: Path) -> None:
    """Context should correctly return fragments."""
    root = _get_root(shared_datadir, 'fragment testFragment on User { id, username, }')
    fragments = list(root.fragments)
    assert len(fragments) == 1
    fragment = fragments[0]
    assert fragment.name == 'testFragment'
    fields = list(fragment.selection)
    assert len(fields) == 2
    assert fields[0].name == 'id'
    assert fields[1].name == 'username'


def test_variables(shared_datadir: Path) -> None:
    """Context should correctly return all kinds of variables."""
    mutation = _get_mutation(shared_datadir, """
        scalar Int
        mutation testMutation($intVar: Int, $nonNullVar: Int!, $listVar: [Int]) {
            setStatus(status: "new_status")
        }
    """)
    assert mutation.name == 'testMutation'
    variables = list(mutation.variables)
    assert len(variables) == 3
    variable = variables[0]
    assert variable.name == 'intVar'
    assert variable.type_name == 'Int'
    assert not variable.is_non_null
    assert not variable.is_list

    variable = variables[1]
    assert variable.name == 'nonNullVar'
    assert variable.type_name == 'Int'
    assert variable.is_non_null
    assert not variable.is_list

    variable = variables[2]
    assert variable.name == 'listVar'
    assert variable.type_name == 'Int'
    assert not variable.is_non_null
    assert variable.is_list


def test_source(shared_datadir: Path) -> None:
    """Context should correctly return all kinds of operations."""
    query = _get_query(shared_datadir, """
        type OtherDefinition {
            id: Int
        }

        query testQuery {
            users {
                id
                username
            }
        }

        type AgainOtherDefinition {
            id: Int
        }
        """)
    assert query.name == 'testQuery'
    assert query.source == """query testQuery {
            users {
                id
                username
            }
        }"""


def _get_root(shared_datadir: Path, document_string: str) -> Root:
    document = parse_append_schema(shared_datadir, document_string)
    return Root(document)


def _get_query(datadir: Path, document_string: str) -> Operation:
    root = _get_root(datadir, document_string)
    queries = list(root.queries)
    assert len(queries) == 1
    return queries[0]


def _get_mutation(datadir: Path, document_string: str) -> Operation:
    root = _get_root(datadir, document_string)
    mutations = list(root.mutations)
    assert len(mutations) == 1
    return mutations[0]


def _get_subscription(datadir: Path, document_string: str) -> Operation:
    root = _get_root(datadir, document_string)
    subscriptions = list(root.subscriptions)
    assert len(subscriptions) == 1
    return subscriptions[0]
