from sys import argv

def open_code(directory: str):
    try:
        file_contents = open(directory, 'r').read()

        #file_contents += "<EOF>"
    except FileNotFoundError as e:
        print(f"ERROR: FileNotFound -> The file \"{directory}\" is not found.")
        exit()

    return file_contents

"""
if in keyword
colon
pinalitan ko code nung sa variable mo. ginawa kong "string" in tk para madetect niya yung =
for and while loop sa keywords

data types: [int, float, string, bool]
"""

def lexer(code: str):
    tokens = []
    token = ""

    string = ""
    tk = ""

    state = 0
    variable_state = 0

    keywords = {
        'print': 'PRINT_KW ',
        'if': 'CONDITION ',
        'for': 'FOR_LOOP',
        'while': 'WHILE_LOOP',
    }

    variable = ""
    variables = {

    }


    numeral = ""
    numerals = ['0','1','2','3','4','5','6','7','8','9', '.']

    for c in code:
        tk += c 
        
        if tk == " ":
            if state == 0:
                tk = ""
            else:
                string += " "
        elif tk == "\n":
            tk = ""
        elif tk in keywords:
            token += keywords[tk]
            tk = ""
        elif variable_state == 1:
            if tk == "\"":
                if state == 0:
                    token += "OP_QUOT "
                    state = 1
                elif state == 1:
                    token += f"STRING "
                    token += "CL_QUOT "
                    variables[variable] = (string, "STRING")
                    variable = ""
                    state = 0
                    tk = ""
                    string = ""
                    variable_state = 0
            elif tk in numerals:
                numeral += tk 
                tk = ""
            else:
                string += c 
                tk = ""

        elif tk == '(':
            token += "LPAREN "
            tk = ""
        elif tk == ")":
            token += "RPAREN "
            tk = ""
        elif tk == "\"":
            if state == 0:
                token += "OP_QUOT "
                state = 1
            elif state == 1:
                token += f"STRING:\"{string}\" "
                token += "CL_QUOT "

                string = ""
                state = 0 
                tk = ""
        elif state == 1:
            string += c 
            tk = ""
        elif "=" in tk:
            variable = tk.replace("=", "")
            variable = variable.strip()

            token += f"VARIABLE:{variable} EQUALS "

            variables[variable] = ""
            variable_state = 1 # is variable
            tk = ""
        elif tk == ":":
            token += "COLON"
            tokens.append(token)
            token = ""
            tk = ""
            state = 0
        elif tk == ";":
            token += "SEMICOLON"
            tokens.append(token)
            token = ""
            tk = ""
            state = 0
    
    print(variables)
    return tokens

if __name__ == "__main__":
    tokens = lexer(open_code(argv[1]))
    print(tokens)