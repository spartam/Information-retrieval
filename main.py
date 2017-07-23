import argparse, os, shutil

from btree  import btreeInstance, btreeReverseInstance
from config import config
from WordCache import WordCacheInstance
from queryloop import queryloop
from FileController import FileController

parser = argparse.ArgumentParser(description='Kwinten Pardon information retrieval project')

parser.add_argument('query', nargs='?', help='Query or path to either the file or directory you wish to add')

parser.add_argument('-a', '--add', action='store_true', help='add file')
parser.add_argument('-r', action='store_true', help='set flag to recursively add from directory')
parser.add_argument('-c', '--clean', action='store_true', help='removes all existing look up files')
parser.add_argument('-s', '--stemming', action='store_true', help='Set this flag if words need to be stemmed', default=False)
parser.add_argument('-q', '--queryloop', action='store_true', help='Start the queryloop')

args = parser.parse_args()

if args.clean:
	print('clean')
	try:
		shutil.rmtree(config['lookup'])
		shutil.rmtree(config['stemming'])
	except:
		pass

if args.stemming:
	WordCacheInstance.directory = 'stemming'
	btreeInstance.directory = 'stemming'
	btreeReverseInstance.directory = 'stemming'


if args.add and args.r:
	if args.query:
		FC = FileController(stemming=args.stemming)
		FC.recursiveAdd(args.query)
		FC.save()
	else:
		print('No path given. A path is required')
elif args.add:
	if args.query:
		FC = FileController(stemming=args.stemming)
		name = os.path.split(args.query)[1]
		FC.add(name, args.query)
		FC.save()
	else:
		print('No path given. A path is required')
	
if args.queryloop:
	queryloop(args.stemming)


# print(args.accumulate(args.integers))