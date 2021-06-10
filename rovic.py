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

variables = {

}

keywords = {
    'print': 'PRINT_KW ',
    'if': 'CONDITION ',
    'for': 'FOR_LOOP',
    'while': 'WHILE_LOOP',
}

numerals = ['0','1','2','3','4','5','6','7','8','9', '.']

math_symbols = ['+','-','/','*','%']

def lexer(code: str):
    tokens = []
    token = ""

    string = ""
    tk = ""

    state = 0
    variable_state = 0

    variable = ""

    numeral = ""

    boolean = ""

    expression = 0

    enclosure = 0

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
                    token += "STRING "
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
            elif tk in math_symbols:
                expression = 1
                numeral += tk
                tk = ""
            elif tk == ";":
                if expression:
                    token += "EXPR "
                    variables[variable] = (numeral, "EXPR")
                    numeral = ""
                elif expression == 0 and boolean == "":
                    variables[variable] = (numeral, "INT" if "." not in numeral else "FLOAT")

                    token += "INT " if "." not in numeral else "FLOAT "
                    
                    numeral = ""
                elif boolean != "":
                    variables[variable] = (boolean, "BOOLEAN")

                    token += "BOOLEAN "

                    boolean = ""

                tk = ""
                numeral = ""
                variable_state = 0
                expression = 0
                token += "SEMICOLON"
                tokens.append(token)
                token = ""
            elif state == 1:
                string += c 
                tk = ""
            else:
                boolean += c 
                tk = ""

        elif tk == '(':
            token += "LPAREN "
            tk = ""
            enclosure = 1
        elif tk == ")":
            if enclosure == 1:
                if expression == 1 and variable == "":
                    token += f"EXPR:{numeral} "

                    numeral = ""
                elif expression == 0 and variable == "":
                    token += f"INT:{numeral} " if "." not in numeral else f"FLOAT:{numeral} "
                    
                    numeral = ""
                else:
                    token += f"VARIABLE:{variable} "
                    variable = ""


            token += "RPAREN "
            enclosure = 0
            tk = ""
        elif tk == "\"":
            if state == 0:
                token += "OP_QUOT "
                state = 1
            elif state == 1:
                token += f"STRING:\"{string}\" "
                token += "CL_QUOT "
                
                enclosure = 0
                string = ""
                state = 0 
                tk = ""
        elif state == 1:
            string += c 
            tk = ""
        elif enclosure == 1:
            if tk in numerals:
                numeral += tk 
                tk = ""
            elif tk in math_symbols:
                expression = 1
                numeral += tk
                tk = ""
            else:
                variable += tk 
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