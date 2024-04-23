import src.banking as banking

print("Welcome to the banking shell")


while True:
    text = input("banking > ")
    if text == "exit":
        break
    result = banking.run(text)
    if result:
        print(result)
    

    