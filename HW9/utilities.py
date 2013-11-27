import re 

class Utilities:
	def __init__(self):
		self.wordPosRegex = "/[^/]+$"

	def getWordPosTuple(self, str):
		match = re.search(self.wordPosRegex, str)
		
		if match:
			forwardSlashIndex = match.start()
			startOfPosIndex = forwardSlashIndex + 1
			endOfPosIndex = match.end()

			word = str[0:forwardSlashIndex]
			pos = str[startOfPosIndex:endOfPosIndex]

			return (word, pos)

		return None
