import os
import signal
import subprocess
import time

processes = {}

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
	return to_return

# Return none if arguments or flags are not valid
def bg(args, flags):
	pid = int(args[0])
	processes[pid][0].send_signal(signal.SIGCONT)
	processes[pid][1] = "running"

# Return none if arguments or flags are not valid
def fg(args, flags):
	pid = int(args[0])
	processes[pid][0].send_signal(signal.SIGCONT)
	processes[pid][1] = "running"
	out, err = processes[pid][0].communicate(timeout=1000)
	processes[pid][1] = "done"

def test(args, flags):
	time.sleep(int(args[0]))