from curses import raw
import subprocess





def get_params_output_from_testcases(name: str, testcases: str):
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

def check_constraint(constraint: str, raw_submission: str) -> bool:
    return constraint in raw_submission


def get_output(source_code):
    try:
        result = subprocess.check_output(['python', '-c', f"{source_code}"], stderr=subprocess.PIPE)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()


# return List[  ( param, expected, actual, score )  ]
def grade_testcases(params, expected_output, raw_student_output, item_score):
    # transform student_output into array of lines. 1 line for each case
    student_outputs = raw_student_output.splitlines()

    return_data = []
    for i in range(len(params)):
        expected = expected_output[i]
        try:
            actual = student_outputs[i]
        except:
            actual = ""

        score = item_score if expected == actual else 0
        return_data.append( (params[i], expected, actual, score) )

    return return_data
