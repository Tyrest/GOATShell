
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


def help(args, flags): 
	everything_dictionary = {"cd": "takes the user to a specified directory",
							"pwd": "prints the working directory", 
							"help": "displays a list of commands and flags and what each does", 
							"exit": "exits the terminal", 
							"ls": "gives the user a list of everything within the directory", 
							"echo": "repeats user input", 
							"jobs": "lists all active jobs", 
							"bg": "move jobs to the background", 
							"fg": "move jobs to the foreground", 

							"SpONgeBoBtEXt": "randomly capitalizes letters in user input",
							"meme": "generates a random meme", 
							"mege": "makes a meme using user input", 
							"djoosh": "makes an array for favorited songs", 
							"autocomplete": "returns the closest named command"}


	if args:
		for arg in args:
			if arg in everything_dictionary: 
				print(arg + " " + everything_dictionary[arg])
	else:
		print(everything_dictionary)


djoosh([], [])

