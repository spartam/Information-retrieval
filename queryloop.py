import os

import search
import QueryProcessing
import btree
from FileController import FileController

def queryloop(stemming, directory='lookup'):
	FC  = FileController()
	FCs = FileController(stemming=True)
	# stemming = False

	looping = True
	while looping:
		user_input = input("Enter search query:\t").strip()
		if user_input[:2] == '->':
			user_input = user_input[2:].strip()
			if user_input == "exit":
				looping = False
			elif user_input == "clear":
				os.system('cls')
			elif user_input == 'stemming':
				print('stemming: ', stemming)
			elif user_input[:8] == 'stemming':
				new_state = user_input[8:].strip().lower()
				if new_state == 'false':
					stemming = False
				elif new_state == 'true':
					stemming = True
				else:
					print('unknown stemming state: must be true or false')
				print('stemming: ', stemming)
			else:
				print('unknown command')

		else:
			try:
				directory = 'stemming' if stemming else 'lookup'
				print(user_input)
				documents = QueryProcessing.process(user_input, directory=directory)
			except Exception as e:
				print('An error occured \n', e)
				documents = set()
			for docID in documents:
				doc = FCs.get(docID) if stemming else FC.get(docID)
				doc = list(map( lambda x : x.encode('utf-8').decode('ascii', 'ignore'), doc))
				print(doc[0], doc[1])
			print(len(documents), 'results found')

		print('---\n')

def switch(store_type):
	if store_type == 'stemming' or store_type == 'lookup':
		btreeInstance.switch(store_type)
		btreeReverseInstance.switch(store_type)
