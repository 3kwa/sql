from distutils.core import setup

setup(
    name='sql',
    version='0.1.1',
    description='DB API 2.0 for Humans',
    long_description=open('README.rst').read(),
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
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries'
        ],
     )
