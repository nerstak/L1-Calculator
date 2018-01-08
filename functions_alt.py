def type_calc(x): #This function defines the type of the variable put in. It doesn't work with string
    if x in ["/","-","+","*","==","<",">","<>","<=",">=","not","and","or","#","%"] :
        return 'operator'
    elif x == '(' or x == ')':
        return 'parenthesis'
    elif x in ["true","false"]:
        return 'boolean'
    else:
        try: #The try-except part is a way to differentiate integer (including float) from variable. It avoids the crash of the program when 'int(x)' is executed
            int(x)
            return 'integer'
        except ValueError:
            return 'string'

def string_to_list_type(string): #Function to converts a string into a list of list. Container 0 is the content, Container 1 is the type of content
    list = []
    i = 0
    while i < len(string):
        if 'integer' == type_calc(string[i]):
            nb = ''
            cpt_point = 0
            while i < len(string) and ('integer' == type_calc(string[i]) or string[i]=='.'):
                nb = nb + string[i]
                if string[i] == '.':
                    cpt_point+=1
                    if cpt_point > 1:
                        return (None,"Error: Incorrect number")
                i+=1
            if float(nb) == int(float(nb)):
                nb = int(float(nb))
            list.append((nb,type_calc(i)))
        elif string[i] == '"':
            if string.count('"') % 2 != 0:
                return (None,"Error: Missing quote")
            nb = ''
            i+=1
            while i < len(string) and string[i] != '"':
                nb = nb +string[i]
                i+=1
            i+=1
            list.append((nb,"string"))
        elif string[i] != " ":
            if (type_calc(string[i]) in ["operator","parenthesis"]):
                if string[i] == "<" and i+1<len(string) and string[i+1] in ["=",">"]:
                    list.append((string[i]+string[i+1],"operator"))
                    i+=2
                elif string[i] == ">" and i+1<len(string) and string[i+1] == "=":
                    list.append((string[i]+string[i+1],"operator"))
                    i+=2
                else:  
                    list.append((string[i],type_calc(string[i])))
                    i+=1
            elif string[i] == '=':
                if i+1<len(string) and string[i+1] == '=':
                    list.append(("==","operator"))
                    i+=2
                else:
                    list.append(("=","setvariable"))
                    i+=1
            else:
                continu = True
                nb = ''
                while i < len(string) and (string[i] not in [" ",'"','(',')','='] and type_calc(string[i]) != "operator") and continu == True:
                    nb = nb + string[i]
                    i+=1
                    if i>= len(string) or nb in ['not','or','and'] and type_calc(string[i]) not in ("integer","string"):
                        continu = False
                if type_calc(nb) == 'string':
                    list.append((nb,'variable'))
                else:
                    list.append((nb,type_calc(nb)))
        else:
            i+=1
    return (list,None)

def check_errors(array1,array2,result): #Function to check if they are any error for some parts
    if array1[1] == array2[1] == None:
        return (result,None)
    elif array1[1] != None:    
        return (None,array1[1])
    else:
        return (None,array2[1])

def evaluate(polynom,str_warn=0):
    for i in polynom:
        if i[1] == "string":
            str_warn = 1
    list1 = []
    list2 = []
    list3 = []
    if ('(','parenthesis') in polynom or (')','parenthesis') in polynom:
        i = cpt =0
        while cpt >= 0 and i < len(polynom):
            if polynom[i][0] == '(':
                cpt +=1
            elif polynom[i][0] == ')':
                cpt -= 1
            i += 1
            if cpt < 0:
                return (None,"Error: wrong syntax (missing parenthesis '(')")
        if cpt !=0:
            return (None,"Error: wrong syntax (missing parenthesis ')')")
        nbr_p = i = 0
        pos_p = -1
        while i < len(polynom) and pos_p == -1:
            if polynom[i][0] == '(':
                nbr_p += 1
            elif polynom[i][0] == ')' and nbr_p == 1:
                pos_p = i
            elif polynom[i][0] == ')' and nbr_p != 1:
                nbr_p -= 1
            i += 1
        for i in range(polynom.index(('(','parenthesis'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('(','parenthesis'))+1,pos_p):
            list2.append(polynom[i])
        for i in range(pos_p+1,len(polynom)):
            list3.append(polynom[i])
        temp = evaluate(list2)
        if temp[1] is not None:
            return (None,temp[1])
        else:
            temp, Error = string_to_list_type(str(temp[0]))
            if temp[0][1] == 'variable':
                ret = list1 + [(temp[0][0],'string')] + list3
            else:
                ret = list1 + temp + list3
            return (evaluate(ret))
    elif ('or','operator') in polynom:
        temp = len(polynom)
        for i in range(polynom.index(('or','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('or','operator'))+1,temp):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "or"')
        temp1 = evaluate(list1)
        temp2 = evaluate(list2)
        expected_result = None
        if temp2[1] == None and temp2[1] == None:    
            if temp1[0] == 'true' or temp2[0] == 'true' :
                expected_result = "true"
            else:
                expected_result = "false"
        return check_errors(temp1,temp2,expected_result)
    elif ('and','operator') in polynom:
        temp = len(polynom)
        operator_pos = -1
        t = polynom.index(('and','operator'))+1
        while t < len(polynom) and operator_pos==-1:
            if polynom[t][0] in ["or"]:
                temp = t
            t+=1
        for i in range(polynom.index(('and','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('and','operator'))+1,temp):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "and"')
        temp1 = evaluate(list1)
        temp2 = evaluate(list2)
        expected_result = None
        if temp1[1] == None and temp2[1] == None:    
            if temp1[0] == temp2[0] == "true" :
                expected_result = "true"
            else:
                expected_result = "false"
        return check_errors(temp1,temp2,expected_result)
    elif ('not','operator') in polynom:
        temp = len(polynom)
        operator_pos = -1
        t = polynom.index(('not','operator'))+1
        while t < len(polynom) and operator_pos==-1:
            if polynom[t][0] in ["and","or"]:
                temp = t
            t+=1
        for i in range(polynom.index(('not','operator'))+1,temp):
            list1.append(polynom[i])
        if list1 == []:
            return (None,"Error: Missing operand after 'not'")
        temp1 = evaluate(list1)
        expected_result = None
        if temp1[1] == None:
            if temp1[0] in  ("false","0"):
                expected_result = "true"
            else:
                expected_result = "false"
        return check_errors(temp1,(None,None),expected_result)
    elif ("==","operator") in polynom:
        for i in range(polynom.index(('==','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('==','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "=="')
        if str_warn == 1:
            temp1,Error1 = evaluate(list1,1)
            temp2,Error2 = evaluate(list2,1)
            temp1 = str(temp1)
            temp2 = str(temp2)
        else:
            temp1, Error1 = evaluate(list1)
            temp2, Error2 = evaluate(list2)
        expected_result = None
        if Error1 == None and Error2 == None:    
            if temp1 == temp2:
                expected_result = 'true'
            else:
                expected_result = 'false'
        return check_errors((temp1,Error1),(temp2,Error2),expected_result)
    elif ("<=","operator") in polynom:
        for i in range(polynom.index(('<=','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('<=','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "<="')
        if str_warn == 1:
            temp1,Error1 = evaluate(list1,1)
            temp2,Error2 = evaluate(list2,1)
            temp1 = str(temp1)
            temp2 = str(temp2)
        else:
            temp1, Error1 = evaluate(list1)
            temp2, Error2 = evaluate(list2)
        expected_result = None
        if Error1 == None and Error2 == None:    
            if (type_calc(temp1) in ['string','boolean'] and type_calc(temp2) in ['string','boolean']) or (type_calc(temp1) == type_calc(temp2) == 'integer'):
                if temp1 <= temp2:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(temp1)+" <= "+type_calc(temp2)+")")
        return check_errors((temp1,Error1),(temp2,Error2),expected_result)
    elif (">=","operator") in polynom:
        for i in range(polynom.index(('>=','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('>=','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near ">="')
        if str_warn == 1:
            temp1,Error1 = evaluate(list1,1)
            temp2,Error2 = evaluate(list2,1)
            temp1 = str(temp1)
            temp2 = str(temp2)
        else:
            temp1, Error1 = evaluate(list1)
            temp2, Error2 = evaluate(list2)
        expected_result = None
        if Error1 == None and Error2 == None:    
            if (type_calc(temp1) in ['string','boolean'] and type_calc(temp2) in ['string','boolean']) or (type_calc(temp1) == type_calc(temp2) == 'integer'):
                if temp1 >= temp2:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(temp1)+" >= "+type_calc(temp2)+")")
        return check_errors((temp1,Error1),(temp2,Error2),expected_result)
    elif ("<>","operator") in polynom:
        for i in range(polynom.index(('<>','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('<>','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "<>"')
        if str_warn == 1:
            temp1,Error1 = evaluate(list1,1)
            temp2,Error2 = evaluate(list2,1)
            temp1 = str(temp1)
            temp2 = str(temp2)
        else:
            temp1, Error1 = evaluate(list1)
            temp2, Error2 = evaluate(list2)
        expected_result = None
        if Error1 == None and Error2 == None:    
            if temp1 != temp2:
                expected_result = 'true'
            else:
                expected_result = 'false'
        return check_errors((temp1,Error1),(temp2,Error2),expected_result)
    elif ("<","operator") in polynom:
        for i in range(polynom.index(('<','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('<','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "<"')
        if str_warn == 1:
            temp1,Error1 = evaluate(list1,1)
            temp2,Error2 = evaluate(list2,1)
            temp1 = str(temp1)
            temp2 = str(temp2)
        else:
            temp1, Error1 = evaluate(list1)
            temp2, Error2 = evaluate(list2)
        expected_result = None
        if Error1 == None and Error2 == None: 
            if (type_calc(temp1) in ['string','boolean'] and type_calc(temp2) in ['string','boolean']) or (type_calc(temp1) == type_calc(temp2) == 'integer'):
                if temp1 < temp2:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(temp1)+" < "+type_calc(temp2)+")")
        return check_errors((temp1,Error1),(temp2,Error2),expected_result)
    elif (">","operator") in polynom:
        for i in range(polynom.index(('>','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('>','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near ">"')
        if str_warn == 1:
            temp1,Error1 = evaluate(list1,1)
            temp2,Error2 = evaluate(list2,1)
            temp1 = str(temp1)
            temp2 = str(temp2)
        else:
            temp1, Error1 = evaluate(list1)
            temp2, Error2 = evaluate(list2)
        expected_result = None
        if Error1 == None and Error2 == None:
            if (type_calc(temp1) in ['string','boolean'] and type_calc(temp2) in ['string','boolean']) or (type_calc(temp1) == type_calc(temp2) == 'integer'):
                if temp1 > temp2:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(temp1)+" > "+type_calc(temp2)+")")
        return check_errors((temp1,Error1),(temp2,Error2),expected_result)
    elif ('+','operator') in polynom:
        for i in range(polynom.index(('+','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('+','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "+"')
        if str_warn == 1:
            temp1,Error1 = evaluate(list1,1)
            temp2,Error2 = evaluate(list2,1)
            temp1 = str(temp1)
            temp2 = str(temp2)
        else:
            temp1, Error1 = evaluate(list1)
            temp2, Error2 = evaluate(list2)
        expected_result = None
        if Error1 == None and Error2 == None:
            if type_calc(temp1) == 'string' or type_calc(temp2) == 'string':
                return (str(temp1)+str(temp2),None)
            elif type_calc(temp1) != 'integer' or type_calc(temp2) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(temp1)+" + "+type_calc(temp2)+")")
            else:
                expected_result = temp1 + temp2
        return check_errors([temp1,Error1],[temp2,Error2],expected_result)
    elif ('-','operator') in polynom:
        for i in range(polynom.index(('-','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('-','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list2 == []:
            return (None,'Error: Missing operand near "-"')
        elif list1 == []:
            
            list1.append((0,"integer"))
            return evaluate([('-1','integer'),('*','operator')]+list2)
        temp1 = evaluate(list1)
        temp2 = evaluate(list2)
        expected_result = None
        if temp1[1] == None and temp2[1] == None:
            if type_calc(temp1[0]) == 'string':
                return (temp1[0].replace(str(temp2[0]),''),None)
            elif type_calc(temp1[0]) != 'integer' or type_calc(temp2[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" - "+type_calc(temp2[0])+")")
            else:
                expected_result = temp1[0]-temp2[0]
        return check_errors(temp1,temp2,expected_result)
    elif ('/','operator') in polynom or ('*','operator') in polynom or ('%','operator') in polynom:
        index_div = index_mult = index_mod = -1
        for i in range(len(polynom)):
            if polynom[i][0] == '*':
                index_mult = i
            if polynom[i][0] == '/':
                index_div = i
            if polynom[i][0] == '%':
                index_mod = i
        if index_div < index_mult and index_mod < index_mult:
            for i in range(index_mult):
                list1.append(polynom[i])
            for i in range(index_mult+1,len(polynom)):
                list2.append(polynom[i])
            if list1 == [] or list2 == []:
                return (None,'Error: Missing operand near "*"')
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
            expected_result = None
            if type_calc(temp1[0]) != 'integer' or type_calc(temp2[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" * "+type_calc(temp2[0])+")")
            elif temp1[1] == None and temp2[1] == None:    
                expected_result = temp1[0]*temp2[0]
            return check_errors(temp1,temp2,expected_result)
        elif index_mult < index_div and index_mod < index_div:
            for i in range(index_div):
                list1.append(polynom[i])
            for i in range(index_div+1,len(polynom)):
                list2.append(polynom[i])
            if list1 == [] or list2 == []:
                return (None,'Error: Missing operand near "/"')
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
            if temp2[0] == 0 and temp2[1] is None:
                return (None,"Error: Division by zero")
            elif type_calc(temp1[0]) != 'integer' or type_calc(temp2[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" / "+type_calc(temp2[0])+")")
            else:
                expected_result = None
                if temp1[1] == None and temp2[1] == None:    
                    expected_result = temp1[0] / temp2[0]
                return check_errors(temp1,temp2,expected_result)
        else:
            for i in range(index_mod):
                list1.append(polynom[i])
            for i in range(index_mod+1,len(polynom)):
                list2.append(polynom[i])
            if list1 == [] or list2 == []:
                return (None,'Error: Missing operand near "%"')
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
            if temp2[0] == 0 and temp2[1] is None:
                return (None,"Error: Division by zero")
            elif type_calc(temp1[0]) != 'integer' or type_calc(temp2[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" % "+type_calc(temp2[0])+")")
            else:
                expected_result = None
                if temp1[1] == None and temp2[1] == None:    
                    expected_result = temp1[0] % temp2[0]
                return check_errors(temp1,temp2,expected_result)
    elif ('#','operator') in polynom:
        for i in range(polynom.index(('#','operator'))+1,len(polynom)):
            list1.append(polynom[i])
        temp1 = evaluate(list1)
        if temp1[1] == None:
            if type_calc(temp1[0]) != 'string':
                return (None,'Error: Inverter only accept string')
            else:
                return (temp1[0][::-1],None)
        else:
            return (None,temp1[1])
    elif polynom == []:
        return (0,None)
    else:
        if len(polynom) == 1:
            if polynom[0][1] in ["string","boolean"]:
                return (polynom[0][0],None)
            elif polynom[0][1]=='integer':
                if float(polynom[0][0]) == int(float(polynom[0][0])):
                    return (int(float(polynom[0][0])),None)
                else:
                    return (float(polynom[0][0]),None)
        else:
            return (None,'Error: Missing operator between "'+str(polynom[0][0])+'" and "'+str(polynom[1][0])+'"')