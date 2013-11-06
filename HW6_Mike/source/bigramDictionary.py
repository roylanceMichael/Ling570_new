class BigramDictionary:
### I think we want a hash of hashes here
### the first key will represent what bigram we're looking for
### IE if we have the sentence she walked to the store
### walked | she => we want walked to be the key
### then walked would have a list of hashes that would contain
### the keys and the counts
	def __init__(self):
		self.dictionary = { }

	def buildKeyAndSetItem(self, word, pos):
		key = word + "~" + pos