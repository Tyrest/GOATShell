#!/usr/bin/env python3
import unittest, main, input_management, interface, basic_programs, extras, random, string

class TestStringMethods(unittest.TestCase):

	def test_SpONgeBoBtEXt(self):
		s = ''.join(random.choice(string.printable) for i in range(random.randint(0,200)))
		self.assertEqual(extras.SpONgeBoBtEXt([s]).lower(), s.lower())

	'''def test_djoosh(self):
		song_list = []
		self.assertEqual(len(extras.song_list), 0)
		for i in range(0, 10):
			newSong = ''.join(random.choice(string.printable) for j in range(random.randint(0,100))) + str(i)
			song_list.append(newSong)
			self.assertEqual(extras.djooshAdd([newSong]), "Song successfully added")
		for i in range(0, 10):
			self.assertEqual(extras.djooshRemove([newSong[i]]), "Song successfully removed")'''

	def test_script(self):
		o = open("outputs.txt").read()
		g = open("goals.txt").read()
		o = ''.join(o.split())
		g = ''.join(g.split())
		print('\n======================================================================\nRESULT:\n' + o)
		print('\nINTENDED RESULT:\n' + g)
		self.assertEqual(o, g)

if __name__ == '__main__':
	unittest.main()