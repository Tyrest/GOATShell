class input_manager:
    def __init__(self, fns):
        self.functions = fns

    # Return (bg, [[function 1, arglist 1], [function 2, arglist 2]])
    # where bg = True if the process should run in the background, false otherwise
    def parse(self, stdin):
        if len(stdin.strip()) == 0:
            return None,None

        # check if the process should run in the background
        bg = False
        stdin = stdin.strip()
        if stdin[-1] == '&':
            bg = True
            stdin = stdin[:-1]

        tokens = stdin.split("|")
        tokens = list(map(lambda x: x.split(), tokens))

        # separate fn name from args
        return bg, list(map(lambda x: [x[0], x[1:]], tokens))
