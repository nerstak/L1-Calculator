def type_calc(x):
    if x == "+" or x == "*" or x == "-" or x == "/":
        return 'operator'
    elif x == '(' or x == ')':
        return 'parenthesis'
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
            nb = ''
            i+=1
            while i < len(string) and string[i] != '"':
                nb = nb +string[i]
                i+=1
            if string.count('"') % 2 != 0:
                return "Error: missing quote"
            list.append((nb,"string"))
            i+=1        
        elif string[i] != " ":
            list.append((string[i],type_calc(string[i])))
            i+=1
        else:
            i+=1
    return list

def evaluate(polynom):
    for i in polynom:
        if i[1] == "string":
            return concatenation(polynom)
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
        list1 = []
        list2 = []
        list3 = []
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
    
    elif ('+','operator') in polynom:
        list1 = []
        list2 = []
        for i in range(polynom.index(('+','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('+','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        return evaluate(list1) + evaluate(list2)
    elif ('-','operator') in polynom:
        list1 = []
        list2 = []
        for i in range(polynom.index(('-','operator'))):
            list1.append(polynom[i])
        for i in range(polynom.index(('-','operator'))+1,len(polynom)):
            list2.append(polynom[i])
        return evaluate(list1) - evaluate(list2)
    elif (('/','operator') in polynom) or (('*','operator') in polynom):
        try:
            index_div = polynom.index(('/','operator'))
        except ValueError:
            index_div = 999
        try:
            index_mult = polynom.index(('*','operator'))
        except ValueError:
            index_mult = 999
        list1 = []
        list2 = []
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
        print(polynom)
        return int(polynom[0][0])

def concatenation(string_list):
    temp = ""
    cpt = 0
    i = 0
    while i < len(string_list):
        if string_list[i][0] == "-" or string_list[i][0] == "/" or string_list[i][0] == "*" or string_list[i][1] == "integer":
            return "Error: Wrong syntax"
        if string_list[i][1] == "parenthesis":
            del string_list[i]
        else:
            i+=1
    for i in range(len(string_list)):
        if i % 2 == 0 and string_list[i][1] == 'string':
            temp = temp + string_list[i][0]
        elif i % 2 == 1 and string_list[i][1] == 'operator' and i != len(string_list)-1:
            None
        else:
            return "Error: Wrong syntax"
    return temp