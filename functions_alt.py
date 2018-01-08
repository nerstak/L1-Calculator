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
        if 'integer' == type_calc(string[i]): #Part for numbers
            nb = ''
            cpt_point = 0
            while i < len(string) and ('integer' == type_calc(string[i]) or string[i]=='.'):
                nb = nb + string[i]
                if string[i] == '.':
                    cpt_point+=1
                    if cpt_point > 1:
                        return (None,"Error: Incorrect number")
                i+=1
            if float(nb) == int(float(nb)): #Removing '.0' for integer
                nb = int(float(nb))
            list.append((nb,type_calc(i)))
        elif string[i] == '"': #Part for string
            if string.count('"') % 2 != 0:
                return (None,"Error: Missing quote")
            nb = ''
            i+=1
            while i < len(string) and string[i] != '"':
                nb = nb +string[i]
                i+=1
            i+=1
            list.append((nb,"string"))
        elif string[i] != " ": #Part for 
            if (type_calc(string[i]) in ["operator","parenthesis"]): #Part to recognise operator composed of two other operator or parenthesis
                if string[i] == "<" and i+1<len(string) and string[i+1] in ["=",">"]:
                    list.append((string[i]+string[i+1],"operator"))
                    i+=2
                elif string[i] == ">" and i+1<len(string) and string[i+1] == "=":
                    list.append((string[i]+string[i+1],"operator"))
                    i+=2
                else:  
                    list.append((string[i],type_calc(string[i])))
                    i+=1
            elif string[i] == '=': #Part to recognise that the user is assigning a variable or just checking equality
                if i+1<len(string) and string[i+1] == '=':
                    list.append(("==","operator"))
                    i+=2
                else:
                    list.append(("=","setvariable"))
                    i+=1
            else:
                continu = True
                nb = ''
                while i < len(string) and (string[i] not in [" ",'"','(',')','='] and type_calc(string[i]) != "operator") and continu == True: #Composing a string, until a forbidden caracter
                    nb = nb + string[i]
                    i+=1
                if type_calc(nb) == 'string': #If its type is string, it means it is as variable
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

def evaluation_of_two(list1,list2,str_warn=0): #Commons lines of severals parts of the program
    if str_warn == 1:
        return evaluate(list1,1),evaluate(list2,1)
    else:
        return evaluate(list1),evaluate(list2)

def evaluate(polynom,str_warn=0): #Main part of the program
    for i in polynom: #str_warn is used for promotting any type to string
        if i[1] == "string":
            str_warn = 1
    list1 = [] #Lists used almost everywhere
    list2 = []
    list3 = []
    if ('(','parenthesis') in polynom or (')','parenthesis') in polynom: #First we compute what's inside parenthesis
        i = cpt =0
        while cpt >= 0 and i < len(polynom): #While to check the number of parenthesis
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
        while i < len(polynom) and pos_p == -1: #While-loop to determine from which left parenthesis to which right parenthesis it will compute
            if polynom[i][0] == '(':
                nbr_p += 1
            elif polynom[i][0] == ')' and nbr_p == 1: #This append only for right parenthesis corresponding to the left parenthesis from which we started
                pos_p = i
            elif polynom[i][0] == ')' and nbr_p != 1:
                nbr_p -= 1
            i += 1
        for i in range(polynom.index(('(','parenthesis'))): #List1 is for everything before parenthesis
            list1.append(polynom[i])
        for i in range(polynom.index(('(','parenthesis'))+1,pos_p): #List2 is for everything inside the parenthesis
            list2.append(polynom[i])
        for i in range(pos_p+1,len(polynom)): #List3 is for everything after parenthesis
            list3.append(polynom[i])
        temp = evaluate(list2) #Compute inside of parenthesis
        if temp[1] is not None: #If there is an error inside the parenthesis, stop everything and directly return the error
            return (None,temp[1])
        else:
            temp, Error = string_to_list_type(str(temp[0])) #Transforming the result (a string) into a list
            if temp[0][1] == 'variable': #If it is a variable, it means that it is a string that couln't have been recognised because they were no quote
                ret = list1 + [(temp[0][0],'string')] + list3
            else:
                ret = list1 + temp + list3
            return (evaluate(ret))
    elif ('or','operator') in polynom: #Less important operator precedence
        for i in range(polynom.index(('or','operator'))): #Splitting into two parts, excluding the operator concerned
            list1.append(polynom[i])
        for i in range(polynom.index(('or','operator'))+1,len(polynom)):
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
        for i in range(polynom.index(('and','operator'))): #Splitting into two parts, excluding the operator concerned
            list1.append(polynom[i])
        for i in range(polynom.index(('and','operator'))+1,len(polynom)):
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
        for i in range(polynom.index(('not','operator'))+1,len(polynom)): #Keeping only what is after the 'not'
            list1.append(polynom[i])
        if list1 == []:
            return (None,"Error: Missing operand after 'not'")
        temp1 = evaluate(list1)
        expected_result = None
        if temp1[1] == None:
            if temp1[0] in  ("false","0",0):
                expected_result = "true"
            else:
                expected_result = "false"
        return check_errors(temp1,(None,None),expected_result)
    elif ("==","operator") in polynom: 
        for i in range(polynom.index(('==','operator'))): #Splitting into two parts, excluding the operator concerned
            list1.append(polynom[i])
        for i in range(polynom.index(('==','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "=="')
        temp1,temp2 = evaluation_of_two(list1,list2,str_warn)
        expected_result = None
        if temp1[1] == None and temp2[1] == None:    
            if temp1[0] == temp2[0]:
                expected_result = 'true'
            else:
                expected_result = 'false'
        return check_errors(temp1,temp2,expected_result)
    elif ("<=","operator") in polynom:
        for i in range(polynom.index(('<=','operator'))): #Splitting into two parts, excluding the operator concerned
            list1.append(polynom[i])
        for i in range(polynom.index(('<=','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "<="')
        temp1,temp2 = evaluation_of_two(list1,list2,str_warn)
        expected_result = None
        if temp1[1] == None and temp2[1] == None:    
            if (type_calc(temp1[0]) in ['string','boolean'] and type_calc(temp2[0]) in ['string','boolean']) or (type_calc(temp1[0]) == type_calc(temp2[0]) == 'integer'):
                if temp1[0] <= temp2[0]:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" <= "+type_calc(temp2[0])+")")
        return check_errors(temp1,temp2,expected_result)
    elif (">=","operator") in polynom:
        for i in range(polynom.index(('>=','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('>=','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near ">="')
        temp1,temp2 = evaluation_of_two(list1,list2,str_warn)
        expected_result = None
        if temp1[1] == None and temp2[1] == None:    
            if (type_calc(temp1[0]) in ['string','boolean'] and type_calc(temp2[0]) in ['string','boolean']) or (type_calc(temp1[0]) == type_calc(temp2[0]) == 'integer'):
                if temp1[0] >= temp2[0]:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" >= "+type_calc(temp2[0])+")")
        return check_errors(temp1,temp2,expected_result)
    elif ("<>","operator") in polynom:
        for i in range(polynom.index(('<>','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('<>','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "<>"')
        temp1,temp2 = evaluation_of_two(list1,list2,str_warn)
        expected_result = None
        if temp1[1] == None and temp2[1] == None:    
            if temp1[0] != temp2[0]:
                expected_result = 'true'
            else:
                expected_result = 'false'
        return check_errors(temp1,temp2,expected_result)
    elif ("<","operator") in polynom:
        for i in range(polynom.index(('<','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('<','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "<"')
        temp1,temp2 = evaluation_of_two(list1,list2,str_warn)
        expected_result = None
        if temp1[1] == None and temp2[1] == None: 
            if (type_calc(temp1[0]) in ['string','boolean'] and type_calc(temp2[0]) in ['string','boolean']) or (type_calc(temp1[0]) == type_calc(temp2[0]) == 'integer'):
                if temp1[0] < temp2[0]:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" < "+type_calc(temp2[0])+")")
        return check_errors(temp1,temp2,expected_result)
    elif (">","operator") in polynom:
        for i in range(polynom.index(('>','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('>','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near ">"')
        temp1,temp2 = evaluation_of_two(list1,list2,str_warn)
        expected_result = None
        if temp1[1] == None and temp2[1] == None:
            if (type_calc(temp1[0]) in ['string','boolean'] and type_calc(temp2[0]) in ['string','boolean']) or (type_calc(temp1[0]) == type_calc(temp2[0]) == 'integer'):
                if temp1[0] > temp2[0]:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" > "+type_calc(temp2[0])+")")
        return check_errors(temp1,temp2,expected_result)
    elif ('+','operator') in polynom:
        for i in range(polynom.index(('+','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('+','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if list1 == [] or list2 == []:
            return (None,'Error: Missing operand near "+"')
        temp1,temp2 = evaluation_of_two(list1,list2,str_warn)
        expected_result = None
        if temp1[1] == None and temp2[1] == None:
            if type_calc(temp1[0]) not in ['string','integer','boolean'] or type_calc(temp2[0]) not in ['string','integer','boolean']:
                return (None,"Error: Type mismatch ("+type_calc(temp1[0])+" + "+type_calc(temp2[0])+")")
            else:
                expected_result = temp1[0] + temp2[0]
        return check_errors(temp1,temp2,expected_result)
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
        print(type_calc(temp2[0]))
        if temp1[1] == None and temp2[1] == None:
            if type(temp1[0]) == str:
                return (temp1[0].replace(str(temp2[0]),''),None)
            elif type_calc(temp1[0]) != 'integer' or type_calc(temp2[0]) != 'integer':
                print("n")
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
            if polynom[0][1] in ["string","boolean"] or str_warn == 1:
                return (str(polynom[0][0]),None)
            elif polynom[0][1]=='integer':
                if float(polynom[0][0]) == int(float(polynom[0][0])):
                    return (int(float(polynom[0][0])),None)
                else:
                    return (float(polynom[0][0]),None)
        else:
            return (None,'Error: Missing operator between "'+str(polynom[0][0])+'" and "'+str(polynom[1][0])+'"')