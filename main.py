#Importation
import functions, functions_alt

exit = False
while exit == False:
    entry = str(input("Calc (beta)> ")) 
    if entry.lower() == 'exit': #Checking if the user want to stop
        exit = True
    else:
        list_entry = functions_alt.string_to_list_type(entry) #Transformation to give a regular form
        if list_entry == "Error: missing quote":
            print(list_entry)
        else:
            print("Entry",list_entry)
            Result = functions_alt.evaluate(list_entry)
            print(Result)
    #Important to check if list_entry won't be False

    #If there's a boolean's signs, seperate into two parts then compare