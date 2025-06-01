import json
import sys

class Manager:
    
    def __init__(self):
        self.__masterkey = "User110"  # attribute is set private, and cannot be accessed directly
        self.__file_path = r"C:\Users\Public\Downloads\password.json" # Path is set to Users\Public to make it system independent
        if not self.__authentication():
            sys.exit()
        self.passwords = self.__load_data()
        
    # Aunthentication function is set private, to safegaurd the masterkey
    def __authentication(self):
        key = input("Enter master key: ")
        if key != self.__masterkey:
            print("Incorrect Master-key, Try again...")
            return False
        return True
    
    # Saving_data function is set private to keep the file_path safe
    def __save_data(self):
        # now load the data in write mode
        with open(self.__file_path, 'w') as f:
            json.dump(self.passwords, f, indent = 4)

    # Exit function saves the updates in the data
    def exit(self):
        self.__save_data()
        print("Data saved Successfully!")
        
    # Loading function is set private, to safegaurd the file_path
    def __load_data(self):
        
        # Creates a default file(if file not present) at the given path, using append mode
        file = open(self.__file_path, 'a') 
        file.close()
        
        # now load the data in read mode
        with open(self.__file_path, 'r') as f:
            try:
                contents = json.load(f)
                return contents
            except json.JSONDecodeError:
                # If file is empty or corrupted, set into empty dictionary
                return {}

    
    # function to add new passwords
    def add_new_password(self):
        new = input("Enter website_name and password(with space in-between): ")

        try:
            website, password = new.strip().split()
            self.passwords[website.lower()] = password  # adding website names in lowercase, to avoid future errors
            print("Password added Successfully")
        except:
            print("Invalid input format, Try again...")

    # function to update passwords, if input website is present
    def update_password(self):
        web_site = input("Enter website to update: ")  # User can give input in any Case(Upper, Lower, or Mixture) 
        
        # search for the input_website in lower case 
        if web_site.lower() in self.passwords:
            new_password = input("Enter new password: ")
            self.passwords[web_site.lower()] = new_password
            print("Password updated Successfully")
        else:
            print("Website not found! Try adding a new_password")

    # function to search password for the input website
    def search_password(self):
        web_site = input("Enter website to search: ")  # User can give input in any Case(Upper, Lower, or Mixture) 
        
        # search for the input_website in lower case 
        if web_site.lower() in self.passwords:
            print(f"{web_site}: {self.passwords[web_site.lower()]}")
        else:
            print("No matching website found!")

    # function to remove input website and its password from the data
    def remove_password(self):
        web_site = input("Enter website to update: ")  # User can give input in any Case(Upper, Lower, or Mixture) 
        
        # search for the input_website in lower case 
        if web_site.lower() in self.passwords:
            del self.passwords[web_site.lower()]
            print("Password removed Successfully!")
        else:
            print("No matching website found!")

    # function to view all passwords stored
    def view_all_passwords(self):
        if not self.passwords:
            print("No passwords found!")

        for website, password in self.passwords.items():
            print(f"{website}: {password}")