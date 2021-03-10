import random

def SpONgeBoBtEXt(args):

	#initialize spongetext variable
	spongetext = ""
	for char in input:
		
		#check if the character is in the alphabet
		if char.isalpha():
			random_num = random.random()
			
			#change the character to a capital letter
			if random_num > 0.5:
				spongetext += char.upper()
			
			#change the character to a lowercase letter
			else:
				spongetext += char.lower()
		
		#if the character is not in the alphabet, add it to the output without changing
		else:
			spongetext += char

	return spongetext

if Spongetext == true:
	text = SpONgeBoBtEXt(text)
print(text)
