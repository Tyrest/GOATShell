import os

def ls_long(ls_output):
    return ls_output

def ls_rec(current_directory, depth):
    to_return = []
    for path in os.listdir(current_directory):
        to_return.append("| "*depth + "{}".format(path))
        if not os.path.isfile("{}\\{}".format(current_directory, path)) and path[0] != '.':
            to_return += ls_rec("{}\\{}".format(current_directory, path), depth + 1)
    return to_return

def ls(args, flags):
    # Implement Recursive ls here (-R)
    ls_output = []
    hidden = []

    for path in os.listdir(os.getcwd()):
        if path[0] == '.':
            hidden.append(path)
        else:
            ls_output.append(path)
    
    flag_dictionary = {"-d": lambda x : list(filter(lambda y : not os.path.isfile(y), x)),
                       "-S": lambda x : list(sorted(x, key=lambda y :\
                           os.path.getsize(os.getcwd() + "\\{}".format(y)), reversed=True)),
                       "-a": lambda x : hidden + x,
                       "-s": lambda x : x,
                       "-l": ls_long,
                       "-X": lambda x : list(sorted(x, key=lambda y :\
                           os.path.splitext(os.getcwd() + "\\{}".format(y))[1], reversed=True))}
    
    flags = set(flags)
    
    # Sort flags in order of importance
    # (-a should go first and -l last)
    
    for flag in flags:
        flag_dictionary[flag](ls_output)
    
    to_return = "\nDirectory: {}\n{}\n".format(os.getcwd(), "-"*(len(os.getcwd()) + 11))

    for line in ls_output:
        to_return += "{}\n".format(line)

    return to_return

# dict_pids = {
#     p.info["pid"]: p.info["name"]
#     for p in psutil.process_iter(attrs=["pid", "name"])
# }

# print(dict_pids)

import subprocess
import psutil
p = subprocess.Popen("echo 5", shell=True)
p.wait()
print("{}\t{}\t{}".format(p.pid, "running" if p.poll() is None else "done", p.args))

current_process = psutil.Process()
children = current_process.children(recursive=True)

for child in children:
    print("{}\t{}\t{}".format(child.pid, child.status(), child.name()))#, " ".join(child.args)))

# while True:
#     stdin = input("GOATS: ")
#     p = subprocess.Popen(stdin, shell=True)

import subprocess
p = subprocess.Popen(['/bin/echo', 'hello'], stdout = open('/Users/Sarah/Desktop/GOATShell/sarah.py', 'w'))
p.communicate()