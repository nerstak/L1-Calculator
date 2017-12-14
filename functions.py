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
    print('pol',poly_list)
    for i in range(len(poly_list)):
        print('gg',poly_list[i])
        if i-1 > 0:
            if poly_list[i-1][0] == '*' and poly_list[i][1] == 'integer':
                calc = calc * int(poly_list[i][0])
            elif poly_list[i-1][0] == '/' and poly_list[i][1] == 'integer':
                calc = calc / int(poly_list[i][0])
        elif poly_list[i][1] == 'integer':
            calc = calc + int(poly_list[i][0])
    print("c",calc)
    return calc
            
    

def evaluate(polynom_list):
    print('li',polynom_list)
    if polynom_list == None:
        return
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
        if list1 == [] and list3 == []:
            print(13)
            re = (string_to_list_type(str(evaluate(list2))))
        elif list1 == []:
            print(1)
            re = (string_to_list_type(str(evaluate(list2)))) + list3
        elif list3 == []:
            print(3)
            re = list1 + (string_to_list_type(str(evaluate(list2))))
        else:
            print(0)
            re = list1 + (string_to_list_type(str(evaluate(list2)))) + list3
        print('re',re)
        return (evaluate(re))

    else:
        print('v')
        if ('+','operator') in polynom_list: #RAJOUTE UN TRUC POUR PRENDRE EN COMPTE LES PARENTHESES EN PREMIER
            list1 = []
            list2 = []
            for i in range(polynom_list.index(('+','operator'))):
                list1.append(polynom_list[i])
            for i in range(polynom_list.index(('+','operator'))+1,len(polynom_list)):
                list2.append(polynom_list[i])
            print('oy',int(evaluate(list1)) + int(evaluate(list2)))
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