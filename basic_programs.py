import os
import signal
import subprocess
import time

processes = {}

# Signal handler for while a process is running
# Handler set for CTRL-C (SIGINT) and CTRL-Z (SIGTSTP)
# Raises exception with description of signal as message
# Exception is caught in exec_process to handle cases
def signal_handler(sig, frame):
	raise Exception(signal.strsignal(sig))


# Takes in complete path or end of path as argument
# flags: none
def cd(args):
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
def pwd(args):
	print(os.getcwd())

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
							"djoosh": "makes an array for favorited songs", 
							"autocomplete": "returns the closest named command"}


	if args:
		for arg in args:
			if arg in everything_dictionary: 
				print(arg + " " + everything_dictionary[arg])
	else:
		print(everything_dictionary)

# Return none if arguments or flags are not valid
def jobs(args):
	global processes
	to_return = ""
	new_dict = {}
	for pid, val in processes.items():
		if val[0].poll() != None:
			val[1] = "done"
		to_return += "{}\t{}\t{}\n".format(pid, val[1], " ".join(val[0].args))
		if val[1] != "done":
			new_dict[pid] = val
		else:
			val[0].kill()
	processes = new_dict
	return to_return.strip()

# Return none if arguments or flags are not valid
def bg(args):
	pid = int(args[0])
	processes[pid][0].send_signal(signal.SIGCONT)
	processes[pid][1] = "running"

# Return none if arguments or flags are not valid
def fg(args):
	global processes
	try:
		p, status = processes.pop(int(args[0]))
		p.send_signal(signal.SIGCONT)
		
		# Set signal handlers to interrupt or stop the current process
		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGTSTP, signal_handler)

		out, err = p.communicate()
		return out

	except Exception as e:
		if e.args[0] == signal.strsignal(signal.SIGTSTP):
			p.send_signal(signal.SIGTSTP)
			processes[p.pid] = [p, "stopped"]
		elif e.args[0] == signal.strsignal(signal.SIGINT):
			p.send_signal(signal.SIGINT)
		return None

# Checks processes in list, prints out status/process if jobs are done and removes the process from the jobs list
# If any processes terminated improperly, print out the signal 
def check_processes():
	global processes
	new_dict = {}
	for pid, val in processes.items():
		if val[0].poll() != None:
			val[1] = "done"
			print("{}\t{}\t{}\n".format(pid, val[1], " ".join(val[0].args)))
			status = val[0].returncode
			if status:
				print(signal.strsignal(-status))
				print("Process was terminated improperly")
			val[0].kill()
		else:
			new_dict[pid] = val
	processes = new_dict
			
