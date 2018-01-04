#Importation
import functions

exit = False
while exit == False:
    entry = str(input("Calc (beta)> ")) 
    if entry.lower() == 'exit': #Checking if the user want to stop
        exit = True
    else:
        list_entry, Error = functions.string_to_list_type(entry) #Transformation to give a regular form
        if Error is not None:
            print(Error)
        else:
            print(list_entry)
            Result = functions.evaluate(list_entry)
            print(Result)
    #Important to check if list_entry won't be False

    #If there's a boolean's signs, seperate into two parts then compare