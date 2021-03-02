import os

print(os.getcwd())
print(os.listdir(os.getcwd()))

def ls_long(ls_output):
    return ls_output

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

print(ls([], []))