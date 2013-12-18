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

>>> bliss.run("CREATE TABLE contributors (firstname VARCHAR, lastname VARCHAR)")
>>> bliss.run("INSERT INTO contributors VALUES (?, ?)", [('Andrew', 'Kuchling'),
...                                                      ('James', 'Henstridge'),
...                                                      ('Daniele', 'Varrazzo'),
...                                                      ('Marc-Andre', 'Lemburg')])

Nothing impressive so far, creating a cursor and calling executemany would achieve
the same result.

one
---

`one` is the method to use when you know the result is a single row or only care
about one.

>>> bliss.one("SELECT firstname FROM contributors WHERE lastname='Lemburg'") # doctest: +SKIP
u'Marc-Andre'

The string, nothing but the string, which in my book beats:

>>> cursor = connection.cursor()
>>> cursor.execute("SELECT firstname FROM contributors WHERE lastname='Lemburg'") # doctest: +ELLIPSIS
<sqlite3.Cursor object at ...>
>>> cursor.fetchone() # doctest: +SKIP
(u'Marc-Andre',)

Even better, if the result contains several column, one returns a namedtuple_:

>>> bliss.one("SELECT * FROM contributors WHERE firstname='James'") # doctest: +SKIP
Record(firstname=u'James', lastname=u'Henstridge')

all
---

`all` is the method to use to retrieve all rows from a query.

>>> bliss.all("SELECT firstname FROM contributors") #doctest: +SKIP
[u'Andrew', u'James', u'Daniele', u'Marc-Andre']

It returns a list of namedtuples when appropriate:

>>> bliss.all("SELECT firstname, LENGTH(lastname) AS length FROM contributors") # doctest: +NORMALIZE_WHITESPACE +SKIP
[Record(firstname=u'Andrew', length=8),
 Record(firstname=u'James', length=10),
 Record(firstname=u'Daniele', length=8),
 Record(firstname=u'Marc-Andre', length=7)]

.. _DB API 2.0: http://www.python.org/dev/peps/pep-0249/
.. _postgres: https://postgres-py.readthedocs.org/en/latest/
.. _namedtuple: http://docs.python.org/3/library/collections.html#collections.namedtuple
