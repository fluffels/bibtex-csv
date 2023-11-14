#!/usr/bin/env python3

"""
This is a simple (and probably broken) Python script that converts BibTeX
entries to CSV.

Input is via standard input.
Output is via standard output.
"""

from re import match
from re import search
from re import findall
from sys import stdin
from string import capwords

entries = []
entry = {}
key = None

for line in stdin:
    if match('^@', line.strip()):
        if entry != {}:
            entries.append(entry)
            entry = {}
        entry['label'] = findall('^@.+{([^,]+),?', line.strip())[0]
    elif match('url', line.strip()):
        value = findall('[{"](\S+)[}"]', line)[0]
        entry["url"] = value
    elif search('=', line.strip()):
        key, value = [v.strip(' {},\n"') for v in line.split("=", maxsplit=1)]
        entry[key] = value
    elif entry != {}:
        # This line is part of the previous key
        entry[key] += (' ' + line.strip(' {},\n"'))
    else:
        raise ValueError('Incorrectly formatted line', line)

entries.append(entry)

for entry in entries:
    for key in entry.keys():
        entry[key] = entry[key].strip().replace('\n', ' ').replace('\t', ' ')
    author = "Anonymous"
    if "author" in entry:
        author = entry["author"]
    elif "authors" in entry:
        author = entry["authors"]
    elif "editor" in entry:
        author = entry["editor"]
    
    title = "No title"
    if "title" in entry:
        title = entry["title"]

    publish = "No publishing information"
    if "journal" in entry:
        publish = entry["journal"]
    if "journaltitle" in entry:
        publish = entry["journaltitle"]
    elif "booktitle" in entry:
        publish = entry["booktitle"]
    elif "howpublished" in entry:
        publish = entry["howpublished"]
    elif "type" in entry:
        publish = entry["type"]
    elif "url" in entry:
        publish = "Website: {}".format(entry["url"])
    elif "crossref" in entry:
        publish = entry["crossref"].replace("_", " ")
        publish = capwords(publish)
    elif "publisher" in entry:
        publish = entry["publisher"]
    
    year = "Unknown year"
    if "year" in entry:
        year = entry["year"]

    label = entry['label']

    print("{}\t{}\t{}\t{}\t{}".format(author, title, year, publish, label))
