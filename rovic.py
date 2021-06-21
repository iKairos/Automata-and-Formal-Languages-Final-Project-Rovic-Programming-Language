from sys import argv, path_importer_cache

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
condition = [
    
]
keywords = {
    'print': 'PRINT_KW ',
    'if': 'CONDITION_IF_KW ',
    'elsif': 'CONDITION_ELSIF_KW ',
    'else': 'CONDITION_ELSE_KW ',
    'for': 'FOR_LOOP_KW ',
    'while': 'WHILE_LOOP_KW ',
    'endif': 'END_IF_KW '
}
loop = [

]
math_symbols = ['+', '-', '*', '/', '%']
numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
operators = ['=', '!', '<', '>']
variables = {

}

def lexer(code: str):
    
    tokens = []
    token = ""
    tk = ""

    boolean = ""
    loop_operator = ""
    numeral = ""
    operator = ""
    string = ""
    variable = ""

    condition = 0
    enclosure = 0
    expression = 0
    fill_paren = 0
    ifBool = 0
    loop = 0
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

                    elif ifBool == 1:                                          
                        token += f"BOOL:{boolean} "           
                    
                    variable = ""
                    operator = ""
                    condition = 0
                    operation = 0   

                elif ifBool == 1:                                           
                        token += f"BOOL:{boolean} " 

                        boolean = ""
                        ifBool = 0

                elif loop == 1:
                    token += f"VARIABLE:{variable} OPERATOR:{loop_operator} INT:{numeral} "

                    loop_operator = ""
                    numeral = ""
                    variable = ""
                    loop = 0

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

                if tk == "i":
                    loop_operator += tk

                elif loop_operator == "i":
                    loop_operator += tk

                if loop_operator == "in":                    
                    loop = 1
                    variable = variable.replace("in", "")

                if "True" in variable:                      
                    ifBool = 1

                    boolean = boole[variable.replace("var", "")]
                    variable = variable.replace("True", "")                                   
                                    
                elif "False" in variable:
                    ifBool = 1
                    boolean = boole[variable.replace("var", "")]
                    variable = variable.replace("False", "")
                
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

    #print(variables)
    return tokens

def parser(tokens):
    line = 1
    
    cond_closures = []

    for token in tokens:
        #print(token)
        normalizedToken = token

        identifier = token[0:8]
        # check if print
        if identifier == "PRINT_KW":
            if "STRING" in token:
                normalizedToken = normalizedToken[0:30] + " CL_QUOT RPAREN SEMICOLON"
            elif "BOOL" in token:
                normalizedToken = normalizedToken[0:20] + " RPAREN SEMICOLON"
            elif "EXPR" in token:
                normalizedToken = normalizedToken[0:20] + " RPAREN SEMICOLON"
            elif "VARIABLE" in token:
                normalizedToken = normalizedToken[0:24] + " RPAREN SEMICOLON"
            elif "FLOAT" in token:
                normalizedToken = normalizedToken[0:21] + " RPAREN SEMICOLON"
            elif "INT" in token:
                normalizedToken = normalizedToken[0:19] + " RPAREN SEMICOLON"
            
            if normalizedToken == "PRINT_KW LPAREN BOOL RPAREN SEMICOLON":
                key_list = list(boole.keys())
                val_list = list(boole.values())
                position = val_list.index(token[21:].replace(" RPAREN SEMICOLON", ""))
                print(key_list[position])
            elif normalizedToken == "PRINT_KW LPAREN FLOAT RPAREN SEMICOLON":
                print(token[22:].replace(" RPAREN SEMICOLON", ""))
            elif normalizedToken == "PRINT_KW LPAREN INT RPAREN SEMICOLON":
                print(token[20:].replace(" RPAREN SEMICOLON", ""))
            elif normalizedToken == "PRINT_KW LPAREN OP_QUOT STRING CL_QUOT RPAREN SEMICOLON":
                print(token[32:].replace("\" CL_QUOT RPAREN SEMICOLON", ""))
            elif normalizedToken == "PRINT_KW LPAREN EXPR RPAREN SEMICOLON":
                print(eval(token[21:].replace(" RPAREN SEMICOLON", "")))
            elif normalizedToken == "PRINT_KW LPAREN VARIABLE RPAREN SEMICOLON":
                variable = token[25:].replace(" RPAREN SEMICOLON", "")
                try:
                    print(variables[variable][0])
                except KeyError:
                    print(f"An error has occurred at line {line}: Variable does not exist.")
        
        identifier = token[0:15]

        # check if if
        if identifier == "CONDITION_IF_KW":
            cond_enclosure = 1

            condition = token[:token.index("RPAREN")-1].replace("CONDITION_IF_KW LPAREN ", "")
            condition = condition.split(" ")
            condition = [i.split(":") if len(i.split(":")) > 1 else None for i in condition]
            condition = list(filter(None, condition))
            print(condition)
            stringified = ""
            for tok, val in condition:
                if tok == "VARIABLE":
                    stringified += variables[val][0]
                else:
                    stringified += val
            
            print(stringified)
            print(eval(stringified))
        
        line += 1

if __name__ == "__main__":
    tokens = lexer(open_code(argv[1]))
    parser(tokens)