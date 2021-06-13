from sys import argv

def open_code(directory: str):
    try:
        file_contents = open(directory, 'r').read()

        #file_contents += "<EOF>"
    except FileNotFoundError as e:
        print(f"ERROR: FileNotFound -> The file \"{directory}\" is not found.")
        exit()

    return file_contents

boole = {
    'True': 'BOOL_TRUE',
    'False': 'BOOL_FALSE',
}
keywords = {
    'print': 'PRINT_KW ',
    'if': 'CONDITION_IF ',
    'elsif': 'CONDITION_ELSIF ',
    'else': 'CONDITION_ELSE ',
    'for': 'FOR_LOOP ',
    'while': 'WHILE_LOOP '
}
math_symbols = ['+', '-', '*', '/', '%']
numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
operators = ['=', '!', '<', '>']
variables = {

}

def lexer(code: str):
    
    tokens = []
    token = ""
    tk = ""

    numeral = ""
    operator = ""
    string = ""
    variable = ""

    condition = 0
    enclosure = 0
    expression = 0
    fill_paren = 0
    ifBool = 0
    operation = 0
    state = 0
    var_state = 0

    for c in code:
        tk += c                

        # WHITE SPACE
        if tk == " ":
            if state == 0:
                tk = ""

            elif state == 1:
                string += " "

        # NEXT LINE
        elif tk == "\n":
            tk = ""

        # KEYWORDS
        elif tk in keywords:     
            if tk == "if":
                condition = 1
            token += keywords[tk]

            tk = ""

        # VARIABLE INSTANTIATION
        elif "=" in tk and enclosure == 0:                        
            variable = tk.replace("=", "").strip()            
            
            var_state = 1
            variables[variable] = ""
            token += f"VARIABLE:{variable} EQUALS "
            
            tk = ""

        # VARIABLE VALUE
        elif var_state == 1:                
            if tk == "\"":
                if state == 0:
                    state = 1
                    token += "OP_QUOT "
                
                elif state == 1:
                    variables[variable] = (string, "STRING")
                    token += "STRING CL_QUOT "

                    string = ""
                    tk = ""
                    variable = ""

                    state = 0
                    var_state = 0
            
            elif tk in numerals:
                numeral += tk

                tk = ""

            elif tk in math_symbols:
                expression = 1
                numeral += tk

                tk =""

            elif state == 1:
                string += c

                tk = ""

            elif tk in boole:
                variables[variable] = (tk, "BOOLEAN")
                token += boole[tk] + " "
                ifBool = 1         

                tk = "" 
                variable = ""    
                var_state = 0 

            elif tk == "input":
                token += f"INPUT_KW "

                tk = ""
                variable = ""
                var_state = 0

            elif tk == ";":
                if expression == 1:
                    variables[variable] = (numeral, "EXPR")
                    token += "EXPR "

                    numeral = ""
                    expression = 0
                
                elif expression == 0 and ifBool == 0:
                    variables[variable] = (numeral, "INT" if "." not in numeral else "FLOAT")
                    token += "INT " if "." not in numeral else "FLOAT "

                    numeral = ""

                token += "SEMICOLON"
                tokens.append(token)

                tk = ""
                token = ""
                variable = ""
                ifBool = 0
                var_state = 0
                
        # LEFT PARENTHESIS
        elif tk == "(":
            token += "LPAREN "
            enclosure = 1

            tk = ""

        # RIGHT PARENTHESIS
        elif tk == ")":                                  
            if fill_paren == 1:     
                if operation == 1:
                    token += f"VARIABLE:{variable} OPERATOR:{operator} "
                    
                    if numeral != "":
                        token += f"INT:{numeral} " if "." not in numeral else f"FLOAT:{numeral} "

                        numeral = ""
                    
                    elif string != "":
                        token += f"OP_QUOT STRING:\"{string}\" CL_QUOT "

                        string = ""
                    
                    variable = ""
                    operator = ""
                    condition = 0
                    operation = 0   

                elif expression == 1:                
                    token += f"EXPR:{numeral} "

                    numeral = ""
                    expression = 0
                
                elif expression == 0 and numeral != "":                
                    token += f"INT:{numeral} " if "." not in numeral else f"FLOAT:{numeral} "

                    numeral = ""

                elif variable != "":
                    token += f"VARIABLE:{variable} "

                    variable = ""

            token += "RPAREN "
            enclosure = 0
            fill_paren = 0

            tk = ""        

        # ENCLOSURE
        elif enclosure == 1:            
            # QUOTATION MARK
            if tk == "\"" and condition == 0:
                fill_paren = 1
                if state == 0:
                    state = 1
                    token += "OP_QUOT "

                    tk = ""

                elif state == 1:
                    token += f"STRING:\"{string}\" CL_QUOT "

                    string = ""
                    tk = ""
                    state = 0

            # QUOTATION MARK IN CONDITION
            elif tk == "\"" and condition == 1:
                fill_paren = 1
                if state == 0:
                    state = 1                    

                    tk = ""

                elif state == 1:                   
                    tk = ""
                    state = 0
            
            # STRING READER
            elif state == 1:
                string += c

                tk = ""

            # INTEGER
            elif tk in numerals:
                fill_paren = 1
                numeral += tk

                tk = ""

            # EXPRESSION
            elif tk in math_symbols:
                expression = 1
                numeral += tk

                tk = ""

            # OPERATORS
            elif tk in operators:                
                fill_paren = 1
                operation = 1
                operator += tk

                tk = ""
                
            # VARIABLE READER
            else:                      
                fill_paren = 1
                variable += tk

                tk = ""


        # COLON
        elif tk == ":":
            token += "COLON"
            tokens.append(token)

            tk = ""
            token = ""

        # SEMICOLON
        elif tk == ";":
            token += "SEMICOLON"
            tokens.append(token)

            tk = ""
            token = ""

        

    
    print(variables)
    return tokens

if __name__ == "__main__":
    tokens = lexer(open_code(argv[1]))
    print(tokens)