import re
import transitionState

class Utilities:
	def processYesNo(self, boolVal):
		if(boolVal == True):
			return 'Yes'
		else:
			return 'No'

	def readLexicon(self, strVal):
		# first, split the string into many lines
		strLines = re.split("\n", strVal.strip())

		lexiconItems = {}

		# second, go through each line
		for i in range(0, len(strLines)):
			# next, split this line by white space
			wordsInLine = re.split("\s+", strLines[i].strip())

			if(len(wordsInLine) != 2):
				continue

			if(lexiconItems.has_key(wordsInLine[1])):
				wordsList = lexiconItems[wordsInLine[1]]
				wordsList.append(wordsInLine[0])
			else:
				lexiconItems[wordsInLine[1]] = [ wordsInLine[0]]

		return lexiconItems

	def cleanseInput(self, strVal):
		if(strVal == None):
			return ''
		return re.sub(r'\"', '', re.sub(r'\'', '', strVal))

	def valsBeforeParen(self, strVal):
		parenIdx = len(strVal)

		for i in range(0, len(strVal)):
			if(strVal[i] == '('):
				parenIdx = i
				break

		subStr = strVal[0:parenIdx]
		return re.split("\s+", subStr)

	def parenIndex(self, strVal):
		parenStart = -1
		leftParenCount = 0

		for i in range(0, len(strVal)):
			currentChar = strVal[i]

			if(currentChar == '('):
				
				if(parenStart == -1):
					parenStart = i
				
				leftParenCount = leftParenCount + 1
			elif(currentChar == ')'):
				leftParenCount = leftParenCount - 1

				if(leftParenCount == 0):
					# dictionary fine
					return { 'start': parenStart+1, 'end': i }

		return { 'start': -1, 'end': -1 }

	def createTransitionState(self, strVal):
		parenIndexes = self.parenIndex(strVal)

		if(parenIndexes['start'] == -1):
			return {}

		# business rules
		# 1) identify where the paren is
		# 2) get the first item
		# 3) get the next paren list
		# 4) get list of those items, they will be in the second level

		workSpace = strVal[parenIndexes['start']:parenIndexes['end']]
		fromStateValue = self.valsBeforeParen(workSpace)[0]

		transitionStates = []

		# at this point, I need to process all of the remaining parens
		otherParenIndexes = self.parenIndex(workSpace)

		while(otherParenIndexes['start'] != -1):
			toStateSubStr = workSpace[otherParenIndexes['start']:otherParenIndexes['end']]
			
			toStateValues = self.valsBeforeParen(toStateSubStr)
			
			tempTransitionState = transitionState.TransitionState(
				fromStateValue,
				toStateValues.pop(0),
				self.cleanseInput(toStateValues.pop(0)),
				toStateValues)

			transitionStates.append(tempTransitionState)

			if(len(workSpace) == otherParenIndexes['end']):
				break
			else:
				workSpace = workSpace[(otherParenIndexes['end']+1):]
				otherParenIndexes = self.parenIndex(workSpace)

		return transitionStates