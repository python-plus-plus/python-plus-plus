# python++

[![Build Status](https://badge.fury.io/py/python-plus-plus.svg)](https://pypi.python.org/pypi/python-plus-plus)

Python++ is a transpiled superset of Python 3 that aims to address several commonly complained about aspects of Python by implementing the following features:

1. Addition of tail call optimization for self-recursive functions
2. Immutable default arguments by default
3. Object deep copy by default when using the * operator
4. Addition of increment (++) and decrement (--) operators

## Install

The easiest way to install Python++ is using pip, you can install from PyPI using the following command:
> $ pip install python-plus-plus  

Alternatively, you can install from source:
>  $ git clone https://github.com/python-plus-plus/python-plus-plus.git  
>  $ cd python-plus-plus  
>  $ python setup.py install

## Usage

When provided with the path to a valid `.ppp` source file, the Python++ transpiler will output a standard Python 3 compatible `.py` file with the same name and execute the transpiled code in the Python interpreter:
> $ ppp source.ppp  