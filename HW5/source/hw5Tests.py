import unittest
import ngrams


class CollectNGramsTest(unittest.TestCase):

  def test_BOS_EOS(self):
    testSent = """Pierre Vinken , 61 years old , will join the board as a nonexecutive director Nov. 29 .
Mr. Vinken is chairman of Elsevier N.V. , the Dutch publishing group .
Rudolph Agnew , 55 years old and former chairman of Consolidated Gold Fields PLC , was named a nonexecutive director of this British industrial conglomerate ."""

    NGramsObj = ngrams.NGrams()
#    print testSent
    actualResult = NGramsObj.BOS_EOS(testSent)
#    print actualResult
    self.assertTrue(actualResult == """<s> Pierre Vinken , 61 years old , will join the board as a nonexecutive director Nov. 29 . </s>
<s> Mr. Vinken is chairman of Elsevier N.V. , the Dutch publishing group . </s>
<s> Rudolph Agnew , 55 years old and former chairman of Consolidated Gold Fields PLC , was named a nonexecutive director of this British industrial conglomerate . </s>""")


  def test_unigrams(self):
    testSent = """John likes Mary"""

    NGramsObj = ngrams.NGrams()
#    print testSent
    actualResult = NGramsObj.count_unigrams(testSent)
#    print actualResult
    self.assertTrue(actualResult == [('<s>', 1), ('John', 1), ('</s>', 1), ('likes', 1), ('Mary', 1)])


  def test_bigrams(self):
    testSent = """I love my cat .
my cat loves me ."""

    NGramsObj = ngrams.NGrams()
    print testSent
    actualResult = NGramsObj.count_bigrams(testSent)
    print actualResult
    self.assertTrue(actualResult == [('my cat', 2), ('. </s>', 2), ('cat loves', 1), ('cat .', 1), ('<s> I', 1), ('<s> my', 1), ('love my', 1), ('me .', 1), ('I love', 1), ('loves me', 1)])


  def test_trigrams(self):
    testSent = """I love my cat .
my cat loves me ."""

    NGramsObj = ngrams.NGrams()
    print testSent
    actualResult = NGramsObj.count_trigrams(testSent)
    print actualResult
    self.assertTrue(actualResult == [('cat . </s>', 1), ('loves me .', 1), ('love my cat', 1), ('me . </s>', 1), ('my cat .', 1), ('my cat loves', 1), ('<s> my cat', 1), ('cat loves me', 1), ('<s> I love', 1), ('I love my', 1)])



def main():
	unittest.main()

if __name__ == '__main__':
	main()
