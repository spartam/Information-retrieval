import os, bisect, codecs
import datetime

from File import File
from config import config
from WordCache import WordCacheInstance
from btree import btreeInstance, btreeReverseInstance

class FileController:

	def __init__(self, stemming=False):
		self.filesList = []
		self.stemming = stemming
		self.storekey = 'stemming' if stemming else 'lookup'
		self.filesListPath = os.path.join(config[self.storekey], config['fileslist'])

		if os.path.exists(config[self.storekey]):
			self.load()
		else:
			os.mkdir(config[self.storekey])
			self.save()


	def add(self, fileName, filePath):
		F = File(len(self.filesList), filePath, stemming=self.stemming)
		if F.status:
			self.filesList.append((fileName, filePath))
			return F
		else:
			return False


	def recursiveAdd(self, path):
		paths = [path]
		interval = 20000
		increment = 20000
		files = []
		print(datetime.datetime.now())
		while len(paths) > 0:
			p = paths.pop()
			for f in os.listdir(p):
				path = os.path.join(p, f)
				if os.path.isfile(path) or path[len(path)-5:] == '.html':
						files.append(path)
				else:
					paths.append(path)
			if len(files) > interval:
				interval += increment
				print(datetime.datetime.now(), len(files))
		print(datetime.datetime.now(), len(files))

		interval = 120
		last_print = datetime.datetime.now().timestamp()

		count = 0
		for filePath in files:
			self.add(os.path.split(filePath)[1], filePath)
			count += 1
			if last_print + interval < datetime.datetime.now().timestamp():
				print("%s/%s \t %s" % (count, len(files), datetime.datetime.now()))
				last_print = datetime.datetime.now().timestamp()

		# self.save()


	def save(self):
		with codecs.open(self.filesListPath, 'w', 'utf-8') as fileslist:
			for file in self.filesList:
				fileslist.write('*.*'.join(file) + '\n')

		# btreeInstance.save()
		# btreeReverseInstance.save()
		WordCacheInstance.save()

	
	def load(self):
		self.filesList = []
		with codecs.open(self.filesListPath, 'r', 'utf-8') as fileslist:
			for line in fileslist:
				self.filesList.append(tuple(line.strip().split('*.*')))

	def get(self, n):
		return self.filesList[n]


if __name__ == '__main__':
		
	FC = FileController()
	print(FC.get(7103))

	# print(FC.get(683))
	# print(FC.get(707))
	# print(FC.get(17352))
	# print(FC.get(82121))

	# FC.add('test.html', 'test.html')

	# print(FC.filesList)

	# FC.save()
	# FC.load()

	# FC.recursiveAdd(os.path.join(os.getcwd(), "dataset"))
	# FC.save()