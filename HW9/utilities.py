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

	def getModifiedWordTagTuple(self, wordTags, index, modifier):
		modifiedIndex = index + modifier
		
		# make sure we're within bounds
		if len(wordTags) > modifiedIndex and modifiedIndex > -1:
			return wordTags[modifiedIndex]

		return None
