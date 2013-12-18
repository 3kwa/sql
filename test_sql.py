import sqlite3
from contextlib import closing

import pytest

import sql


@pytest.fixture
def connection():
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE test (a, b , c)")
    cursor.executemany("INSERT INTO test VALUES (?, ?, ?)",
                   (('A', 1, '101'),
                    ('B', 2, '202'),
                    ('C', 3, '303')))
    cursor.close()
    return connection

def test_one_column_select_one(connection):
    sql_ = sql.SQL(connection)
    assert sql_.one("SELECT SUM(b) FROM test") == 6

def test_parameterized_one(connection):
    sql_ = sql.SQL(connection)
    assert sql_.one("SELECT SUM(b) FROM test WHERE c != ?", ['202']) == 4

def test_make_record_ok(connection):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT a AS aa, c AS cc FROM test")
        Record = sql.SQL.make_record(cursor)
    assert hasattr(Record, 'aa')
    assert hasattr(Record, 'cc')

def test_make_record_none(connection):
    with closing(connection.cursor()) as cursor:
        cursor.execute("SELECT a AS aa FROM test")
        Record = sql.SQL.make_record(cursor)
    assert Record is None

def test_many_column_select_one(connection):
    sql_ = sql.SQL(connection)
    record = sql_.one("SELECT a, b FROM test WHERE c = '303'")
    assert (record.a, record.b) == ('C', 3)

def test_one_column_select_many(connection):
    sql_ = sql.SQL(connection)
    assert sql_.all("SELECT b FROM test") == [1, 2, 3]

def test_many_column_select_many(connection):
    sql_ = sql.SQL(connection)
    records = sql_.all("SELECT b, c FROM test ORDER BY a DESC")
    record = records[0]
    assert (record.b, record.c) == (3, '303')

def test_parameterized_all(connection):
    sql_ = sql.SQL(connection)
    records = sql_.all("SELECT a, b FROM test WHERE c IN (:1, :2) ORDER BY a",
                       ['101', '202'])
    assert [record.a for record in records] == ['A', 'B']

def test_run(connection):
    sql_ = sql.SQL(connection)
    record = sql_.run("DROP TABLE test")
    assert record is None
    with pytest.raises(sqlite3.OperationalError):
        sql_.one("SELECT COUNT(*) FROM test")

def test_parameterized_run_one(connection):
    sql_ = sql.SQL(connection)
    sql_.run("INSERT INTO test VALUES (:a, :b, :c)",
             {'a': 'D', 'b': 4, 'c': '404'})
    assert sql_.one("SELECT SUM(b) FROM test") == 10

def test_parameterized_run_many(connection):
    sql_ = sql.SQL(connection)
    sql_.run("INSERT INTO test VALUES (:a, :b, :c)",
             [{'a': 'D', 'b': 4, 'c': '404'}, {'a': 'E', 'b': 5, 'c': '505'}])
    assert sql_.one("SELECT SUM(b) FROM test") == 15

def test_which_execute_case_one_mapping():
    assert sql.SQL.which_execute({}) == 'execute'

def test_which_execute_case_one_plain_sequence_list():
    assert sql.SQL.which_execute([1, 2, 3]) == 'execute'

def test_which_execute_case_one_plain_sequence_tuple():
    assert sql.SQL.which_execute((1, 2, 3)) == 'execute'

def test_which_execute_case_many_sequence_list():
    assert sql.SQL.which_execute([[1], [2]]) == 'executemany'

def test_which_execute_case_many_sequence_tuple():
    assert sql.SQL.which_execute(([1], [2])) == 'executemany'

def test_which_execute_case_many_sequence_tuple_tuple():
    assert sql.SQL.which_execute(((1,), (2,))) == 'executemany'

def test_which_execute_case_many_sequence_tuple_dict():
    assert sql.SQL.which_execute(({'a': 1}, {'a': 2})) == 'executemany'

def test_which_execute_empty_list():
    assert sql.SQL.which_execute([]) == 'execute'
