'''
Recommendation:
Add condition in input_management.parse() that makes everything following echo an argument
For example:
 for t_list in tokens:
            new_list = [t_list[0], [], []]
            if t_list[0] == "echo": new_list[1] = [t_list[i] for i in range(1,len(t_list))]
            for t in t_list[1:]:
            etc
'''
def echo(args, flags):
  s = ""
  for a in args: s += a + " "
  for f in flags: s += f + " "
  print(s[:-1])
