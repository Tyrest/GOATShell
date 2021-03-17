import os, subprocess
# Takes in input string from stdin
# Return (value for Popen stdin arg, value for Popen stdout arg, s without in/out redirectors)
# Valid values are PIPE, DEVNULL, an existing file descriptor (a positive integer), an existing file object, and None.
def in_out_info(s):
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
                s = s[i+1:]
            else:
                stdout = open(s[i+1:].strip(), 'w')
                s = s[i+1:]
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
            s = s[:i]
    else:
        stdin = subprocess.PIPE
    return stdin, stdout, s
s = "echo hellohello >/Users/Sarah/Desktop/test.py"
print(in_out_info(s))