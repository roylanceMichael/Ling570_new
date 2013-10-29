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
  #  print actualResult
    self.assertTrue(actualResult == [('<s>', 1), ('John', 1), ('</s>', 1), ('likes', 1), ('Mary', 1)])


  def test_bigrams(self):
    testSent = """I love my cat .
my cat loves me ."""

    NGramsObj = ngrams.NGrams()
#    print testSent
    actualResult = NGramsObj.count_bigrams(testSent)
#    print actualResult
    self.assertTrue(actualResult == [('my cat', 2), ('. </s>', 1), ('cat loves', 1), ('cat .', 1), ('<s> I', 1), ('<s> my', 1), ('love my', 1), ('me .', 1), ('I love', 1), ('loves me', 1)])


  def test_trigrams(self):
    testSent = """I love my cat .
my cat loves me ."""

    NGramsObj = ngrams.NGrams()
#    print testSent
    actualResult = NGramsObj.count_trigrams(testSent)
 #   print actualResult
    self.assertTrue(actualResult == [('cat . </s>', 1), ('loves me .', 1), ('love my cat', 1), ('me . </s>', 1), ('my cat .', 1), ('my cat loves', 1), ('<s> my cat', 1), ('cat loves me', 1), ('<s> I love', 1), ('I love my', 1)])



class Count_NGrams(unittest.TestCase):

  def test_countTypesTokens(self):
    testdict = {'a': 3, 'b': 2, 'c': 7}
    
    NGramsObj = ngrams.NGrams()
    actualResult = NGramsObj.count_types_tokens(testdict)
    self.assertTrue(actualResult == (3,12))


  def test_CalcUniProbs(self):
    testdict = {'a': 3, 'b': 2, 'c': 7}
    
    NGramsObj = ngrams.NGrams()
    NGramsObj.uni_dict = testdict
    actualResult = NGramsObj.calc_uni_prob()
    self.assertTrue(actualResult == [[3, 0.25, -0.6020599913279624, 'a'], [7, 0.5833333333333334, -0.23408320603336796, 'c'], [2, 0.16666666666666666, -0.7781512503836436, 'b']])


  def test_UnigramreadIntoDict(self):
    teststr = "100 but"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_into_dicts(teststr)
    self.assertTrue(NGramsObj.uni_dict["but"] == "100")


  def test_BigramReadIntoDict(self):
    teststr = "100 but if"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_into_dicts(teststr)
    self.assertTrue(NGramsObj.bi_dict["but if"] == "100")


  def test_TrigramReadIntoDict(self):
    teststr = "100 but what if"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_into_dicts(teststr)
    self.assertTrue(NGramsObj.tri_dict["but what if"] == "100")


  def test_readIntoDict(self):
    teststr1 = "100 but"
    teststr2 = "100 but if"
    teststr3 = "100 but what if"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_into_dicts(teststr1)
    NGramsObj.read_into_dicts(teststr2)
    NGramsObj.read_into_dicts(teststr3)
    self.assertTrue(NGramsObj.uni_dict["but"] == "100")
    self.assertTrue(NGramsObj.bi_dict["but if"] == "100")
    self.assertTrue(NGramsObj.tri_dict["but what if"] == "100")


  def test_CalcBiProbs(self):
    testdict2 = {'alpha zulu': 3, 'bravo yankee': 2, 'charlie xray': 7}
    testdict1 = {'alpha': 6, 'zulu': 3, 'bravo': 9, 'yankee': 2, 'charlie': 12, 'xray': 7}


    NGramsObj = ngrams.NGrams()
    NGramsObj.bi_dict = testdict2
    NGramsObj.uni_dict = testdict1
    actualResult = NGramsObj.calc_bi_prob()
    self.assertTrue(actualResult == [[2, 0.2222222222222222, -0.6532125137753437, 'bravo yankee'], [3, 0.5, -0.3010299956639812, 'alpha zulu'], [7, 0.5833333333333334, -0.23408320603336796, 'charlie xray']])


  def test_CalcTriProbs(self):
    testdict3 = {'alpha zulu bravo': 1, 'bravo yankee charlie': 4, 'charlie xray alpha': 5}
    testdict2 = {'alpha zulu': 3, 'bravo yankee': 2, 'charlie xray': 7}
    testdict1 = {'alpha': 6, 'zulu': 3, 'bravo': 9, 'yankee': 2, 'charlie': 12, 'xray': 7}


    NGramsObj = ngrams.NGrams()
    NGramsObj.tri_dict = testdict3
    NGramsObj.bi_dict = testdict2
    NGramsObj.uni_dict = testdict1
    actualResult = NGramsObj.calc_tri_prob()
    self.assertTrue(actualResult == [[1, 0.3333333333333333, -0.47712125471966244, 'alpha zulu bravo'], [5, 0.7142857142857143, -0.146128035678238, 'charlie xray alpha'], [4, 2.0, 0.3010299956639812, 'bravo yankee charlie']])





def main():
	unittest.main()

if __name__ == '__main__':
	main()
