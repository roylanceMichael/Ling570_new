import unittest
import utilities
import bigramDictionary

class UtilitiesTest(unittest.TestCase):
	def test_createsBigramTuplesFromStr(self):
		testSent = "<s>/BOS John/N likes/V Mary/N </s>/EOS"

		utils = utilities.Utilities()

		result = utils.createBigramTuplesFromStr(testSent)

		self.assertTrue(4, len(result))

		self.assertTrue(result[0][0] == "BOS", result[0][0])
		self.assertTrue(result[0][1] == "N")

		self.assertTrue(result[1][0] == "N")
		self.assertTrue(result[1][1] == "V")

		self.assertTrue(result[2][0] == "V")
		self.assertTrue(result[2][1] == "N")

		self.assertTrue(result[3][0] == "N")
		self.assertTrue(result[3][1] == "EOS", result[3][1])

class NgramDictionaryTest(unittest.TestCase):
	def test_unigrams(self):
		testSent = """<s>/BOS John/N likes/V Mary/N </s>/EOS"""

		# print actualResult
    	# self.assertTrue(actualResult == [('<s>', 1), ('John', 1), ('</s>', 1), ('likes', 1), ('Mary', 1)])


def main():
	unittest.main()

if __name__ == '__main__':
	main()