import unittest
import ngrams


class CollectNGramsTest(unittest.TestCase):

  def test_BOS_EOS(self):
    testSent1 = "Pierre Vinken , 61 years old , will join the board as a nonexecutive director Nov. 29 ."
    testSent2 = "Mr. Vinken is chairman of Elsevier N.V. , the Dutch publishing group ."
    testSent3 = "Rudolph Agnew , 55 years old and former chairman of Consolidated Gold Fields PLC , was named a nonexecutive director of this British industrial conglomerate ."""

    NGramsObj = ngrams.NGrams()
#    print testSent
    actualResult1 = NGramsObj.BOS_EOS(testSent1)
#    print actualResult1
    self.assertTrue(actualResult1 == "<s> Pierre Vinken , 61 years old , will join the board as a nonexecutive director Nov. 29 . </s>" + '\n')
    actualResult2 = NGramsObj.BOS_EOS(testSent2)
    self.assertTrue(actualResult2 == "<s> Mr. Vinken is chairman of Elsevier N.V. , the Dutch publishing group . </s>" + '\n')
    actualResult3 = NGramsObj.BOS_EOS(testSent3)
    self.assertTrue(actualResult3 == "<s> Rudolph Agnew , 55 years old and former chairman of Consolidated Gold Fields PLC , was named a nonexecutive director of this British industrial conglomerate . </s>" + '\n')


  def test_unigrams(self):
    testSent = """<s> John likes Mary </s>"""

    NGramsObj = ngrams.NGrams()
#    print testSent
    actualResult = NGramsObj.count_unigrams(testSent)
#    print actualResult
    self.assertTrue(actualResult == [('<s>', 1), ('John', 1), ('</s>', 1), ('likes', 1), ('Mary', 1)])


  def test_bigrams(self):
    testSent = """<s> I love my cat . </s>
<s> my cat loves me . </s>
"""

    NGramsObj = ngrams.NGrams()
#    print testSent
    actualResult = NGramsObj.count_bigrams(testSent)
#    print actualResult
    self.assertTrue(actualResult == [('my cat', 2), ('. </s>', 2), ('cat loves', 1), ('cat .', 1), ('<s> I', 1), ('<s> my', 1), ('love my', 1), ('me .', 1), ('I love', 1), ('loves me', 1)])


  def test_trigrams(self):
    testSent = """<s> I love my cat . </s>
<s> my cat loves me . </s>"""

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
   # print actualResult
    self.assertTrue(actualResult == [[7, 0.5833333333333334, -0.23408320603336796, 'c'], [3, 0.25, -0.6020599913279624, 'a'], [2, 0.16666666666666666, -0.7781512503836436, 'b']])


  def test_UnigramreadIntoDict(self):
    teststr = "100 but"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_into_dicts(teststr)
    self.assertTrue(NGramsObj.uni_dict["but"] == 100)


  def test_BigramReadIntoDict(self):
    teststr = "100 but if"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_into_dicts(teststr)
    self.assertTrue(NGramsObj.bi_dict["but if"] == 100)


  def test_TrigramReadIntoDict(self):
    teststr = "100 but what if"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_into_dicts(teststr)
    self.assertTrue(NGramsObj.tri_dict["but what if"] == 100)


  def test_readIntoDict(self):
    teststr1 = "100 but"
    teststr2 = "100 but if"
    teststr3 = "100 but what if"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_into_dicts(teststr1)
    NGramsObj.read_into_dicts(teststr2)
    NGramsObj.read_into_dicts(teststr3)
    self.assertTrue(NGramsObj.uni_dict["but"] == 100)
    self.assertTrue(NGramsObj.bi_dict["but if"] == 100)
    self.assertTrue(NGramsObj.tri_dict["but what if"] == 100)


  def test_CalcBiProbs(self):
    testdict2 = {'alpha zulu': 3, 'bravo yankee': 2, 'charlie xray': 7}
    testdict1 = {'alpha': 6, 'zulu': 3, 'bravo': 9, 'yankee': 2, 'charlie': 12, 'xray': 7}


    NGramsObj = ngrams.NGrams()
    NGramsObj.bi_dict = testdict2
    NGramsObj.uni_dict = testdict1
    actualResult = NGramsObj.calc_bi_prob()
#    print actualResult
    self.assertTrue(actualResult == [[7, 0.5833333333333334, -0.23408320603336796, 'charlie xray'], [3, 0.5, -0.3010299956639812, 'alpha zulu'], [2, 0.2222222222222222, -0.6532125137753437, 'bravo yankee']])


  def test_CalcTriProbs(self):
    testdict3 = {'alpha zulu bravo': 1, 'bravo yankee charlie': 4, 'charlie xray alpha': 5}
    testdict2 = {'alpha zulu': 3, 'bravo yankee': 2, 'charlie xray': 7}
    testdict1 = {'alpha': 6, 'zulu': 3, 'bravo': 9, 'yankee': 2, 'charlie': 12, 'xray': 7}


    NGramsObj = ngrams.NGrams()
    NGramsObj.tri_dict = testdict3
    NGramsObj.bi_dict = testdict2
    NGramsObj.uni_dict = testdict1
    actualResult = NGramsObj.calc_tri_prob()
#    print actualResult
    self.assertTrue(actualResult == [[5, 0.7142857142857143, -0.146128035678238, 'charlie xray alpha'], [4, 2.0, 0.3010299956639812, 'bravo yankee charlie'], [1, 0.3333333333333333, -0.47712125471966244, 'alpha zulu bravo']])


  def test_readLMIntoDict(self):
    teststr1 = "1000 0.0391374114516 -1.40740790197 <s>"
    teststr2 = ""
    teststr3 = "1 0.2 -0.698970004336 executives drooled"
    teststr4 = "\\3-grams:" 
    teststr5 = "1 0.333333333333 -0.47712125472 20 % and"

    NGramsObj = ngrams.NGrams()
    NGramsObj.read_lm_file_into_dicts(teststr1)
    NGramsObj.read_lm_file_into_dicts(teststr2)
    NGramsObj.read_lm_file_into_dicts(teststr3)
    NGramsObj.read_lm_file_into_dicts(teststr4)
    NGramsObj.read_lm_file_into_dicts(teststr5)
    self.assertTrue(NGramsObj.uni_dict["<s>"] == "0.0391374114516")
    self.assertTrue(NGramsObj.read_into_dicts(teststr2) == None)
    self.assertTrue(NGramsObj.bi_dict["executives drooled"] == "0.2")
    self.assertTrue(NGramsObj.read_into_dicts(teststr4) == None)
    self.assertTrue(NGramsObj.tri_dict["20 % and"] == "0.333333333333")


  def test_readLMIntoDict_1(self):
    teststr = "<s> Influential members of the House Ways and Means Committee introduced legislation that would restrict how the new savings-and-loan bailout agency can raise capital , creating another potential obstacle to the government 's sale of sick thrifts . </s>"
    l1 = 0.2
    l2 = 0.3
    l3 = 0.5

    NGramsObj = ngrams.NGrams()

    idx = 0
    fileStream = open("../examples/lm_ex")
    t = fileStream.readline() 
    while t:
      idx += 1
      if idx < 6:
        t = fileStream.readline()
        continue
      NGramsObj.read_lm_file_into_dicts(t)
      t = fileStream.readline()

    perp = NGramsObj.Perplexity(teststr, l1, l2, l3)
    print perp
    self.assertTrue(perp == (-82.8860891791949, 37) )



def main():
	unittest.main()

if __name__ == '__main__':
	main()
