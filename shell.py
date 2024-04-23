import sys
import src.banking as banking

# Check if a file is provided as an argument
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


while True:
    text = input("banking > ")
    if text == "exit":
        break
    result = banking.run(text)
    if result:
        print(result)
    

    