#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2015/06/26

@author: ryosuke
'''

from itertools import chain
import nltk
import MeCab
import math
from urllib2 import HTTPError
import urllib2
CharEncoding = 'utf-8'
mecab = MeCab.Tagger ("-Ochasen")

def tf(words, doc):
  tf_values=[doc.count(word) for word in words]
  return list(map(lambda x: x*1.0/sum(tf_values),tf_values))

def idf(words, docs):
  return [math.log10(len(docs)*1.0/sum([bool(word in doc) for doc in docs])) for word in words]

def tf_idf(words, docs):
  """対象の文書と全文の形態素解析した単語リストを指定すると対象の文書のTF-IDFを返す"""
  #words=words.encode(CharEncoding) if isinstance(words,unicode) else words
  #docs=docs.encode(CharEncoding) if isinstance(docs,unicode) else docs
  return [[_tf*_idf for _tf,_idf in zip(tf(words,doc),idf(words,docs))] for doc in docs]

def doc2words(text):
  """テキストを与えると名詞のリストにして返す"""
  text=text.encode(CharEncoding) if isinstance(text,unicode) else text

  keywords=[] #結果を格納する配列
  node=mecab.parseToNode(text) #Mecabによる解析を実行
  while node:
     surface=node.surface.decode(CharEncoding)
     meta=node.feature.split(",")  #featureをカンマ区切りで取得
     if meta[0]==("名詞"): #featureの品詞が名詞なら配列に単語を追加
        keywords.append(node.surface)
     node=node.next
  return keywords


words = ["リンゴ", "ゴリラ", "ラッパ"]
docs = ["リンゴ、リンゴ", "リンゴとゴリラ", "ゴリラとラッパ"]
print tf_idf(words, docs)
