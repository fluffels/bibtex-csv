#!/usr/bin/env python3

"""
This is a simple (and probably broken) Python script that converts BibTeX
entries to CSV.

Input is via standard input.
Output is via standard output.
"""

"""
Added in argparse and fixed some issues
with the conversion process
@author Daniel J. Finnegan
"""

import os
import sys
from os import getcwd
from os import listdir
from re import match
from re import search
from re import findall
from sys import stdin
from string import capwords
import argparse

def main (bib_lines, output_file_path):
	entries = []
	entry = {}

	for line in bib_lines:
		# print (line)
		if (match('^@', line.strip())):
			if entry != {}:
				entries.append(entry)
				entry = {}
		elif (match('url', line.strip())):
			value, = findall('\{(\S+).*(\S+)\}', line)
			entry["url"] = value
		elif (search('=', line.strip())):
			key, value = [v.strip(" {},\n") for v in line.split("=", maxsplit=1)]
			entry[key] = value

	print ('Writing csv file...')
	with open (output_file_path, 'w', encoding='utf8') as fp:
		fp.write ("{}\t{}\t{}\t{}".format('author', 'title', 'year', 'publish'))
		for entry in entries:
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

			# print("{}\t{}\t{}\t{}".format(author, title, year, publish))
			fp.write ("{}\t{}\t{}\t{}".format(author, title, year, publish))

if __name__ == '__main__':
	parser = argparse.ArgumentParser (description='Converts a bib file to a csv spreadsheet')
	parser.add_argument (dest='input_file', help='The bib file to convert')
	parser.add_argument (dest='output_file', help='The csv file to output')

	args = parser.parse_args ()

	## Load the file
	input_file_path = os.path.abspath (args.input_file)
	output_file_path = os.path.abspath (args.output_file)
	if not os.path.exists (input_file_path) or os.path.isdir (input_file_path):
		print ('Input file doesn\'t exist or is a directory. Aborting...')
		sys.exit ()

	with open (input_file_path, 'r', encoding='utf8') as fp:
		bib_lines = fp.readlines ()

	print ('Loaded input bib file. Converting to csv...')
	main(bib_lines, output_file_path)



