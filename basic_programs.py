import os
import signal
import subprocess
import time

processes = []

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
	for p in processes:
		print("{}\t{}\t{}".format(p.pid, "running" if p.poll() is None else "done", " ".join(p.args)))
		if p.poll() != None:
			p.terminate()
	processes = list(filter(lambda x : x.poll() == None, processes))

# Return none if arguments or flags are not valid
def bg(args, flags):
	pid = int(args[0])
	p = next(iter([x for x in processes if x.pid == pid]))
	p.send_signal(signal.SIGCONT)

# Return none if arguments or flags are not valid
def fg(args, flags):
	pid = int(args[0])
	p = next(iter([x for x in processes if x.pid == pid]))
	p.send_signal(signal.SIGCONT)
	out, err = p.communicate(timeout=1000)

def test(args, flags):
	time.sleep(int(args[0]))