import os
import signal
import subprocess
import time

processes = {}

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

def help(args):
	pass

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
	p, status = processes.pop(args[0])
	p.send_signal(signal.SIGCONT)
	out, err = p.communicate(timeout=1000)

# Returns input	
def echo(args, flags):
	return " ".join(args + flags)

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
				print("Process was terminated improperly")
			val[0].kill()
		else:
			new_dict[pid] = val
	processes = new_dict
			
