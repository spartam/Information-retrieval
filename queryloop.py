import search
import QueryProcessing
import btree
from FileController import FileController

def queryloop(directory='lookup'):
	FC  = FileController()
	FCs = FileController(stemming=True)
	stemming = False

	looping = True
	while looping:
		user_input = input("Search query:\t")
		if user_input == "exit":
			looping = False
		else:
			documents = QueryProcessing.process(user_input)
			for docID in documents:
				doc = FCs.get(docID) if stemming else FC.get(docID)
				print(doc[0], doc[1])
			print(len(documents), 'results found')

def switch(store_type):
	if store_type == 'stemming' or store_type == 'lookup':
		btreeInstance.switch(store_type)
		btreeReverseInstance.switch(store_type)
