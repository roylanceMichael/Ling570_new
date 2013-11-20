import re


class Convert:
	def separateWordsFromPOS(self, line):
	### separate input lines by "=>" and get rid of the probability in the end of the line
		match = re.search('(.+)=>(\D+)\s+([-?]-*\d*\.*\d*)$', line)
		if match:
			words = match.group(1)
			pos = match.group(2)
#			prob = match.group(3)
			return (words, pos)	# return two strings
		
		else:
			return line
#		return (words, pos)	# return two strings


	def ReadObsStr(self, StrVal):
	### split by whitespace
                splitVals = re.split("\s+", StrVal.strip())
                return splitVals


	def bigramOrTrigram(self, posList):
	### check if the POS tags are bigrams or trigrams
		match = re.search('(.+)[~\-\_](.+)', posList[0])
		
		if match:
			newPosList = []
			for tag in posList:
				match = re.search('(.+)[~\-\_](.+)', tag)
				newPosList.append(match.group(2))	# if it is a trigram we are only interested in the toState

		else:
			newPosList = posList

		return newPosList


	def wordTag(self, line):
	### print word followed by tag
		tup = self.separateWordsFromPOS(line)
		if len(tup) != 2:
			return tup.strip()
		else:
			wordsList = self.ReadObsStr(tup[0])
			pos = self.ReadObsStr(tup[1])[1:]	# ignore first tag - BOS
			posList = self.bigramOrTrigram(pos)
			strBuilder = ''
			if len(wordsList) == len(posList):
				for i in range(0, len(wordsList)):
					strBuilder = strBuilder + wordsList[i] + '/' + posList[i] + ' ' 
			return strBuilder
