# Takes in complete path or end of path as argument
# flags: none
def cd(args, flags):
	if args == ['..']:
		parent = os.path.dirname(os.getcwd())
		os.chdir(parent)
	elif args == ['~']:
		home = os.getenv("HOME")
		os.chdir(home)
	else:
		try:
			os.chdir(args[0])
		except TypeError:
			raise TypeError('Bad arguments, try again')
		except OSError:
			raise OSError("Invalid or inaccessible file names and paths")
		except FileNotFoundError:
			raise FileNotFoundError('No such file or directory')
		except:
			raise Exception('Bad input, try again')

# Returns path of current working directory
def pwd(args, flags):
	print(os.getcwd())

def help(args, flags):
	pass

# Return none if arguments or flags are not valid
def jobs(args, flags):
    pass

# Return none if arguments or flags are not valid
def bg(args, flags):
    pass

# Return none if arguments or flags are not valid
def fg(args, flags):
    pass