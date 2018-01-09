#Importation
import functions_alt

variable_list = {}
exit = False
while exit == False:
    entry = str(input("Calc> ")) 
    if entry.lower() == 'exit': #Checking if the user want to stop
        exit = True
    else:
        list_entry, Error = functions_alt.string_to_list_type(entry) #Transformation to give a regular form
        if Error != None: #Checking if string are correctly quote
            print(Error)
        else:
            if ('=','setvariable') in list_entry: #This part is to assign (or reassign) a variable
                if list_entry.count(('=','setvariable')) > 1:
                    print("Error: Can only assigned one value at the time")
                elif list_entry[0][1] != 'variable' or list_entry[0][0] == 'exit': #Verify that the user is not assigning anything to something that shoulnd't
                    print("Error: Cannot assign value to "+list_entry[0][1])
                else:
                    error_msg = None
                    variable_content = []
                    for i in range(2,len(list_entry)): #We only store the final result, so we have to compute everything which is on the right hand side of the '='
                        if list_entry[i][1] == 'variable': #If there is a variable, we place its content in the list
                            if list_entry[i][0] in variable_list:
                                variable_content.append(variable_list[list_entry[i][0]])
                            else:
                                error_msg = 'Error: Unknown variable "'+list_entry[i][0]+'"'
                                print(error_msg) #It informs the user that he tried to set a variable using an unknonw variable
                        else:
                            variable_content.append(list_entry[i])
                    if error_msg == None: #If one variable called doesn't exist, we stop
                        temp = functions_alt.evaluate(variable_content)
                        if temp[1] != None: #Print error message relative to the part that have been compute
                            print(temp[1])
                        else:
                            variable_list[list_entry[0][0]] = (temp[0],functions_alt.type_calc(temp[0]))
            else: #This part is for calculation
                error_msg = None         
                for i in range(len(list_entry)): #This loop replaces know variable by their content and warns the user if one is unknown
                    if list_entry[i][1] == 'variable':
                            if list_entry[i][0] in variable_list:
                                list_entry[i] = variable_list[list_entry[i][0]]
                            else:
                                error_msg = 'Error: Unknown variable "'+list_entry[i][0]+'"'
                                print(error_msg)
                if error_msg == None: #If one variable called doesn't exist, we stop
                    for i in list_entry:
                        print(i[0],end=" ")
                    print("=")
                    print(functions_alt.evaluate(list_entry))
                    Result, *Error = functions_alt.evaluate(list_entry) #Result stores the result (in the first container) and Error everything else
                    if Error[0] is not None: #If there is an error, print the error
                        print(Error[0])
                    else: #Otherwise it prints the result
                        print(Result)