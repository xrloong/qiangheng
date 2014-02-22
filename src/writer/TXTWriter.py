class TXTWriter:
	def write(self, imInfo, codeMappingInfoList):
		table="\n".join(sorted(map(lambda x : '{0}\t{1}'.format(*x.getKey()), codeMappingInfoList)))
		print(table)

