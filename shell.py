# =================================================================================================
#       Title:              shell.py
#       Description:        This file is the entry point of the application. It provides an 
#                           interactive shell to the user
#
#       Author(s):          Norlander, Robert       (Primary)
#                           Koenigsfeld, Jarod      (Debugging)
#                           Salamonska, Aleksandra  (Documentation)
#
#       Class:              CSC 330-100 Language Design and Implementation
#       Date:               2024-04-28
#       Version:            1.0
# =================================================================================================
import sys
import src.banking as banking

# Check if a file is provided as an argument, if yes then read the file and execute the commands
if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as file:
        for line in file:
            result = banking.run(line)
            if result:
                print(result)
    exit()

# Interactive shell
print("Welcome to the banking shell\n")
print("The following commands are available:")
print("\t- CREATE FIRSTNAME <first name> LASTNAME <last name> {BALANCE <balance>} {ACCOUNT <account number>}")
print("\t- DEPOSIT <account_number> <amount>")
print("\t- WITHDRAW <account_number> <amount>")
print("\t- BALANCE <account_number>")
print("\t- exit")

text = ""
while text != "exit":
    text = input("banking > ")
    result = banking.run(text)
    if result:
        print(result)
    

    