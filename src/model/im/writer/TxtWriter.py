class TxtWriter:
	def write(self, imInfo, codeMappingInfoList):
		table="\n".join(map(lambda x : '{0}\t{1}'.format(*x.getKey()), codeMappingInfoList))
		print(table)

