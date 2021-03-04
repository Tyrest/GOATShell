class input_manager:
    def __init__(self, fns):
        self.functions = fns

    # Return [[function 1, arglist 1, flags 1], [function 2, arglist 2, flags 2]]
    def parse(self, stdin):
        tokens = stdin.split("|")
        tokens = list(map(lambda x: x.split(), tokens))
        to_return = []

        # loop through each function call and separate args from flags
        for t_list in tokens:
            new_list = [t_list[0], [], []]
            for t in t_list[1:]:
                if t[0] == '-':
                    new_list[2].append(t)
                else:
                    new_list[1].append(t)
            to_return.append(new_list)
        return to_return

    # Return true if functions exist, false otherwise
    def check_input(self, input_functions):
        names = [self.functions[i][0] for i in range(len(self.functions))]
        for f in input_functions:
            if f[0] not in names:
                return False
        return True