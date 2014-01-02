import os

from distutils.core import setup

curdir = os.path.dirname(__file__)
readme = os.path.join(curdir, 'README.rst')

setup(
    name='sql',
    version='0.3.0',
    description='DB API 2.0 for Humans',
    long_description=open(readme).read(),
    author='Eugene Van den Bulke',
    author_email='eugene.vandenbulke@gmail.com',
    url='http://github.com/3kwa/sql',
    py_modules=['sql'],
    license='BSD',
    classifiers=[
    'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries'
        ],
     )
