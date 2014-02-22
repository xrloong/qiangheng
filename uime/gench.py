#!/usr/bin/env python3

import sys

start=int(sys.argv[1], 16)
end=int(sys.argv[2], 16)

for i in range(start, end+1):
	if i%256==0:
		print("# %X"%i)
		print("# U+    字      構      倉      行      易      嘸      嘸補    鄭      鄭類")
	print("U+%04X	%s	(龜)	XXXX	XXXX	XXXX	XXXX	XXXX	XXXX	XXXX"%(i, chr(i)))

