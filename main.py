import basic_programs
import input_management
import interface
import extras
from inspect import getmembers, isfunction

functions = getmembers(basic_programs, isfunction) + getmembers(extras, isfunction)

def main():
	loop()

def loop():
	im = input_management.input_manager(functions)
	while(True):
		stdin = input("GOATS ")
		t = im.parse(stdin)
		break

# Set up file thing??????
# sarah

def cd(args, flags):
	pass

def pwd(args, flags):
	pass

def help(args, flags):
	pass

def exit(args, flags):
	pass


if __name__ == '__main__':
	main()