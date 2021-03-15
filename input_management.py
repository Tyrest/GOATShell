import main
class input_manager:
    def __init__(self, fns):
        self.functions = fns

    # Return (bg, [[function 1, arglist 1], [function 2, arglist 2]])
    # where bg = True if the process should run in the background, false otherwise
    def parse(self, stdin):
        # check if the process should run in the background
        bg = False
        stdin = stdin.strip()
        if stdin[-1] == '&':
            bg = True
            stdin = stdin[:-1]

        # handle case of subcommands
        while '$(' in stdin:
            stdin = self.subcommand_handler(stdin)

        tokens = stdin.split("|")
        tokens = list(map(lambda x: x.split(), tokens))

        # separate fn name from args
        return bg, list(map(lambda x: [x[0], x[1:]], tokens))

    # For command substitution
    # Replaces deepest instance of $(command) with output from command
    def subcommand_handler(self, stdin):
        # find deepest occurence of $, index = len(stdin) - 1 - (first index of $ in reversed stdin)
        index1 = len(stdin) - 1 - (stdin[::-1].index('($'))
        index2 = stdin.index(')', index1)
        c = stdin[index1 + 1 : index2]
        
        # execute command 
        output = main.exec_command(c, self)
        if output is None: 
            output = ''

        # replace $(command) with output
        return stdin.replace('$(' + c + ')', output.decode('utf-8').strip())
