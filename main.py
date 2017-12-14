#Importation
import functions

exit = False
while exit == False:
    entry = str(input("? ")) 
    if entry.lower() == 'exit': #Checking if the user want to stop
        exit = True
    list_entry = functions.string_to_list_type(entry) #Transformation to give a regular form
    print(functions.evaluate(list_entry))
    #Important to check if list_entry won't be False