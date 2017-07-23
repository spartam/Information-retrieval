import search
import itertools, re

def process(query, directory='lookup'):
	query = expand(query) if expandable(query) else query
	query = query.lower()

	solutions = None
	if (query.count('(') != query.count(')')):
		raise Exception('unbalanced brackets')
	if query.count('(') == 0 or (query.count('(') == 1 and query.count(')') == 1 and query[0] == '(' and query[-1] == ')'):
		query = query.strip('(').strip(')')
		if query.count('&') != 0 or query.count('|') != 0:
			raise Exception('&& and || operations must be surrounded by expressions in brackets')
		args = [a.strip() for a in query.split(' ')]
		if not( '\\' in query):
			solutions = search.grouped_near(*args, directory=directory)
		elif args[len(args) - 1][0] == '\\':
			proximity = int(args[-1].strip('\\'))
			solutions = search.grouped_near(*args[0:len(args)-1], proximity=proximity, directory=directory)
		else:
			words  = [w for w in [args[i] for i in range(0, len(args), 2)]]
			counts = [w for w in [args[i] for i in range(1, len(args), 2)]]

			if all(['\\' in x for x in counts]):
				counts = list(map(lambda x : int(x.strip('\\')), counts))
				proximity = 0
				solutions = None
				for i in range(len(counts)):
					if solutions is None:
						solutions = search.grouped_near(words[i], words[i+1], directory=directory)
					else:
						solutions = solutions.union(search.grouped_near(words[i], words[i+1], directory=directory))
				
			else:
				raise Exception('Wrongly formatted query')

	elif query[0] != '(':
		raise Exception('did not start with bracket')

	else:
		indx = 0
		bracket_count = 0
		for i in range(len(query)):
			char = query[i]
			indx += 1
			if char == '(':
				bracket_count += 1
			elif char == ')':
				bracket_count -= 1

			if bracket_count == 0:
				break

		head = query[1:indx-1].strip()
		tail = query[indx:].strip()

		operator = tail[:tail.find(' ')].strip()
		tail = tail[tail.find(' '):].strip()

		if (not('&&' in tail) and not('||' in tail)):
			tail = tail.strip('(').strip(')')

		if operator == '&&' or operator == '||':
			head_result = process(head)
			tail_result = process(tail)

			if operator == '&&':
				return head_result.intersection(tail_result)
			else:
				return head_result.union(tail_result)
		elif len(operator.strip()) == 0:
			return process(head)
		else:
			raise Exception('Unknown operator: %s' % (operator))




	return solutions


def expandable(strng):
	return len(re.findall('E\([a-z]*\)', strng)) > 0


def expand(strng):
	m = re.findall('E\([a-z]*\)', strng)
	for keyword in m:
		strng = strng.replace(keyword, '%s')
	sets = [search.synonyms(keyword[2:len(keyword)-1]) + [keyword[2:len(keyword)-1]] for keyword in m]
	result = ''
	for combination in itertools.product(*sets):
		result += ' || (' + strng % combination + ')'

	return result.strip(' ||')


if __name__ == '__main__':
	# pass
	# print(process('CURRENCY'))
	# print()
	# print(process('CURRENCY', directory='stemming'))
	# expand('(failure) && (success)')
	# print(expand('(failure) && (success)'))
	print(process('(E(failure)) && (success)'))
	# print(process('((failure) && (success))'))
	# print(expand('E(test) && E(repetition)'))
	# print(process('financial \\9 crisis \\9 asian'))
	# print()
	# print(process('(financial \\9 crisis) && (crisis \\9 asian)'))
	# print()
	# print(process('financial crisis asian \\9'))
	# print()
	# print('----')
	# print()
	# print(process('financial \\9 crisis \\9 asian', directory='stemming'))
	# print()
	# print(process('(financial \\9 crisis) && (crisis \\9 asian)', directory='stemming'))
	# print()
	# print(process('financial crisis asian \\9', directory='stemming'))
	# print()
	# print(process('''(financial \\2 crisis \\7 asian) && (currency)'''))
	# print()
	# print(process('''(financial \\2 crisis \\7 asian) || (currency)'''))
	# print(type(set()) is set)