#Currents functions
def type_calc(x): #This function defines the type of the variable put in. Used in string_to_list_type()
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

def check_errors(array1,array2,result): #Function to check if they are any error for some parts, and return them easily. Used in evaluate()
    if array1[1] == array2[1] == None:
        return (result,None)
    elif array1[1] != None:    
        return (None,array1[1])
    else:
        return (None,array2[1])

def evaluation_of_two(list1,list2,str_warn=0): #Promoting non-string value to string if it is asked. Used in evaluate()
    if str_warn == 1:
        return evaluate(list1,1),evaluate(list2,1)
    else:
        return evaluate(list1),evaluate(list2)

def fill_list(operator,polynom): #plit the polynom into two lists, excluding the concerned operator. Used in evaluate()
    leftPart=[]
    rightPart=[]
    for i in range(polynom.index((operator,'operator'))):
        leftPart.append(polynom[i])
    for i in range(polynom.index((operator,'operator'))+1,len(polynom)):
        rightPart.append(polynom[i])
    return leftPart,rightPart

def float_to_int(nb): #Removing the float if its null. Used in evaluate() and string_to_list_type()
    if int(float(nb))==float(nb):
        return int(float(nb))
    else:
        return float(nb)

#Processing functions
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
            nb = float_to_int(nb)
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
        elif string[i] != " ": #Part for operator, variable
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

def evaluate(polynom,str_warn=0): #Main part of the program
    for i in polynom: #str_warn is used for promotting any type to string
        if i[1] == "string":
            str_warn = 1
    if ('(','parenthesis') in polynom or (')','parenthesis') in polynom: #First we compute what's inside parenthesis
        i = cpt =0
        while cpt >= 0 and i < len(polynom): #While to check the number of parenthesis, and if they are well placed
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
        leftPart = []
        insidePart = []
        rightPart = []
        for i in range(polynom.index(('(','parenthesis'))): #leftPart is for everything before parenthesis
            leftPart.append(polynom[i])
        for i in range(polynom.index(('(','parenthesis'))+1,pos_p): #insidePart is for everything inside the parenthesis
            insidePart.append(polynom[i])
        for i in range(pos_p+1,len(polynom)): #rightPart is for everything after parenthesis
            rightPart.append(polynom[i])
        resultPart = evaluate(insidePart) #Compute inside of parenthesis
        if resultPart[1] is not None: #If there is an error inside the parenthesis, stop everything and directly return the error
            return (None,temp[1])
        else:
            listResult, Error = string_to_list_type(str(resultPart[0])) #Transforming the result ( which is a string) into a list
            if temp[0][1] == 'variable': #If it is a variable, it means that it is a string that couln't have been recognised because they were no quotation marks
                ret = leftPart + [(listResult[0][0],'string')] + rightPart
            else:
                ret = leftPart + listResult + rightPart
            return (evaluate(ret))
    elif ('or','operator') in polynom: #Less important operator precedence
        leftPart,rightPart = fill_list('or',polynom) 
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near "or"')
        resultLeft = evaluate(leftPart)
        resultRight = evaluate(rightPart)
        expected_result = None
        if resultRight[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if resultLeft[0] == 'true' or resultRight[0] == 'true' :
                expected_result = "true"
            else:
                expected_result = "false"
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ('and','operator') in polynom:
        leftPart,rightPart = fill_list('and',polynom) 
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near "and"')
        resultLeft = evaluate(leftPart)
        resultRight = evaluate(rightPart)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if resultLeft[0] == resultRight[0] == "true" :
                expected_result = "true"
            else:
                expected_result = "false"
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ('not','operator') in polynom:
        leftPart, rightPart = fill_list('not',polynom)
        resultRight = evaluate(rightPart)
        expected_result = None
        if resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if resultRight[0] in  ("false","0",0):
                return evaluate(leftPart+[("true","boolean")])
            else:
                return evaluate(leftPart+[("false","boolean")])
        else:
            return (None,resultRight[1]) #Return error message or the result
    elif ("==","operator") in polynom: 
        leftPart,rightPart = fill_list('==',polynom)
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near "=="')
        resultLeft,resultRight = evaluation_of_two(leftPart,rightPart,str_warn)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1  
            if resultLeft[0] == resultRight[0]:
                expected_result = 'true'
            else:
                expected_result = 'false'
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ("<=","operator") in polynom:
        leftPart,rightPart = fill_list('<=',polynom)
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near "<="')
        resultLeft,resultRight = evaluation_of_two(leftPart,rightPart,str_warn)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None:  #Checking if they were no errors, stored in the index 1
            if (type_calc(resultLeft[0]) in ['string','boolean'] and type_calc(resultRight[0]) in ['string','boolean']) or (type_calc(resultLeft[0]) == type_calc(resultRight[0]) == 'integer'):
                if resultLeft[0] <= resultRight[0]:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" <= "+type_calc(resultRight[0])+")")
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif (">=","operator") in polynom:
        leftPart,rightPart = fill_list('>=',polynom)
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near ">="')
        resultLeft,resultRight = evaluation_of_two(leftPart,rightPart,str_warn)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None:  #Checking if they were no errors, stored in the index 1 
            if (type_calc(resultLeft[0]) in ['string','boolean'] and type_calc(resultRight[0]) in ['string','boolean']) or (type_calc(resultLeft[0]) == type_calc(resultRight[0]) == 'integer'):
                if resultLeft[0] >= resultRight[0]:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" >= "+type_calc(resultRight[0])+")")
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ("<>","operator") in polynom:
        leftPart,rightPart = fill_list('<>',polynom)
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near "<>"')
        resultLeft,resultRight = evaluation_of_two(leftPart,rightPart,str_warn)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if resultLeft[0] != resultRight[0]:
                expected_result = 'true'
            else:
                expected_result = 'false'
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ("<","operator") in polynom:
        leftPart,rightPart = fill_list('<',polynom)
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near "<"')
        resultLeft,resultRight = evaluation_of_two(leftPart,rightPart,str_warn)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if (type_calc(resultLeft[0]) in ['string','boolean'] and type_calc(resultRight[0]) in ['string','boolean']) or (type_calc(resultLeft[0]) == type_calc(resultRight[0]) == 'integer'):
                if resultLeft[0] < resultRight[0]:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" < "+type_calc(resultRight[0])+")")
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif (">","operator") in polynom:
        leftPart,rightPart = fill_list('>',polynom)
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near ">"')
        resultLeft,resultRight = evaluation_of_two(leftPart,rightPart,str_warn)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if (type_calc(resultLeft[0]) in ['string','boolean'] and type_calc(resultRight[0]) in ['string','boolean']) or (type_calc(resultLeft[0]) == type_calc(resultRight[0]) == 'integer'):
                if resultLeft[0] > resultRight[0]:
                    expected_result = 'true'
                else:
                    expected_result = 'false'
            else:
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" > "+type_calc(resultRight[0])+")")
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ('+','operator') in polynom:
        leftPart,rightPart = fill_list('+',polynom)
        if leftPart == [] or rightPart == []:
            return (None,'Error: Missing operand near "+"')
        resultLeft,resultRight = evaluation_of_two(leftPart,rightPart,str_warn)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if str_warn == 1:
                expected_result = str(resultLeft[0])+str(resultRight[0])
            elif type_calc(resultLeft[0]) != 'integer' or type_calc(resultRight[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" + "+type_calc(resultRight[0])+")")
            else:
                expected_result = resultLeft[0] + resultRight[0]
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ('-','operator') in polynom:
        leftPart,rightPart = fill_list('-',polynom)
        resultRight = evaluate(rightPart) 
        if rightPart == [] or type_calc(resultRight[0]) != 'integer' and (leftPart == [] or leftPart[-1][1] == 'operator'):
            return (None,'Error: Missing operand near "-"')
        elif leftPart == []: #For a negative number
            return evaluate([('-1','integer'),('*','operator')]+rightPart)
        elif leftPart[-1][1] == 'operator': #For a negative number part of calculation
            return evaluate([('-','operator')]+leftPart+rightPart)
        resultLeft = evaluate(leftPart)
        expected_result = None
        if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if type(resultLeft[0]) == str: #Remove one string from another
                return (resultLeft[0].replace(str(resultRight[0]),''),None)
            elif type_calc(resultLeft[0]) != 'integer' or type_calc(resultRight[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" - "+type_calc(resultRight[0])+")")
            else:
                expected_result = resultLeft[0]-resultRight[0]
        return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ('/','operator') in polynom or ('*','operator') in polynom or ('%','operator') in polynom:
        leftPart = []
        rightPart = []
        index_div = index_mult = index_mod = -1
        for i in range(len(polynom)): #For to determine the last operator
            if polynom[i][0] == '*':
                index_mult = i
            if polynom[i][0] == '/':
                index_div = i
            if polynom[i][0] == '%':
                index_mod = i
        if index_div < index_mult and index_mod < index_mult: #The last operator will be used to split (here *)
            for i in range(index_mult): #Splitting into two lists, excluding the operator
                leftPart.append(polynom[i])
            for i in range(index_mult+1,len(polynom)):
                rightPart.append(polynom[i])
            if leftPart == [] or rightPart == []:
                return (None,'Error: Missing operand near "*"')
            resultLeft = evaluate(leftPart)
            resultRight = evaluate(rightPart)
            expected_result = None
            if type_calc(resultLeft[0]) != 'integer' or type_calc(resultRight[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" * "+type_calc(resultRight[0])+")")
            elif resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1
                expected_result = float_to_int(resultLeft[0] * resultRight[0])
            return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
        elif index_mult < index_div and index_mod < index_div: #The last operator will be used to split (here /)
            for i in range(index_div): #Splitting into two lists, excluding the operator
                leftPart.append(polynom[i])
            for i in range(index_div+1,len(polynom)):
                rightPart.append(polynom[i])
            if leftPart == [] or rightPart == []:
                return (None,'Error: Missing operand near "/"')
            resultLeft = evaluate(leftPart)
            resultRight = evaluate(rightPart)
            if resultRight[0] == 0 and resultRight[1] is None:
                return (None,"Error: Division by zero")
            elif type_calc(resultLeft[0]) != 'integer' or type_calc(resultRight[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" / "+type_calc(resultRight[0])+")")
            else:
                expected_result = None
                if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1    
                    expected_result = float_to_int(resultLeft[0] / resultRight[0])
                return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
        else: #The last operator will be used to split (here %)
            for i in range(index_mod): #Splitting into two lists, excluding the operator
                leftPart.append(polynom[i])
            for i in range(index_mod+1,len(polynom)):
                rightPart.append(polynom[i])
            if leftPart == [] or rightPart == []:
                return (None,'Error: Missing operand near "%"')
            resultLeft = evaluate(leftPart)
            resultRight = evaluate(rightPart)
            if resultRight[0] == 0 and resultRight[1] is None:
                return (None,"Error: Division by zero")
            elif type_calc(resultLeft[0]) != 'integer' or type_calc(resultRight[0]) != 'integer':
                return (None,"Error: Type mismatch ("+type_calc(resultLeft[0])+" % "+type_calc(resultRight[0])+")")
            else:
                expected_result = None
                if resultLeft[1] == None and resultRight[1] == None: #Checking if they were no errors, stored in the index 1  
                    expected_result = float_to_int(resultLeft[0] % resultRight[0])
                return check_errors(resultLeft,resultRight,expected_result) #Return error message or the result
    elif ('#','operator') in polynom: #Operator to reverse any string #Most important operator
        leftPart,rightPart = fill_list('#',polynom)
        resultRight = evaluate(rightPart)
        if resultRight[1] == None: #Checking if they were no errors, stored in the index 1
            if type_calc(resultRight[0]) != 'string':
                return (None,'Error: Inverter only accept string')
            else:
                return evaluate(leftPart+[(resultRight[0][::-1],'string')])
        else:
            return (None,resultRight[1])
    elif polynom == []: #If polynom is empty
        return (0,None)
    else:
        if len(polynom) == 1:
            if polynom[0][1] in ["string","boolean"]:
                return (polynom[0][0],None)
            elif str_warn == 1: #Promoting to string
                return (str(float_to_int(polynom[0][0])),None)
            elif polynom[0][1]=='integer': #Return number (float or integer)
                return (float_to_int(polynom[0][0]),None)
        else:
            return (None,'Error: Missing operator between "'+str(polynom[0][0])+'" and "'+str(polynom[1][0])+'"')