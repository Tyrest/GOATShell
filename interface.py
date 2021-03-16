import math
names = ['ls', 'echo', 'help', 'cd', 'pwd', 'jobs', 'fg', 'bg', 'exit', 'SpONgeBoBtEXt', 'djooshAdd', 'djooshRemove']

def autocomplete(args, flags):
	input = args[0]
	#1) Remove all non-letter characters from strings
	keepLetters = lambda x: "".join([c for c in x if c.isalpha()])
	newNames = list(map(lambda x: keepLetters(x).lower(), names))
	a = keepLetters(input).lower()
	#dict containing rough (row,col) position of each letter on the keyboard
	keyboard = {'q': (0,0), 'w':(0,1), 'e':(0,2), 'r':(0,3), 't':(0,4), 'y':(0,5), 'u':(0,6), 'i':(0,7), 'o':(0,8), 'p':(0,9), 'a':(1.2,0.2), 's':(1.2,1.2), 'd':(1.2,2,2), 'f':(1.2,3.2), 'g':(1.2,4.2), 'h':(1.2,5.2), 'j':(1.2,6.2), 'k':(1.2,7.2), 'l':(1.2,8.2), 'z':(2.4,0.5), 'x':(2.4,1.5), 'c':(2.4,2.5), 'v':(2.4,3.5), 'b':(2.4,4.5), 'n':(2.4,5.5), 'm':(2.4,6.5)} 
	#2) Create list newStrings that changes the letters of each function name to closest character of input
	newStrings = []
	for n in newNames:
		newString = ""
		for c in n:
			#uses euclidean distance to calculate letter proximity
			ed = lambda x: math.sqrt((keyboard[c][0] - keyboard[x][0])**2 + (keyboard[c][1] - keyboard[x][1])**2)
			newString += min(a, key=ed)
		newStrings.append(newString)
	#3) Returns item in newStrings closest to corresponding function
	m = None
	for word1,word2,word3 in zip(newNames, newStrings, names):
		dis = sum((math.sqrt((keyboard[a][0] - keyboard[b][0])**2 + (keyboard[a][1] - keyboard[b][1])**2) for a, b in zip(word1, word2)))
		if not m or dis/len(word1)<m[0]:
			m = (dis/len(word1), word3)
	return m[1]