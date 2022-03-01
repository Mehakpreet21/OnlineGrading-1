




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