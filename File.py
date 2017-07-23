import lxml.html, os, string
from lxml.html.clean import Cleaner
from config import config

from WordCache import WordCacheInstance

from stemming.porter2 import stem

cleaner = Cleaner()
cleaner.javascript = True # This is True because we want to activate the javascript filter
cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter


class File:

	def __init__ (self, DocumentID, path, stemming=False):

		wordDict = {}

		# try:
		text = open(path, 'r', encoding='utf-8').read().encode('utf-8').decode('ascii', 'ignore')
		text = cleaner.clean_html(text)
		text = lxml.html.fromstring(text).text_content().lower()#.split('\n')
		for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '.', '!', '(', ')', '[', ']', ',', '…', '®', '¦', '™', '{', '}', '_']:
			text = text.replace(c, ' ')
		text = text.split("\n")
		# except:
		# 	self.status = False
		# 	return

		index = 0
		for line in text:
			for word in line.split(' '):
				word = word.strip()
				if len(word) < 1:
					continue
				if stemming:
					word=stem(word)
				if word in wordDict.keys():
					wordDict[word].append(index)
				else:
					wordDict[word] = [index]
				index += 1

		for word in wordDict.keys():
			WordCacheInstance.add(word, DocumentID, wordDict[word])

		self.status = True
