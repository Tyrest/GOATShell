# GLOB notation / expansion with wildcards
cat *.py # should print all of the contents of the .py files
cat *.java # should print nothing
ls -la *.py # should print all names of python files
ls -la *.java #should print nothing
# mv

#The ability to start (in the foreground, or background with the ampersand symbol (&) ) processes on the OS.
sleep 3 # should sleep for 3 seconds
sleep 3 & # should sleep in the background for 3 seconds

# should print pid, "sleep 30", and "running"
sleep 30 &
jobs

sleep 3 & | echo # should return an error

# Quoting and backslash escaping of arguments and names.
touch my\ file.txt # should create a new file called my file.txt
echo hello \> world >my\ file.txt # should print "hello > world" to my file.txt
rm "my file.txt" # should remove this file
echo \> \>\> \& \$  # should print "> >> & $"
echo "> >> & $" # should print "> >> & $"

# Input and output redirection (the equivalent of bash's > and < operations)

# Piping input between commands (the equivalent of bash's | operation)
cat main.py | head -1 # should print "import basic_programs"

# Command substitution
echo $(echo $(echo $(echo hi))) # should print out "hi"
echo $(seq 1 3) # should print 1 2 3
cat $(echo $(echo main.py)) | head -1 # should print "import basic_programs"

# Reap zombie children
