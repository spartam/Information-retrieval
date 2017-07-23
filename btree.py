import json
import os
from stemming.porter2 import stem

from config import config

class btree:

	def __init__(self, name, directory='lookup'):

		self.tree = {}
		self.name = name
		self.directory = directory

	def add(self, word):
		tree = self.tree
		for indx in range(len(word)):
			char = word[indx]
			if indx == len(word)-1:
				tree[char] = {} if not char in tree.keys() else tree[char]
				tree[char]['word'] = True
			elif char in tree.keys():
				tree = tree[char]
			else:
				newtree = {'word' : False}
				tree[char] = newtree
				tree = newtree


	def find(self, word):
		tree = self.tree
		for char in word:
			if not(char in tree.keys()):
				return False
			else:
				tree = tree[char]
		return tree

	def prefixed(self, prefix):
		subtree = self.find(prefix)

		solutions = set()

		if not(subtree):
			return solutions

		if subtree['word']:
			solutions.add(prefix)

		subtrees = [(prefix, subtree)]

		while len(subtrees) > 0:
			prefix, subtree = subtrees.pop()
			if subtree['word']:
				solutions.add(prefix)
			for k in subtree.keys():
				if k == 'word':
					continue
				else:
					subtrees.append((prefix + k, subtree[k]))


		return solutions

	def __str__(self):
		return json.dumps(self.tree)

	def save(self):
		path = os.path.join(config[self.directory], config['btree'])
		if not(os.path.exists(path)):
			os.makedirs(path)

		for root in self.tree.keys():
			file = os.path.join(path, '%s-%s.lkp' % (self.name, root))
			with open(file, 'w') as f:
				f.write(json.dumps(self.tree[root]))

	def load(self, root):
		path = os.path.join(config[self.directory], config['btree'])
		file = os.path.join(path, '%s-%s.lkp' % (self.name, root))
		with open(file, 'r') as f:
			self.tree[root] = json.loads(f.read())


	def foreach(self, func):
		roots = []
		for f in os.listdir(os.path.join(config[self.directory], config['btree'])):
			if self.name in f:
				roots.append(f[len(self.name)+1:len(f) - 4])

		for root in roots:
			self.load(root)
			for el in self.prefixed(root):
				func(el)

	def switch(self, directory):
		self.directory = directory
		self.tree = {}


btreeInstance = btree('btree.lkp')
btreeReverseInstance = btree('btreereversed.lkp')

# btreeInstance.load()
# btreeReverseInstance.load()
dct = {}
def func(x):
	if stem(x) in dct.keys():
		dct[stem(x)].append(x)
	else:
		dct[stem(x)] = [x]

if __name__ == '__main__':
	btreeInstance.foreach(func)

	for key in dct.keys():
		if len(dct[key]) >= 5:
			print(key, dct[key])