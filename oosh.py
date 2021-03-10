
import tempfile

def add(temp):
	val = input("Enter song to add: ")
	if val not in temp: 
		temp.writelines(val)
		temp.seek(0)
	else: 
		print("Already in the file")


def remove(temp):
	val = input("Enter song to remove: ")
	if val in temp: 
		#something
		temp.seek(0)
	else: 
		print("Not in the file")



# Basic Idea: Saves songs that you like in a file that you can add or remove
def djoosh(args, flags):
	print("Temporary File")

	temp = tempfile.TemporaryFile(mode='w+t')

	flag_dictionary = {"-a": add,
						"-r": remove}
	'''
	try:
		temp.writelines("Hello world!")
		temp.seek(0)

		print(temp.read())
	finally:
		temp.close()
	'''

	temp.close()


# Make a text file (help.txt) 
# Read from the file and print out the standard help
def help(args, flags): 
	everything_dictionary = {"cd": "takes the user to a specified directory",
							"pwd": "what the fuck does it do [flags]", 
							"help": "displays a list of commands and flags and what each does", 
							"exit": "what the fuck does it do [flags]", 
							"ls": "gives the user a list of everything within the directory [-d (?), -S (sorts files by size), -a (displays all files, including hidden ones), -s (displays number of bytes), -l (displays long format), -X (?)]", 
							"echo": "repeats user input", 
							"jobs": "what the fuck does it do [flags]", 
							"bg": "move jobs to the background", 
							"fg": "move jobs to the foreground", 

							"SpONgeBoBtEXt": "randomly capitalizes letters in user input",
							"meme": "generates a random meme [flags?]", 
							"mege": "makes a meme using user input [flags?]", 
							"djoosh": "saves favorited songs in a temporary file to be added or removed [-a (adds a song), -r (removes a song)]", 
							"autocomplete": "returns the closest named command"}





djoosh([], [])

