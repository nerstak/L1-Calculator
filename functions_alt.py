def type_calc(x):
    if x in ["/","-","+","*","==","<",">","<>","<=",">=","not","and","or"] :
        return 'operator'
    elif x == '(' or x == ')':
        return 'parenthesis'
    elif x in ["true","false"]:
        return 'boolean'
    else:
        try:
            int(x)
            return 'integer'
        except ValueError:
            return 'string'

def string_to_list_type(string):
    list = []
    i = 0
    while i < len(string):
        if 'integer' == type_calc(string[i]):
            nb = ''
            while i < len(string) and 'integer' == type_calc(string[i]):
                nb = nb + string[i]
                i+=1
            list.append((nb,type_calc(i)))
        elif string[i] == '"':
            if string.count('"') % 2 != 0:
                return "Error: missing quote"
            nb = ''
            i+=1
            while i < len(string) and string[i] != '"':
                print("s",string[i])
                nb = nb +string[i]
                i+=1
            i+=1
            list.append((nb,"string"))
        elif string[i] != " ":
            if (type_calc(string[i]) in ["operator","parenthesis"]) or string[i]== " ":
                if string[i] == "<" and string[i+1] in ["=",">"]:
                    list.append((string[i]+string[i+1],"operator"))
                    i+=2
                elif string[i] == ">" and string[i+1] == "=":
                    list.append((string[i]+string[i+1],"operator"))
                    i+=2
                else:  
                    list.append((string[i],type_calc(string[i])))
                    i+=1
            elif string[i] == '=':
                if string[i+1] == '=':
                    list.append(("==","operator"))
                    i+=2
            else:
                continu = True
                nb = ''
                while i < len(string) and (string[i] not in [" ",'"','(',')'] and type_calc(string[i]) != "operator") and continu == True:
                    nb = nb + string[i]
                    i+=1
                    if nb in ['not','or','and'] and type_calc(string[i]) not in ("integer","string"):
                        continu = False
                list.append((nb,type_calc(nb)))
        else:
            i+=1
    return list

def evaluate(polynom,str_warn=0):
    for i in polynom:
        if i[1] == "string":
            str_warn = 1
    list1 = []
    list2 = []
    list3 = []
    if ('(','parenthesis') in polynom:
        i = cpt =0
        while cpt >= 0 and i < len(polynom):
            if polynom[i][0] == '(':
                cpt +=1
            elif polynom[i][0] == ')':
                cpt -= 1
            i += 1
            if cpt < 0:
                return "Error: wrong syntax (parenthesis)"
        if cpt !=0:
            return "Error: wrong syntax (parenthesis)"
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
        temp = str(evaluate(list2))
        print('ntemp',temp)
        if temp == "Error: Division by zero":
            return temp
        else:
            temp = (string_to_list_type(temp))
            print(type(temp),temp)
            ret = list1 + temp + list3
            print('nret',ret)
            return (evaluate(ret))
    elif ('or','operator') in polynom:
        temp = len(polynom)
        for i in range(polynom.index(('or','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('or','operator'))+1,temp):
            list2.append(polynom[i])
        temp1 = evaluate(list1)
        temp2 = evaluate(list2)
        if temp1 == 'true' or temp2 == 'true' :
            return "true"
        else:
            return "false"
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
        temp1 = evaluate(list1)
        temp2 = evaluate(list2)
        if temp1 == temp2 == "true" :
            return "true"
        else:
            return "false"
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
        temp1 = evaluate(list1)
        if temp1 == "false" or 0:
            return "true"
        else:
            return "false"
    elif ("==","operator") in polynom:
        for i in range(polynom.index(('==','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('==','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if str_warn == 1:
            temp1 = str(evaluate(list1,1))
            temp2 = str(evaluate(list2,1))
        else:
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
        if temp1 == temp2:
            return 'true'
        else:
            return 'false'
    elif ("<=","operator") in polynom:
        for i in range(polynom.index(('<=','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('<=','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if str_warn == 1:
            temp1 = str(evaluate(list1,1))
            temp2 = str(evaluate(list2,1))
        else:
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
        if temp1 <= temp2:
            return 'true'
        else:
            return 'false'
    elif (">=","operator") in polynom:
        for i in range(polynom.index(('>=','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('>=','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if str_warn == 1:
            temp1 = str(evaluate(list1,1))
            temp2 = str(evaluate(list2,1))
        else:
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
        if temp1 >= temp2:
            return 'true'
        else:
            return 'false'
    elif ("<>","operator") in polynom:
        for i in range(polynom.index(('<>','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('<>','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if str_warn == 1:
            temp1 = str(evaluate(list1,1))
            temp2 = str(evaluate(list2,1))
        else:
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
        if temp1 != temp2:
            return 'true'
        else:
            return 'false'
    elif ("<","operator") in polynom:
        for i in range(polynom.index(('<','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('<','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if str_warn == 1:
            temp1 = str(evaluate(list1,1))
            temp2 = str(evaluate(list2,1))
        else:
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
        if temp1 < temp2:
            return 'true'
        else:
            return 'false'
    elif (">","operator") in polynom:
        for i in range(polynom.index(('>','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('>','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if str_warn == 1:
            temp1 = str(evaluate(list1,1))
            temp2 = str(evaluate(list2,1))
        else:
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
        if temp1 > temp2:
            return 'true'
        else:
            return 'false'
    elif ('+','operator') in polynom:
        for i in range(polynom.index(('+','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('+','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        if str_warn == 1:
            temp1 = str(evaluate(list1,1))
            temp2 = str(evaluate(list2,1))
        else:
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
        return temp1 + temp2
    elif ('-','operator') in polynom and str_warn == 0:
            for i in range(polynom.index(('-','operator'))):
                list1.append(polynom[i])
            for i in range(polynom.index(('-','operator'))+1,len(polynom)):
                list2.append(polynom[i])
            return evaluate(list1) - evaluate(list2)
    elif (('/','operator') in polynom) or (('*','operator') in polynom) and str_warn == 0:
        try:
            index_div = polynom.index(('/','operator'))
        except ValueError:
            index_div = 999
        try:
            index_mult = polynom.index(('*','operator'))
        except ValueError:
            index_mult = 999
        if index_div > index_mult:
            for i in range(index_mult):
                list1.append(polynom[i])
            for i in range(index_mult+1,len(polynom)):
                list2.append(polynom[i])
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
            if (temp1 and temp2) != "Error: Division by zero":
                return temp1 * temp2
            else:
                return "Error: Division by zero" 
        else:
            for i in range(index_div):
                list1.append(polynom[i])
            for i in range(index_div+1,len(polynom)):
                list2.append(polynom[i])
            temp1 = evaluate(list1)
            temp2 = evaluate(list2)
            print('ntemp',temp1,temp2)
            if (temp1 and temp2) != "Error: Division by zero":
                if temp2 == 0:
                    return "Error: Division by zero"
                return temp1 / temp2
            else:
                return "Error: Division by zero"
    elif polynom == []:
        return 0
    else:
        print("poly",polynom)
        if len(polynom) <= 1:
            if polynom[0][1] in ["string","boolean"]:
                return polynom[0][0]
            elif polynom[0][1]=='integer':
                return int(polynom[0][0])
        else:
            return "Error: Wrong syntax"