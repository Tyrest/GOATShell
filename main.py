import basic_programs
import input_management
import interface
import extras
from inspect import getmembers, isfunction
import os, sys, subprocess, tempfile, signal, io, glob

# Display type and message of exception
def display_exception(e):
	to_print = type(e).__name__
	if len(e.args) != 0:
		to_print += ": " + str(e.args[0])
	print(to_print)

# Signal handler for while a process is running
# Handler set for CTRL-C (SIGINT) and CTRL-Z (SIGTSTP)
# Raises exception with description of signal as message
# Exception is caught in exec_process to handle cases
def signal_handler(sig, frame):
	raise Exception(signal.strsignal(sig))

# Signal handler while in main loop, when no process is running
# Handler set for CTRL-C (SIGINT) and CTRL-Z (SIGTSTP)
# Can't use SIG_IGN here because we have to acknowledge the signal and then return to prompt
# exception is caught in main loop; returns to prompt and does nothing else
def signal_none(sig, frame):
	print("\n")
	raise Exception

# Kill all processes and exit program
def exit(args):
	for p, status in basic_programs.processes.values():
		p.kill()
	sys.exit(0)

# Main shell loop
def main():
	# get builtins from files
	functions = dict(getmembers(basic_programs, isfunction) + getmembers(extras, isfunction) + getmembers(interface, isfunction))
	functions.update([('exit', exit)]) 

	im = input_management.input_manager(functions)
	while(True):
		# checks on jobs
		basic_programs.check_processes()
		
		# Set signal handlers to ignore signal and reset prompt
		signal.signal(signal.SIGINT, signal_none)
		signal.signal(signal.SIGTSTP, signal_none)
		try:
			stdin = input("GOATS: ")
		except Exception:
			continue
		
		# if the user just enters whitespace
		if len(stdin.strip()) == 0:
			continue
		
		# execute stdin, catch exceptions
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

	# handle command substitution
	while '$(' in stdin:
		stdin = subcommand_handler(stdin, im)
	bg, file_in, file_out, t = im.parse(stdin)

	# pipe_input is passed to next command 
	pipe_input = None
	for fncall in t:
		fn_name = fncall[0]; fn_args = fncall[1]
		
		# Don't pipe anything to echo
		if pipe_input is not None and fn_name != "echo":
			fn_args.append(pipe_input.name)

		if fn_name not in builtin_names:
			exec_normal = True				# execute without globbing
			nonflag_args = [i for i in fn_args if "-" != i[0]]

			# don't want to glob anything echoed
			if len(nonflag_args) > 0 and fn_name != 'echo':
				glob_arg = nonflag_args[0]
				glob_arg_i = fn_args.index(glob_arg)
				output = b''

				# if glob_arg is not a file path
				if len(glob.glob(glob_arg)) != 0:
					exec_normal = False
				
				for path in glob.glob(glob_arg):
					tokens = [fn_name] + fn_args[:glob_arg_i] + [path] + fn_args[glob_arg_i+1:]
					out, err = exec_process(tokens, bg, file_in, file_out)
					if len(err.decode('utf-8').strip()) != 0:
						raise Exception(err.decode('utf-8'))
					else:
						output += out
			
			if exec_normal == True:
				output, error = exec_process([fn_name] + fn_args, bg, file_in, file_out)
				if len(error.decode('utf-8').strip()) != 0:
					raise Exception(error.decode('utf-8'))
			if pipe_input is not None:
				pipe_input.close()
		else:
			# run builtin
			output = builtins[fncall[0]](fn_args)
			if output is not None: 
				output = output.encode('utf-8')
		
		if output is not None:
			# Pass temporary file to next function call
			pipe_input = tempfile.NamedTemporaryFile()
			pipe_input.write(output); pipe_input.seek(0)
	return output

# Executes non-built-in from tokens
# Returns output, error as bytes
# bg is True if the process should run in the background, False otherwise
def exec_process(tokens, bg, file_in, file_out):
	try:
		# Set signal handlers to interrupt or stop the current process
		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGTSTP, signal_handler)

		p = subprocess.Popen(tokens, shell=False, start_new_session=True, stdin=file_in, stdout=file_out, stderr=subprocess.PIPE)

		if bg == False:
			out, err = p.communicate()
			return out, err
		else:
			# Add process to jobs list if running in background
			basic_programs.processes[p.pid] = [p, "running"]
			return None, b''

	except Exception as e:
		# Detect control z and control c events
		if e.args[0] == signal.strsignal(signal.SIGTSTP):
			p.send_signal(signal.SIGTSTP)
			basic_programs.processes[p.pid] = [p, "stopped"]
		elif e.args[0] == signal.strsignal(signal.SIGINT):
			p.send_signal(signal.SIGINT)
		display_exception(e)
		return None, e.__repr__().encode('utf-8')

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