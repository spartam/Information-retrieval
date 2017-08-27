from Word import Word
from btree import btreeInstance, btreeReverseInstance
import numpy as np
import heapq, itertools
from stemming.porter2 import stem
from PyDictionary import PyDictionary
from scipy import spatial

def near(w1, w2, proximity, directory='lookup'):
	w1 = Word(w1, directory)
	w2 = Word(w2, directory)

	if len(w1.occurences) == 0 or len(w2.occurences) == 0:
		return {}

	i = 0
	j = 0

	documents = {}

	while i < len(w1.occurences) and j < len(w2.occurences):
		if w1.occurences[i][0] == w2.occurences[j][0]:
			k = 0
			l = 0
			locations1 = w1.occurences[i][1]
			locations2 = w2.occurences[j][1]
			while k < len(locations1) and l < len(locations2):
				if abs(locations1[k] - locations2[l]) < proximity:
					if w1.occurences[i][0] in documents.keys():
						documents[w1.occurences[i][0]].append((locations1[k], locations2[l]))
					else:
						documents[w1.occurences[i][0]] = [(locations1[k], locations2[l])]
				if (locations1[k] < locations2[l]):
					k += 1
				else:
					l += 1
			i += 1
		elif w1.occurences[i][0] < w2.occurences[j][0]:
			i += 1
		else:
			j += 1

	return documents

def grouped_near(*words, proximity=None, directory='lookup'):
	words = list(words)
	proximity = proximity if proximity is not None else len(words)

	if (len(words) == 1):
		if '*' in words[0]:
			words = word_with_star(words[0])
			if len(words) == 0:
				return set()
		documents = set()
		if directory == 'stemming':
			words = [stem(w) for w in words]
		for W in [Word(w, directory) for w in words]:
			documents = documents.union(W.documents())
		return documents
	else:
		expansions = [word_with_star(w) for w in words if '*' in w]
		remaining  = [w for w in words if '*' not in w]
		if len(expansions) > 0:
			documents  = set()
			for combination in itertools.product(*expansions):
				words = list(combination) + remaining
				documents = documents.union(grouped_near(*words, proximity=proximity, directory=directory))

			return documents
		else:
			if directory == 'stemming':
				words = [stem(w) for w in words]
			w1 = words.pop(0)
			w2 = words.pop(0)

			solutions = near(w1, w2, proximity, directory=directory)

			for W in [Word(w, directory) for w in words]:
				pop = []
				for document in solutions.keys():
					occurences = W.search(document)
					if not(occurences):
						pop.append(document)
						continue
					else:
						occurences = occurences[1]
						matches = solutions[document]
						new = []
						for indx in occurences:
							for match in matches:
								if abs(max(match) - indx) < proximity and abs(min(match) - indx) < proximity:
									new.append(tuple(list(match)+ [indx]))
						if len(new) == 0:
							pop.append(document)
						else:
							solutions[document] = new


				for p in pop:
					solutions.pop(p)

		return set(solutions.keys())


def word_with_star(word):
	fixes = word.split('*')

	words = set()
	if len(fixes[0]) > 0 and len(fixes[1]) > 0:
		words = star(prefix=fixes[0], suffix=fixes[1])
	elif len(fixes[0]) > 0:
		words = star(prefix=fixes[0])
	else:
		words = star(suffix=fixes[1])

	return words


def star(prefix=None, suffix=None):
	if prefix is None and suffix is None:
		return set()
	elif prefix is not None and suffix is None:
		btreeInstance.load(prefix[0])
		return btreeInstance.prefixed(prefix)
	elif prefix is None and suffix is not None:
		btreeReverseInstance.load(suffix[::-1][0])
		return set(map(lambda x : x[::-1], btreeReverseInstance.prefixed(suffix[::-1])))
	else:
		btreeInstance.load(prefix[0])
		btreeReverseInstance.load(suffix[0][::-1])
		return btreeInstance.prefixed(prefix).intersection(set(map(lambda x : x[::-1], btreeReverseInstance.prefixed(suffix[::-1]))))


def ranked(*words, directory='lookup', func=lambda *x: 1):
	if directory == 'stemming':
		words = list(map(lambda x : stem(x), words))

	query = []
	processed = []
	for w in words:
		if w in processed:
			continue
		query.append(words.count(w))
		processed.append(w)

	query = np.array(list(map(lambda x : x / sum(query), query)))

	documents = set()
	# query = np.array([1/len(words) for i in range(len(words))])
	heap = []

	Words = []
	DFt = []
	for word in processed:
		WordInstance = Word(word, directory)
		Words.append(WordInstance)
		documents = documents.union(WordInstance.documents())
		DFt.append(len(WordInstance.documents()))

	N = len(documents)
	iDFt = list(map(lambda X : np.log10(N/X), DFt))

	for document in documents:
		vector = []
		for WordInstance in Words:
			## calculate the TF(t,d)
			count = WordInstance.count(document)
			if count > 0:
				vector.append(1 + np.log10(count))
			else:
				vector.append(0)

		## tf-idf weighting
		for i in range(len(iDFt)):
			vector[i] = vector[i] * iDFt[i]
		
		vector = np.array(vector)

		score = func(query, vector)

		heapq.heappush(heap, (score, document))

	return heap
	

def euclidean(v1, v2):
	return 1 - np.linalg.norm(v1-v2)

def cosine(v1, v2):
	return 1 - spatial.distance.cosine(v1, v2)

def synonyms(word):
	dictionary=PyDictionary()
	return dictionary.synonym(word)

# print(grouped_near("financial", "crisis", proximity=9, directory='stemming'))
# print(near("gaming", "art", proximity=9))
# print(grouped_near("gaming", "art", proximity=9))
# print(grouped_near("financial", "crisis"))

# print(word_with_star('lov*e'))

# print(grouped_near('lov*e', 'aff*', 'nation', proximity=100))
# print(grouped_near('lovable'))
# print(star(prefix="te", suffix="t"))
# res = ranked('test', 'paper', 'print', 'biography', 'print', '0')
# res2 = ranked('test', 'paper', 'print', 'biography', 'print', '0', func=cosine)
# print([x[1] for x in heapq.nlargest(5, res)], '\t', [x[1] for x in heapq.nlargest(5, res2)])
# res = ranked('test', 'paper', 'print', 'biography', '0')
# res2 = ranked('test', 'paper', 'print', 'biography', '0', func=cosine)
# print([x[1] for x in heapq.nlargest(5, res)], '\t', [x[1] for x in heapq.nlargest(5, res2)])