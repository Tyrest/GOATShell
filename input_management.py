import os
import subprocess
class input_manager:
    def __init__(self, fns):
        self.functions = fns

    # Return (bg, file_in, file_out, [[function 1, arglist 1], [function 2, arglist 2]])
    # where bg = True if the process should run in the background, false otherwise
    def parse(self, stdin):
        # check if the process should run in the background
        bg = False
        stdin = stdin.strip()
        if stdin[-1] == '&':
            bg = True
            stdin = stdin[:-1]

        file_in, file_out, stdin = self.in_out_info(stdin)
        tokens = stdin.split("|")
        tokens = list(map(lambda x: x.split(), tokens))

        # separate fn name from args
        return bg, file_in, file_out, list(map(lambda x: [x[0], x[1:]], tokens))

    # Takes in input string from stdin
    # Return (value for Popen stdin arg, value for Popen stdout arg, s without in/out redirectors)
    # Valid values are PIPE, DEVNULL, an existing file descriptor (a positive integer), an existing file object, and None.
    def in_out_info(self, s):
        # characters are escaped if occurrences of \> = occurences of >
        # echo ">" >sarah.py or echo \>>sarah.py
        if s.count("\>") != s.count(">"):
            # take the last occurence of >
            i = len(s) - 1 - s[::-1].index(">")
            # make sure character isn't escaped by surrounding quotation marks
            if "\'" in s[i:] or "\" " in s[i: ]: 
                stdout = subprocess.PIPE
            else:
                # check if > or >>; if so, make sure previous > isn't escaped
                if len(s[:i]) > 1 and s[i-1] == '>' and s[i-2] != '\\':
                    stdout = open(s[i+1:].strip(), 'a')
                    s = s[:i]
                else:
                    stdout = open(s[i+1:].strip(), 'w')
                    s = s[:i]
        else:
            stdout = subprocess.PIPE

        if s.count("\<") != s.count("<"):
            # take the first occurence of <
            i = s.index("<")

            # make sure character isn't escaped by surrounding quotation marks
            if "\'" in s[:i] or "\" " in s[:i]: 
                stdin = subprocess.PIPE
            else:
                # consider pipes?
                stdin = open(s[:i], 'r')
                s = s[i+1:]
        else:
            stdin = subprocess.PIPE
        return stdin, stdout, s
