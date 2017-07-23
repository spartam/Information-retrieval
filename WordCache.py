import random, datetime

from multiprocessing import Pool

from Word import Word
from btree import btreeInstance, btreeReverseInstance

class WordCache:
	
	def __init__(self, directory='lookup'):
		self.cache = {}
		self.directory = directory

	def add(self, word, documentID, occurences):
		if word in self.cache.keys():
			self.cache[word].add(documentID, occurences)
		else:
			wordInstance = Word(word, self.directory)
			wordInstance.add(documentID,occurences)
			self.cache[word] = wordInstance

	def save(self):
		keys = list(self.cache.keys())
		length = len(keys)
		count = 0

		interval = 120
		last_print = datetime.datetime.now().timestamp()
		print('%s/%s - %s' % (count, length, datetime.datetime.now()))
		for word in keys:
			count += 1
			self.cache.pop(word).save()
			btreeInstance.add(word)
			btreeReverseInstance.add(word[::-1])

			if last_print + interval < datetime.datetime.now().timestamp():
				print('%s/%s - %s' % (count, length, datetime.datetime.now()))
				last_print = datetime.datetime.now().timestamp()

		btreeInstance.save()
		btreeReverseInstance.save()

WordCacheInstance = WordCache()