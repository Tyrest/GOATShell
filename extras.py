# Return none if arguments or flags are not valid
# george
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

# Creates an Array of favorite songs where you can add or remove songs
song_list = []

def djooshAdd(args):
	if args not in song_list: 
		song_list.append(args)
		return "Song successfully added"
	else: 
		return "Song already added"

def djooshRemove(args):
	if args in song_list: 
		song_list.remove(args)
		return "Song successfully removed"
	else: 
		return "Song does not exist"
