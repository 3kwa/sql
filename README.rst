===
sql
===


Why?
====

`DB API 2.0`_ works. ORMs are convenient but sometimes overkill. ``sql`` is a
lightweight wrapper sitting on top of any DB API 2.0 connection offering a
postgres_ like interface which makes working with SQL results bliss.

How?
====

>>> import sqlite3
>>> connection = sqlite3.connect(':memory:')

>>> import sql
>>> bliss = sql.SQL(connection)

run
---

`run` is the method to use when you want to run a query but do not care about
the result e.g. to create a table:

>>> bliss.run("CREATE TABLE contributors (firstname VARCHAR, lastname VARCHAR)") #doctest: +ELLIPSIS
<sql.SQL object ...>
>>> bliss.run("INSERT INTO contributors VALUES (?, ?)", [('Andrew', 'Kuchling'),
...                                                      ('James', 'Henstridge'),
...                                                      ('Daniele', 'Varrazzo'),
...                                                      ('Marc-Andre', 'Lemburg')]) #doctest: +ELLIPSIS
<sql.SQL object ...>

Nothing impressive so far, creating a cursor and calling executemany would achieve
the same result.

commit
------

Added in version `2022.4.0` 

>>> bliss.run("INSERT INTO contributors VALUES (?, ?)", ("Chad", "Whitacre")) #doctest: +ELLIPSIS
<sql.SQL object ...>
>>> bliss.commit() 

Just because it is shorter than `bliss.connection.commit()`

`run` returns self so `commit` can be chained

>>> bliss.run("INSERT INTO contributors VALUES (?, ?)", ("Guido", "van Rossum")).commit()

one
---

`one` is the method to use when you know the result is a single row or only care
about one.

>>> bliss.one("SELECT firstname FROM contributors WHERE lastname='Lemburg'")
'Marc-Andre'

The string, nothing but the string, which in my book beats:

>>> cursor = connection.cursor()
>>> cursor.execute("SELECT firstname FROM contributors WHERE lastname='Lemburg'") # doctest: +ELLIPSIS
<sqlite3.Cursor object at ...>
>>> cursor.fetchone()
('Marc-Andre',)

Even better, if the result contains several column, one returns a namedtuple_:

>>> bliss.one("SELECT * FROM contributors WHERE firstname='James'")
Record(firstname='James', lastname='Henstridge')

all
---

`all` is the method to use to retrieve all rows from a query.

>>> bliss.all("SELECT firstname FROM contributors")
['Andrew', 'James', 'Daniele', 'Marc-Andre', 'Chad', 'Guido']

It returns a list of namedtuples when appropriate:

>>> bliss.all("SELECT firstname, LENGTH(lastname) AS length FROM contributors")
[Record(firstname='Andrew', length=8), Record(firstname='James', length=10), Record(firstname='Daniele', length=8), Record(firstname='Marc-Andre', length=7), Record(firstname='Chad', length=8), Record(firstname='Guido', length=10)]

.. _DB API 2.0: http://www.python.org/dev/peps/pep-0249/
.. _postgres: https://postgres-py.readthedocs.org/en/latest/
.. _namedtuple: http://docs.python.org/3/library/collections.html#collections.namedtuple
