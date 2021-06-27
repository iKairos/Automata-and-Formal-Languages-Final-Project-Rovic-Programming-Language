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
    'endif': 'END_IF_KW ',
    'endfor': "END_FOR_KW"
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
    variable_2 = ""

    array_state = 0
    condition = 0
    enclosure = 0
    expression = 0
    fill_paren = 0
    ifBool = 0
    loop = 0
    operation = 0
    state = 0
    sec_var = 0
    var_state = 0

    for c in code:
        tk += c                
        # WHITE SPACE
        if tk == " ":
            if state == 0:
                tk = ""

            elif state == 1:
                string += " "
                tk = ""

        # NEXT LINE
        elif tk == "\n":
            tk = ""

        # KEYWORDS
        elif tk in keywords:     
            if tk == "if" or tk == "elsif":
                condition = 1
            token += keywords[tk]

            tk = ""

        # VARIABLE INSTANTIATION
        elif "=" in tk and enclosure == 0:                        
            variable = tk.replace("=", "").strip()            
            
            var_state = 1
            #variables[variable] = ""
            token += f"VARIABLE:{variable} EQUALS "
            
            tk = ""

        # VARIABLE VALUE
        elif var_state == 1:        
            if tk == "\"":                
                if state == 0:
                    state = 1
                    #token += "OP_QUOT"
                
                elif state == 1 and array_state == 1:                    
                    token += f"STRING:{string}"

                    tk = ""
                    state = 0

                elif state == 1 and array_state == 0:
                    #variables[variable] = (string, "STRING")
                    token += f"STRING:{string}"

                    string = ""
                    tk = ""
                    variable = ""

                    state = 0
                    var_state = 0
            
            elif tk == "[":
                array_state = 1

                token += "ARRAY:["
                tk = ""

            elif tk == "]":
                if numeral != "":
                    token += f"INT:{numeral}" if "." not in numeral else f"FLOAT:{numeral}"
                token += "] "
                tk = ""
                numeral = ""

            elif tk == "," and array_state == 1:
                if numeral != "":
                    token += f"INT:{numeral}," if "." not in numeral else f"FLOAT:{numeral},"
                # elif string != "":
                #     token += f"STRING:{string} CL_QUOT, "
                else:
                    token += ","
            
                tk = ""
                numeral = ""
                string = ""
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

            # elif tk == "input":
            #     token += f"INPUT_KW "

            #     tk = ""
            #     variable = ""
            #     var_state = 0

            elif tk == ";":
                if expression == 1 and array_state == 0:
                    #variables[variable] = (numeral, "EXPR")
                    token += f"EXPR:{numeral} "

                    numeral = ""
                    expression = 0
                
                elif variable_2 != "" and array_state == 0:
                    token += f"VARIABLE:{variable_2} "

                    variable_2 = ""
                
                elif expression == 0 and array_state == 0:
                    #variables[variable] = (numeral, "INT" if "." not in numeral else "FLOAT")
                    token += f"INT:{numeral} " if "." not in numeral else f"FLOAT:{numeral} "

                    numeral = ""

                token += "SEMICOLON"
                tokens.append(token)

                tk = ""
                token = ""
                variable = ""
                array_state = 0
                ifBool = 0
                var_state = 0
            
            else:
                variable_2 += tk 

                if variable_2 == "input":
                    token += f"INPUT_KW "
                    variables[variable] = None
                    tk = ""
                    variable = ""
                    var_state = 0

                elif variable_2 in boole:
                    #variables[variable] = (tk, "BOOLEAN")
                    token += boole[variable_2] + " "      

                    tk = "" 
                    variable = ""    
                    variable_2 = ""
                    var_state = 0

                tk = ""
                
                
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

                    elif variable_2 != "":
                        token += f"VARIABLE2:{variable_2} "
                    
                    variable = ""
                    variable_2 = ""
                    operator = ""
                    condition = 0
                    ifBool = 0
                    operation = 0 
                    sec_var = 0  

                elif ifBool == 1:                                           
                        token += f"BOOL:{boolean} " 

                        boolean = ""
                        ifBool = 0

                elif loop == 1:
                    token += f"VARIABLE:{variable} OPERATOR:{loop_operator} "
                    if numeral != "":
                        token += f"INT:{numeral} " if "." not in numeral else f"FLOAT:{numeral} "

                    elif variable_2 != "":
                        token += f"VARIABLE2:{variable_2} "

                    loop_operator = ""
                    numeral = ""
                    variable = ""
                    loop = 0
                
                elif variable != "":                                        
                    token += f"VARIABLE:{variable} "

                    variable = ""

                elif expression == 1:                
                    token += f"EXPR:{numeral} "

                    numeral = ""
                    expression = 0
                
                elif expression == 0 and numeral != "":                
                    token += f"INT:{numeral} " if "." not in numeral else f"FLOAT:{numeral} "

                    numeral = ""

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
                sec_var = 1

                tk = ""
                
            # VARIABLE READER
            else:                                    
                fill_paren = 1    
                if sec_var == 0:            
                    variable += tk                

                elif sec_var == 1:
                    variable_2 += tk

                if tk == "i":
                    loop_operator += tk

                elif loop_operator == "i":
                    print("kairos the great jakolero")
                    loop_operator += tk

                if loop_operator == "in":  
                    print("kairitous")                  
                    loop = 1
                    sec_var = 1
                    variable = variable.replace("in", "")

                if "True" in variable:                      
                    ifBool = 1

                    boolean = boole[variable[-4:]]
                    variable = variable.replace("True", "")                               
                                    
                elif "False" in variable:
                    ifBool = 1
                    boolean = boole[variable[-5:]]
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

def exec_print(normalizedToken, token, line):
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
            print(variables[variable])
        except KeyError:
            print(f"An error has occurred at line {line}: Variable does not exist.")

def parser(tokens):
    line = 1    
    cond_closures = []
    enc = 0
    who_enc = 0

    in_cond = False
    add_toks = False

    for token in tokens:
        print(token)
        normalizedToken = token        
        if in_cond:

            identifier = token[0:18]

            if identifier == "CONDITION_ELSIF_KW":
                condition = token[:token.index("RPAREN")-1].replace("CONDITION_ELSIF_KW ", "")
                condition = condition.split(" ")
                condition = [i.split(":") if len(i.split(":")) > 1 else None for i in condition]
                condition = list(filter(None, condition))
                
                stringified = ""
                for tok, val in condition:
                    if tok == "VARIABLE":
                        if type(variables[val]) is str:
                            stringified += f"\"{variables[val]}\""
                        else:
                            stringified += f"{variables[val]}"
                    else:
                        stringified += val
                
                who_enc += 1
                cond_closures[enc].append(("elsif", eval(stringified), []))
            
            if add_toks:
                if "CONDITION_ELSIF_KW" in token:
                    pass
                else:
                    cond_closures[enc][who_enc][2].append(token)
            
            identifier = token[0:17]
            if identifier == "CONDITION_ELSE_KW":
                who_enc += 1
                cond_closures[enc].append(("else", True, []))

            identifier = token[0:9]
            if identifier == "END_IF_KW":
                for kw, cond, ts in cond_closures[enc]:
                    if cond:
                        parser(ts)
                        break

                in_cond = False 
                enc += 1
                who_enc = 0 
            
        else:
            identifier = token[0:15]

            # check if if
            if identifier == "CONDITION_IF_KW":
                condition = token[:token.index("RPAREN")-1].replace("CONDITION_IF_KW LPAREN ", "")
                condition = condition.split(" ")
                condition = [i.split(":") if len(i.split(":")) > 1 else None for i in condition]
                condition = list(filter(None, condition))
                stringified = ""

                for tok, val in condition:
                    if tok == "VARIABLE" or tok == "VARIABLE2":
                        if type(variables[val]) is str:
                            stringified += f"\"{variables[val]}\""
                        else:
                            stringified += f"{variables[val]}"
                    elif tok == "BOOL":
                        key_list = list(boole.keys())
                        val_list = list(boole.values())
                        position = val_list.index(val)
                        stringified += key_list[position]
                        stringified = stringified.replace("\"", "")
                    else:
                        stringified += val
            
                cond_closures.append([("if", eval(stringified), [])])

                in_cond = True
                add_toks = True
            
            identifier = token[0:8]

            # check if print
            if identifier == "PRINT_KW":
                exec_print(normalizedToken, token, line)

            identifier = token[0:8]
            
            if identifier == "VARIABLE":
                
                toks = token.replace(" EQUALS", "")
                toks = toks.replace(" SEMICOLON", "")
                toks = toks.replace(" OP_QUOT", "")
                toks = toks.replace(" CL_QUOT", "")
                toks = toks.split(" ")
                
                variable = toks[0][9:]

                data_type = toks[1][0:8]
                if data_type == "INPUT_KW":
                    prompt = token[token.index("STRING") + 7:].replace(" CL_QUOT RPAREN SEMICOLON", "")
                    variables[variable] = input(prompt.replace("\"",""))

                data_type = toks[1][0:3]
                if data_type == "INT":
                    variables[variable] = int(toks[1][4:])
                
                data_type = toks[1][0:5]
                if data_type == "FLOAT":
                    variables[variable] = float(toks[1][6:])
                
                data_type = toks[1][0:6]
                if data_type == "STRING":
                    variables[variable] = token[token.index("STRING") + 7:].replace(" CL_QUOT SEMICOLON", "")
                
                data_type = toks[1][0:4]
                if data_type == "BOOL":
                    key_list = list(boole.keys())
                    val_list = list(boole.values())
                    position = val_list.index(toks[1])
                    variables[variable] = key_list[position]
                
                if data_type == "EXPR":
                    variables[variable] = eval(toks[1][5:])
                
                data_type = toks[1][0:8]
                if data_type == "VARIABLE":
                    variables[toks[0][9:]] = variables[toks[1][9:]]

                data_type = toks[1][0:5]
                if data_type == "ARRAY":
                    temp = toks[1][6:]
                    temp = temp[1:]
                    temp = temp[:len(temp)-1]
                    temp = temp.split(",")

                    arr = []
                    for i in temp:
                        tp = i.split(':')
                        typ = tp[0]
                        va = tp[1]

                        if typ == "INT":
                            arr.append(int(va))
                        elif typ == "FLOAT":
                            arr.append(float(va))
                        elif typ == "STRING":
                            arr.append(va)
                    
                    variables[variable] = arr

            line += 1

if __name__ == "__main__":
    tokens = lexer(open_code(argv[1]))
    parser(tokens)