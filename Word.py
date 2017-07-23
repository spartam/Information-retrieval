import os, bisect

from config import config

class Word:

	def __init__(self, word, directoryKey):
		self.word = word
		self.directory = os.path.join(config[directoryKey], word[0])
		self.filepath  = os.path.join(self.directory, word+'.lkp')
		self.occurences = []


		if not(os.path.exists(self.directory)):
			os.makedirs(self.directory)

		if os.path.exists(self.filepath):
			self.load()


	def save(self):
		try:
			with open(self.filepath, 'w') as f:
				for occurence in self.occurences:
					f.write("%s: %s\n" % tuple(occurence))
		except:
			print(self.filepath)



	def load(self):
		with open(self.filepath, "r") as f:
			for line in f:

				occurence = line.strip().split(":")
				occurence[0] = int(occurence[0])
				occurence[1] = list(map(int, occurence[1].replace('[', '').replace(']', '').split(',')))
				
				bisect.insort_left(self.occurences, occurence)

	def add(self, documentID, occurences):
		value = self.search(documentID)

		if not(value):
			bisect.insort_left(self.occurences, [documentID, occurences])
		else:
			pass

	def documents(self):
		s = set()
		for documentID, occurences in self.occurences:
			s.add(documentID)
		return s

	def count(self, documentID):
		occurences = self.search(documentID)
		return len(occurences[1]) if occurences else 0

	def search(self, documentID, start=0, end=None):

		if len(self.occurences) == 0:
			return False

		if end is None:
			end = len(self.occurences) - 1

		while start != end:

			if end - start == 1:
				if self.occurences[start][0] == documentID:
					return self.occurences[start]
				elif self.occurences[end][0] == documentID:
					return self.occurences[end]
				else:
					return False
			else:
				middle = start + round((end - start) / 2)
				value = self.occurences[middle]

				if value[0] == documentID:
					return value
				elif value[0] > documentID:
					end = middle
				else:
					start = middle
		print(self.occurence[start])
		if self.occurences[start] == documentID:
			return self.occurences[start]
		else:
			return False




if __name__ == '__main__':
	w = Word("test", 'lookup')
	for d in w.documents():
		print('%s:\t%s' % (d, w.count(d)))
