import os

from distutils.core import setup

curdir = os.path.dirname(__file__)
readme = os.path.join(curdir, "README.rst")


def version():
    with open(os.path.join(curdir, "sql.py")) as f:
        for line in f:
            if line.startswith("__version__ = "):
                break
    version = line.partition(" = ")[-1]
    return version.replace('"', "").strip()


setup(
    name="sql",
    version=version(),
    description="DB API 2.0 for Humans",
    long_description=open(readme).read(),
    author="Eugene Van den Bulke",
    author_email="eugene.vandenbulke@gmail.com",
    url="http://github.com/3kwa/sql",
    py_modules=["sql"],
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries",
    ],
)
