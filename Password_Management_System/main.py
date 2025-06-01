from functions import Manager

def main():
    manager = Manager()  # creating an instance of the Manager class
    print("Welcome!")
    
    print("Choose an option from the below list:")
    print("1. Add password")
    print("2. Update pawword")
    print("3. Search password")
    print("4. Remove password")
    print("5. View all paswords")
    print("6. Save and Exit")
    print()
    
    while True:
        option = input("Choose from 1-6 : ")
        
        if option =='1':
            manager.add_new_password()
        elif option =='2':
            manager.update_password()
        elif option =='3':
            manager.search_password()
        elif option =='4':
            manager.remove_password()
        elif option =='5':
            manager.view_all_passwords()
        elif option =='6':
            manager.exit()
            return
        else:
            print("Invalid option!")
        print()
            
# call the main function        
main()