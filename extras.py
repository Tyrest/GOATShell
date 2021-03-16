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

# Return none if arguments or flags are not valid
# oosh
def add(song_list, val):
	if val not in song_list: 
		song_list.append(val)
		return "Song successfully added"
	else: 
		return "Song already added"


def remove(song_list, val):
	if val in song_list: 
		song_list.remove(val)
		return "Song successfully removed"
	else: 
		return "Song does not exist"


# Basic Idea: Saves songs that you like in a file that you can add or remove
def djoosh(args, flags):
	song_list = []

	flag_dictionary = {"-a": add,
						"-r": remove}

	return song_list
