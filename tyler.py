import os

print(os.getcwd())
print(os.listdir(os.getcwd()))

def ls(args, flags):
    # Implement Recursive ls here (-R)

    to_return = "\nDirectory: {}\n{}\n".format(os.getcwd(), "-"*(len(os.getcwd()) + 11))
    for path in os.listdir(os.getcwd()):
        to_return += "{}\n".format(path)
    
    flag_dictionary = {"d": lambda x : list(filter(lambda y : not os.path.isfile(y), x)),
                       "s": lambda x : list(sorted(x, key=lambda y : os.path.getsize(os.getcwd() + "\\{}".format(y)), reversed=True)),
                       "l": ,
                       "a": ,
                       "S": ,
                       "t": ,
                       "X": }

    for flag in flags:
        
    return to_return

print(ls([], []))