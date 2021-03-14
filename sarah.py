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

s = 'cat $(echo $(echo s.py))'
s = 'echo $(seq 1 3)'
im = input_manager(dict())
exec_command(subcommand_handler(s, im), im)