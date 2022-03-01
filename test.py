# this is just some test code for use later for autograde

name = ''
detail = \
"""
"""
testcases = \
"""
#3
#6
# comment

#4
#8

# comment

[1,2,3,4]
10
[0,0,0,1,3,2,0,1]
7
"""
###
submission = \
"""
def sum(arr):
    s = 0
    for i in arr:
        s = s + i
    return s
"""

def get_testing_code(name: str, testcases: str):
    params = []
    output = []

    is_param = True
    for line in testcases.splitlines():
        # skip blank lines and comments 
        if len(line) == 0 or line.startswith("#"): continue

        if is_param:
            params.append(f"print({name}({line}))\n")
        else:
            output.append(line + '\n')

        is_param = not is_param

    return "".join(params), "".join(output)




print(get_testing_code("sum", testcases))


# import subprocess
# result = subprocess.check_output(['python', '-c', run])
# print(str(result.decode("utf-8") ))


