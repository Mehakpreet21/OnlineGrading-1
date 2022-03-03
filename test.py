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
        line = line.strip()

        # skip blank lines and comments 
        if len(line) == 0 or line.startswith("#"): continue

        if is_param:
            params.append(f"{name}({line})")
        else:
            output.append(line)

        is_param = not is_param

    return params, output




print(get_testing_code("sum", testcases))


# import subprocess
# result = subprocess.check_output(['python', '-c', run])
# print(str(result.decode("utf-8") ))




def check_name(expected_function_name: str, raw_submission: str) -> bool:
    for line in raw_submission.splitlines():
        line = line.strip()

        if len(line) == 0 or line.startswith("#"): # skip empty lines and comments
            continue
        if not line.startswith("def "): # skip not function definition lines 
            continue
        
        try:
            # the name a function is the word after 'def ' and before the first '('
            func_name = line[4 : line.index('(')]
            if func_name == expected_function_name:
                return True
        except:
            # skip substring not found or any other error on search for function
            pass

    return False



def correct_name(expected_function_name: str, raw_submission: str) -> str:
    """Replace the first semi valid function definition name with expected_function_name.
    If there are no functions, append an empty function name called expected_function_name 
    """

    for line in raw_submission.splitlines():
        line = line.strip()

        if len(line) == 0 or line.startswith("#"): # skip empty lines and comments
            continue
        if not line.startswith("def "): # skip not function definition lines 
            continue
        
        # we are now at the first supposed function definition
        # it might not be partially syntactically correct. ex: "def ", "def name"

        try:
            # the name a function is the word after 'def ' and before the first '('
            func_name = line[4 : line.index('(')]
            # we are now at a valid function decleration. Replace the name

            return raw_submission.replace(f"def {func_name}(", f"def {expected_function_name}(")
        except:
            # skip substring not found or any other error on search for function
            pass


    # if we are unable to find a valid function definition we will add one.
    definition = f"""\ndef {expected_function_name}():\n    pass\n"""

    return raw_submission + definition



t = '''
#
#
def main():
    pass

#
def one():
    pass
#
#



def two(a,b):
    #
    return a + b

def three
'''

# print(check_name("main", t))
# print(check_name("one", t))
# print(check_name("two", t))
# print(check_name("three", t))
# print(check_name("four", t))
x = """
def d
"""
# print(correct_name("xx", t))
# print(correct_name("xx", x))