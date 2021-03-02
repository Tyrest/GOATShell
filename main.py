import basic_programs
import input_management
import interface
import extras
from inspect import getmembers, isfunction
import os
import sys

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
		except FileNotFoundError:
			raise FileNotFoundError('No such file or directory')
		except:
			raise Exception('Bad input, try again')

# Returns path of current working directory
def pwd(args, flags):
	print(os.getcwd())

def help(args, flags):
	pass

def exit(args, flags):
	sys.exit(0)


functions = dict(getmembers(basic_programs, isfunction) + getmembers(extras, isfunction))
functions.update([('pwd', pwd), ('cd', cd), ('exit', exit)])

def main():
	loop()

def loop():
	im = input_management.input_manager(functions)
	while(True):
		stdin = input("GOATShell: ")
		t = im.parse(stdin)
		for fncall in t:
			fn_name = fncall[0]; fn_args = fncall[1]; fn_flags = fncall[2]
			try:
				output = functions[fncall[0]](fn_args, fn_flags)
			except KeyError:
				print("Error: no such method")
			except Exception as e:
				print(type(e).__name__ + ": " + str(e.args[0]))


if __name__ == '__main__':
	main()