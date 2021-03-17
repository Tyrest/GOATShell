import basic_programs
import input_management
import interface
import extras
from inspect import getmembers, isfunction
import os
import sys
import subprocess
import tempfile
import signal
import io
import glob

def display_exception(e):
	to_print = type(e).__name__
	if len(e.args) != 0:
		to_print += ": " + str(e.args[0])
	print(to_print)

# Signal handler for while a process is running
def signal_handler(sig, frame):
	raise Exception(signal.strsignal(sig))

def signal_none(sig, frame):
	print("\n")
	raise Exception

# Exit program
def exit(args):
	for p, status in basic_programs.processes.values():
		p.kill()
	sys.exit(0)

# Main shell loop
def main():
	# get functions from files
	functions = dict(getmembers(basic_programs, isfunction) + getmembers(extras, isfunction))
	functions.update([('exit', exit)]) 

	im = input_management.input_manager(functions)
	while(True):
		basic_programs.check_processes()
		
		signal.signal(signal.SIGINT, signal_none)
		signal.signal(signal.SIGTSTP, signal_none)
		try:
			stdin = input("GOATS: ")
		except Exception:
			continue
		if len(stdin.strip()) == 0:
			continue
		try:
			output = exec_command(stdin, im)
			if output is not None: 
				print(output.decode('utf-8').strip())
		except Exception as e:
			display_exception(e)
		
# Executes the command passed in from stdin
def exec_command(stdin, im):
	builtins = im.functions
	builtin_names = list(builtins.keys())
	# handle case of subcommands
	while '$(' in stdin:
		stdin = subcommand_handler(stdin, im)
	bg, file_in, file_out, t = im.parse(stdin)

	pipe_input = None
	for fncall in t:
		fn_name = fncall[0]; fn_args = fncall[1]
		
		if pipe_input is not None:
			fn_args.append(pipe_input.name)

		if fn_name not in builtin_names:
			nonflag_args = [i for i in fn_args if "-" != i[0]]
			if len(nonflag_args) > 0 and fn_name != 'echo':
				glob_arg = nonflag_args[0]
				glob_arg_i = fn_args.index(glob_arg)
				output = b''
				if len(glob.glob(glob_arg)) == 0:
					raise FileNotFoundError
				for path in glob.glob(glob_arg):
					tokens = [fn_name] + fn_args[:glob_arg_i] + [path] + fn_args[glob_arg_i+1:]
					out, err = exec_process(tokens, bg, file_in, file_out)
					if len(err.strip()) != 0:
						raise Exception(err)
					else:
						output += out
				
			else:
				output, error = exec_process([fn_name] + fn_args, bg, file_in, file_out)
				if len(error.strip()) != 0:
					raise Exception(error)
			if pipe_input is not None:
				pipe_input.close()
		else:
			output = builtins[fncall[0]](fn_args)
			output = output.encode('utf-8')
		if output is not None:
			#print(output)
			# Pass temporary file to next function call
			pipe_input = tempfile.NamedTemporaryFile()
			pipe_input.write(output); pipe_input.seek(0)
	return output

# Executes non-built-in from tokens
# bg is True if the process should run in the background, False otherwise
def exec_process(tokens, bg, file_in, file_out):
	try:
		# Set signal handlers to interrupt or stop the current process
		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGTSTP, signal_handler)

		p = subprocess.Popen(tokens, shell=False, stdin=file_in, stdout=file_out, stderr=subprocess.PIPE)

		if bg == False:
			out, err = p.communicate(timeout=10**3)
			return out, err.decode('utf-8')
		else:
			basic_programs.processes[p.pid] = [p, "running"]
			return None, None

	except subprocess.TimeoutExpired:
		print("Timeout expired. Killing process...")
		p.kill()
		out, err = p.communicate(timeout=10**3)
		return out, err

	except Exception as e:
		if e.args[0] == signal.strsignal(signal.SIGTSTP):
			p.send_signal(signal.SIGTSTP)
			basic_programs.processes[p.pid] = [p, "stopped"]
		elif e.args[0] == signal.strsignal(signal.SIGINT):
			p.send_signal(signal.SIGINT)
		display_exception(e)
		return None, e.__repr__()

# For command substitution
# Replaces deepest instance of $(command) with output from command
def subcommand_handler(stdin, im):
	# find deepest occurence of $, index = len(stdin) - 1 - (first index of $ in reversed stdin)
	index1 = len(stdin) - 1 - (stdin[::-1].index('($'))
	index2 = stdin.index(')', index1)
	c = stdin[index1 + 1 : index2]
	
	# execute command 
	output = exec_command(c, im)
	if output is None: 
		output = ''

	# replace $(command) with output
	return stdin.replace('$(' + c + ')', output.decode('utf-8').strip())

if __name__ == '__main__':
	main()