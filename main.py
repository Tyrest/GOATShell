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

def signal_handler(sig, frame):
	raise Exception(signal.strsignal(sig))

def signal_none(sig, frame):
	print("\n")
	raise Exception

# Exit program
def exit(args, flags):
	sys.exit(0)

functions = dict(getmembers(basic_programs, isfunction) + getmembers(extras, isfunction))
functions.update([('exit', exit)]) 

# Main shell loop
def main():
	im = input_management.input_manager(functions)
	builtin_names = list(functions.keys())
	while(True):
		signal.signal(signal.SIGINT, signal_none)
		signal.signal(signal.SIGTSTP, signal_none)
		try:
			stdin = input("GOATS: ")
		except Exception:
			continue
		bg, t = im.parse(stdin)
		if t == None: continue

		pipe_input = None
		for fncall in t:
			fn_name = fncall[0]; fn_args = fncall[1]
			if pipe_input != None: fn_args.append(pipe_input.name)
			
			try:
				if fn_name not in builtin_names:
					output = exec_process([fn_name] + fn_args, bg)
					if pipe_input != None: pipe_input.close()
				else:
					output = functions[fncall[0]](fn_args, [])
					if output != None: output = output.encode('utf-8')
				if output != None: 
					print(output.decode('utf-8'))

					# Pass temporary file to next function call
					pipe_input = tempfile.NamedTemporaryFile()
					pipe_input.write(output); pipe_input.seek(0)
			except Exception as e:
				print(type(e).__name__ + ": " + str(e.args[0]))

# Executes process
def exec_process(tokens, bg):
	try:
		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGTSTP, signal_handler)
		current_process = p = subprocess.Popen(tokens, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		if bg == False:
			out, err = p.communicate(timeout=10**3)
			return out + err
		else:
			basic_programs.processes.append(p)
			return None

	except subprocess.TimeoutExpired:
		print("Timeout expired. Killing process...")
		p.kill()
		out, err = p.communicate(timeout=10**3)
		return out + err

	except Exception as e:
		if e.args[0] == signal.strsignal(signal.SIGTSTP):
			p.send_signal(signal.SIGTSTP)
			basic_programs.processes.append(p)
		elif e.args[0] == signal.strsignal(signal.SIGINT):
			p.send_signal(signal.SIGINT)
		print(type(e).__name__ + ": " + str(e.args[0]))

if __name__ == '__main__':
	main()