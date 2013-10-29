from __future__ import division
import sys
import re
import math


class NGrams:
  def __init__(self):
### what to put here???
    self.uni_dict = {}
    self.unitypes = 0
    self.unitokens = 0
    self.bi_dict = {}
    self.bitypes = 0
    self.bitokens = 0
    self.tri_dict = {}
    self.tritypes = 0
    self.tritokens = 0


  def BOS_EOS(self, text):
### insert beginning and end of string tags
    text = re.sub(r'^', '<s> ', text, flags=re.MULTILINE)
    text = re.sub(r'$', ' </s>', text, flags=re.MULTILINE)
    
    return text


  def count_unigrams(self, text):
### get unigrams; stuff in the dictionary; count and sort 
    list_all = self.BOS_EOS(text)
#    uni_dict = {}
    for token in list_all.split():
    #  print token
      if not token in self.uni_dict:
        self.uni_dict[token] = 1
      else:
        self.uni_dict[token] = self.uni_dict[token] + 1
    self.uni_dict = sorted(self.uni_dict.items(), key = lambda a: -a[1])
    return self.uni_dict
   

  def count_bigrams(self, text):
### get bigrams; stuff in the dictionary; count; sort
    list_all = self.BOS_EOS(text)
    t = list_all.split()

#    print t
#    self.bi_dict = {} 
    for i in range(0, len(t)-2):
 #     print t[i] + ' ' + t[i+1]
      bigram = t[i] + ' ' + t[i+1]
      if not bigram in self.bi_dict and not t[i] == '</s>':
        self.bi_dict[bigram] = 1
      elif t[i] == '</s>':
        continue
      else:
        self.bi_dict[bigram] = self.bi_dict[bigram] + 1

    self.bi_dict = sorted(self.bi_dict.items(), key = lambda a: -a[1])
    return self.bi_dict 
   

  def count_trigrams(self, text):
### count trigrams
    list_all = self.BOS_EOS(text)
    t = list_all.split()
  #  print t
 #   tri_dict = {}
    for i in range(0, len(t)-2):
#      print t[i] + ' ' + t[i+1] + ' ' + t[i+2]
      trigram = t[i] + ' ' + t[i+1] + ' ' + t[i+2]
      if not trigram in self.tri_dict and not (t[i] == '</s>' or t[i+1] == '</s>'):
        self.tri_dict[trigram] = 1
      elif (t[i] == '</s>' or t[i+1] == '</s>'):
        continue
      else:
        self.tri_dict[trigram] = self.tri_dict[trigram] + 1

    self.tri_dict = sorted(self.tri_dict.items(), key = lambda a: -a[1])
    return self.tri_dict


  def read_into_dicts(self, line_of_input):
    ilist = re.split('\s+', line_of_input.strip())
    if len(ilist) == 2:
      self.uni_dict[ilist[1]] = ilist[0]
    elif len(ilist) == 3:
      key = ' '.join(ilist[1:])
      self.bi_dict[key] = ilist[0]    
    elif len(ilist) = 4:
      key = ' '.join(ilist[1:])
      self.tri_dict[key] = ilist[0]    




  def count_types_tokens(self, dictionary):
### count how many types and how many tokens
    types = len(dictionary)
#    print types
    tokens = sum([i for i in dictionary.values()])
 #   print tokens
    return (types, tokens)
 

  def calc_uni_prob(self, dictionary):
### calculate probability and logprob and return it all as a list together with the count and the n-gram
    ARPA = []
    for key in dictionary:
      prob = dictionary[key]/self.count_types_tokens(dictionary)[1]
      logprob = math.log10(prob)     
#      logprob = math.log(dictionary[key]) - math.log(self.count_types_tokens(dictionary)[1])
      ARPA.append([dictionary[key], prob, logprob, key])
      print ARPA
    return ARPA


