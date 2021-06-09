from sys import argv

def open_code(directory: str):
    try:
        file_contents = open(directory, 'r').read()

        #file_contents += "<EOF>"
    except FileNotFoundError as e:
        print(f"ERROR: FileNotFound -> The file \"{directory}\" is not found.")
        exit()

    return file_contents

def lexer(code: str):
    tokens = []
    token = ""

    string = ""
    tk = ""

    state = 0

    keywords = {
        'print': 'PRINT_KW '
    }

    variable = ""
    variables = {

    }

    for c in code:
        tk += c 
        print(tk)
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
        elif tk == "=":
            token += f"VARIABLE: {tk}"
            variables[tk] = ""
            tk = ""
        elif tk == ";":
            token += "SEMICOLON"
            tokens.append(token)
            token = ""
            tk = ""
            state = 0
    
    return tokens

if __name__ == "__main__":
    tokens = lexer(open_code(argv[1]))
    print(tokens)