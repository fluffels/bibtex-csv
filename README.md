bibtex-csv
==========

Converts bibtex files to CSV.

Overview
--------

This program converts bibliography databases stored in the BibTeX / BibLaTeX format to the comma-separated value format.

Dependencies
------------

This script requires Python 3.3.3.
It was not tested with other versions of Python.
Python 2 will definitely not work.

Usage
-----

Input is via standard input, output is via standard output.
Files can be processed using your operating system's built in file pipe / redirection operators (see examples below).

Examples
--------

* Converting a single .bib file:

```sh
./convert.py < bibliography.bib > spreadsheet.csv
```

* Converting multiple .bib files:

```sh
cat *.bib | ./convert.py > spreadsheet.csv

