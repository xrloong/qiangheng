#!/usr/bin/env python3

import ruamel.yaml as yaml
import sys
from optparse import OptionParser

oparser = OptionParser()
oparser.add_option("-t", dest="type", help="type")
(options, args) = oparser.parse_args()
codeType = options.type

infile = args[0]

root = yaml.load(open(infile), yaml.cyaml.CSafeLoader)

if "對應集" in root:
	mappings = root["對應集"]

	for mapping in sorted(mappings, key=lambda m: m['按鍵序列']):
		variance = mapping['類型']

		toEnumerate = (codeType and variance=='標準') or codeType=='all'
		if not toEnumerate: continue

		keySequence = mapping['按鍵序列']
		character = mapping['字符']
		print("{}\t{}".format(keySequence, character))

if "描繪法" in root:
	mappings = root["描繪法"]

	for mapping in mappings:
		variance = mapping['類型']

		toEnumerate = (codeType and variance=='標準') or codeType=='all'
		if not toEnumerate: continue

		character = mapping['字符']
		attrib={"字符": character, "類型": variance}

		strokes = mapping['字圖']
		expressions = (stroke["描繪"] for stroke in strokes)
		print("{}\t{}".format(character, "/".join(expressions)))
