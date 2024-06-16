#!/usr/bin/env python3

import ruamel.yaml
import sys
from optparse import OptionParser

oparser = OptionParser()
oparser.add_option("-t", dest="type", help="type")
(options, args) = oparser.parse_args()
codeType = options.type

infile = args[0]

yaml = ruamel.yaml.YAML()
root = yaml.load(open(infile))

codingType = root["編碼類型"]
if "編碼集" in root:
    mappings = root["編碼集"]

    if codingType == "輸入法":
        for mapping in sorted(mappings, key=lambda m: m["按鍵序列"]):
            variance = mapping["類型"]

            toEnumerate = (codeType and variance == "標準") or codeType == "all"
            if not toEnumerate:
                continue

            keySequence = mapping["按鍵序列"]
            character = mapping["字符"]
            print("{}\t{}".format(keySequence, character))
    elif codingType == "描繪法":
        for mapping in mappings:
            variance = mapping["類型"]

            toEnumerate = (codeType and variance == "標準") or codeType == "all"
            if not toEnumerate:
                continue

            character = mapping["字符"]
            attrib = {"字符": character, "類型": variance}

            strokes = mapping["字圖"]
            expressions = (stroke["描繪"] for stroke in strokes)
            print("{}\t{}".format(character, "/".join(expressions)))
    else:
        pass
