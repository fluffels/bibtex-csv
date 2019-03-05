#!/usr/bin/env python3

"""
This is a simple (and probably broken) Python script that converts BibTeX
entries to CSV.

Input is via standard input.
Output is via standard output.
"""

import os
import sys
from os import getcwd
from os import listdir
from re import match
from re import search
from re import findall
from re import fullmatch
from re import sub
from sys import stdin
from string import capwords
import argparse

def bib2csv (bib_lines, output_file_path):
	entries = []
	entry = {}

	count = 0

	for line in bib_lines:
		if (match('^@', line.strip())): # Match the bibkey
			match_obj = search ('\{(\S+),', line)
			if match:
				curr_bibkey = match_obj[0][1:-1]

			if entry != {}:
				entries.append (entry)
				entry = {}

			entry['bibkey'] = curr_bibkey # Store the sentinel bibkey
		elif (match('url', line.strip())): # Match the url
			# value, = findall('\{(\S+).*(\S+)\}', line)
			# value = match('\{(\S+).*(\S+)\}', line)
			value = [v.strip(" ,\n") for v in line.split("=", maxsplit=1)][1]
			entry["url"] = value
		elif (search('=', line.strip())): # Match everything else
			if (search ('author', line.strip ())):
				key, value = [v.strip(" ,\n") for v in line.split("=", maxsplit=1)]
			elif (search ('title', line.strip ())):
				key, value = [v.strip(" ,\n") for v in line.split("=", maxsplit=1)]
			else:
				key, value = [v.strip(" {},\n") for v in line.split("=", maxsplit=1)]
			entry[key] = value

	## Grab the last entry that will have been missed
	if entry != {}:
		entries.append (entry)
		entry = {}

	print ('Writing csv file...')
	with open (output_file_path, 'w', encoding='utf8') as fp:
		fp.write ("{}<>{}<>{}<>{}<>{}<>{}<>{}<>{}".format("bibkey", "author", "title", "year", "url", "publisher", "doi", "keywords") + '\n')
		for entry in entries:
			bibkey = ''
			if 'bibkey' in entry:
				bibkey = entry['bibkey']

			author = "Anonymous"
			if "author" in entry:
				author = entry["author"].strip ('{} ')
			elif "authors" in entry:
				author = entry["authors"].strip ('{} ')
			elif "editor" in entry:
				author = entry["editor"].strip ('{} ')
			
			title = "No title"
			if "title" in entry:
				title = entry["title"].strip ('{} ')

			url = 'No URL'
			if 'url' in entry:
				url = entry['url'].strip ('{} ')

			publisher = "No publishing information"
			if "journal" in entry:
				publisher = entry["journal"].strip ('{} ')
			if "journaltitle" in entry:
				publisher = entry["journaltitle"].strip ('{} ')
			elif "booktitle" in entry:
				publisher = entry["booktitle"].strip ('{} ')
			elif "howpublished" in entry:
				publisher = entry["howpublished"].strip ('{} ')
			elif "type" in entry:
				publisher = entry["type"].strip ('{} ')
			elif "crossref" in entry:
				publisher = entry["crossref"].replace("_", " ").strip ('{} ')
				publish = capwords(publish)
			elif "publisher" in entry:
				publisher = entry["publisher"].strip ('{} ')
			
			year = "Unknown year"
			if "year" in entry:
				year = entry["year"].strip ('{} ')

			doi = 'Unknown DOI'
			if 'doi' in entry:
				doi = entry['doi'].strip ('{} ')

			keywords = 'No Keywords'
			if 'keywords' in entry:
				keywords = entry['keywords'].strip ('{} ')

			# print("{}\t{}\t{}\t{}".format(author, title, year, publish))
			fp.write ("{}<>{}<>{}<>{}<>{}<>{}<>{}<>{}".format(bibkey, author, title, year, url, publisher, doi, keywords) + '\n')

def csv2bib (csv_lines, output_file):
	entries = []

	## For reference
	# entry = """
	# @article{@bibkey@,
	# author = {@author@},
	# title = {@title@},
	# year = {@year@},
	# publish = {@publish@},
	# doi = {@doi@},
	# keywords = {@keywords@}
	# }
	# """

	for line in csv_lines[1:]: # Skip the csv header
		# print (line)
		# print (line.split ('\t'))
		# for item in line.split ('\t'):
		# 	print (item)
		# print ('Number of items:', len (line.split ('\t')))
		bibkey, author, title, year, url, publisher, doi, keywords = line.split('<>')
		entry = '' + sub ('@bibkey@', bibkey, '@article{@bibkey@,') + '\n'
		entry = entry + sub ('@author@', author, 'author = {@author@},') + '\n'
		entry = entry + sub ('@title@', title, 'title = {@title@},') + '\n'
		entry = entry + sub ('@year@', year, 'year = {@year@},') + '\n'
		entry = entry + sub ('@publisher@', publisher, 'publisher = {@publisher@},') + '\n'
		entry = entry + sub ('@url@', url, 'url = {@url@},') + '\n'
		entry = entry + sub ('@doi@', doi, 'doi = {@doi@},') + '\n'
		entry = entry + sub ('@keywords@', keywords, 'keywords = {@keywords@},') + '\n'
		entry = entry + '}' '\n'
		entries.append (entry)

	print ('Writing bib file...')
	with open (output_file_path, 'w', encoding='utf8') as fp:
	# with open (output_file_path, 'w') as fp:
		for line in entries:
			fp.write (line)

def main (input_file_path, output_file_path, conversion_flag):
	with open (input_file_path, 'r', encoding='utf8') as fp:
		input_lines = fp.readlines ()

	## Remove whitespace
	# input_lines = [line.strip () for line in input_lines]

	if conversion_flag:
		print ('Loaded input bib file. Converting to csv...')
		bib2csv (input_lines, output_file_path)
	else:
		print ('Loaded input csv file. Converting to bib...')
		csv2bib (input_lines, output_file_path)

if __name__ == '__main__':
	parser = argparse.ArgumentParser (description='Converts a bib file to a csv spreadsheet')
	parser.add_argument (dest='input_file', help='The bib file to convert')
	parser.add_argument (dest='output_file', help='The csv file to output')
	group = parser.add_mutually_exclusive_group (required=True)
	group.add_argument ('-b', '--to-bib', dest='to_bib', action='store_true', help='Convert a csv file to a bib file')
	group.add_argument ('-c', '--to-csv', dest='to_csv', action='store_true', help='Convert a bib file to a csv file')

	args = parser.parse_args ()

	## Load the file
	input_file_path = os.path.abspath (args.input_file)
	output_file_path = os.path.abspath (args.output_file)
	if not os.path.exists (input_file_path) or os.path.isdir (input_file_path):
		print ('Input file doesn\'t exist or is a directory. Aborting...')
		sys.exit ()

	conversion_flag = True
	if args.to_bib:
		conversion_flag = False

	main (input_file_path, output_file_path, conversion_flag)



