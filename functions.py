import re
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

def string_to_list_type(string): #Count number of parenthesis
    list = []
    i = 0
    while i < len(string):
        if 'integer' == type_calc(string[i]):
            nb = ''
            while i < len(string) and 'integer' == type_calc(string[i]):
                nb = nb + string[i]
                i+=1
            list.append((nb,type_calc(i)))
        elif string[i] != " ":
            list.append((string[i],type_calc(string[i])))
            i+=1
        else:
            i+=1
    return list

def calculation(poly_list):
    calc = 0
    for i in range(len(poly_list)):
        print('npolynom',poly_list[i])
        if i-1 > 0:
            if poly_list[i-1][0] == '*' and poly_list[i][1] == 'integer':
                calc = calc * int(poly_list[i][0])
            elif poly_list[i-1][0] == '/' and poly_list[i][1] == 'integer':
                try:
                    calc = calc / int(poly_list[i][0])
                except ZeroDivisionError:
                    return "Division by zero not allowed"
        elif poly_list[i][1] == 'integer':
            calc = calc + int(poly_list[i][0])
    print("ncalcu",calc)
    return calc
            

def evaluate(polynom_list):
    temp=[]
    for i in range(len(polynom_list)):
        temp.append(polynom_list[i][0])
    print('ntemporaire',temp)
    temp = ''.join(temp)
    print('ntemporore',temp)
    if re.search(r"/\)*\(*0",temp) is not None: #Regular expression
        return 'Division by zero not allowed'
    print('nlist',polynom_list)
    if type(polynom_list) == type(''):
        return polynom_list
    i = cpt =0
    while cpt >= 0 and i < len(temp):
        if temp[i] == '(':
            cpt +=1
        elif temp[i] == ')':
            cpt -= 1
        i += 1
    if cpt < 0:
        return "Input incorrect (parenthesis)"  
    if polynom_list == None:
        return None
    elif ('(','parenthesis') in polynom_list:
        nbr_p = i = 0
        pos_p = -1
        while i < len(polynom_list) and pos_p == -1:
            if polynom_list[i][0] == '(':
                nbr_p += 1
            elif polynom_list[i][0] == ')' and nbr_p == 1:
                pos_p = i
            elif polynom_list[i][0] == ')' and nbr_p != 1:
                nbr_p -= 1
            i += 1
        list1 = []
        list2 = []
        list3 = []
        for i in range(polynom_list.index(('(','parenthesis'))):
            list1.append(polynom_list[i])
        for i in range(polynom_list.index(('(','parenthesis'))+1,pos_p):
            list2.append(polynom_list[i])
        for i in range(pos_p+1,len(polynom_list)):
            list3.append(polynom_list[i])
        temp = str(evaluate(list2))
        if temp == 'Division by zero not allowed':
            return temp
        else:
            ret = list1 + (string_to_list_type(temp)) + list3
            print('nret',ret)
            return (evaluate(ret))

    else:
        print('noperator')
        if ('+','operator') in polynom_list: #RAJOUTE UN TRUC POUR PRENDRE EN COMPTE LES PARENTHESES EN PREMIER
            list1 = []
            list2 = []
            for i in range(polynom_list.index(('+','operator'))):
                list1.append(polynom_list[i])
            for i in range(polynom_list.index(('+','operator'))+1,len(polynom_list)):
                list2.append(polynom_list[i])
            return evaluate(list1) + evaluate(list2)
        elif ('-','operator') in polynom_list:
            list1 = []
            list2 = []
            for i in range(polynom_list.index(('-','operator'))):
                list1.append(polynom_list[i])
            for i in range(polynom_list.index(('-','operator'))+1,len(polynom_list)):
                list2.append(polynom_list[i])
            return evaluate(list1) - evaluate(list2)
        else:
            return (calculation(polynom_list))

# def identify_string(string_in_list):
#     i = nbr_s = 0
#     while i<len(string_in_list):
#         if string_in_list[i][1] == 'string':
#             nbr_s+=1
#         i+=1
#     if nbr_s==len(string_in_list):
#         return True