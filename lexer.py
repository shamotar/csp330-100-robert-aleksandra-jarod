import re

#Jarod's lexer!
#It can actually sort unorganized sets of tokens into the correct order for the program.
#known flaw: if you add multiple types of the 'same' token (2 amounts, 2 ids etc) the most recent will overwrite the original

testString = input('This is a test string, please type something: ')
keywords = ['DEPOSIT', 'WITHDRAW']

space = " "

lex = ''

tokens = []

id_regex = "^[A-Z]{2}[0-9]{6}"

#Dollar regex should accept amounts even if dollar sign isn't present. 
#If someone wants to trade in yuan or euro they need to go to the front desk.
dollar_regex = r"(\$?\d+(?:\.\d{2})){1}"

for i,current in enumerate(testString):

        lex += current
        print(str(i+1),":",current)
        if lex in space:
                lex = ''
                print('Space found. Assuming new word.')
                
        
        if lex.upper() in keywords:
                print("I found a keyword! It is",lex,".")
                tokens.insert(0,lex.upper())
                lex = ''
                
        if re.search(id_regex, lex.upper()):
                
                print("I found an ID! It is",lex.upper(),".")
                
                #The user ID should always be capitalized.
                #This ensures that it is, even if the user types it in lowercase.
                lex = lex.upper()
                tokens.insert(1,lex)
                lex = ''
        
        if re.search(dollar_regex, lex):
                print("I found an amount! It is", lex)
                tokens.insert(2,lex)
                lex = ''
                
        if current in space and len(lex) > 1:
                print('I was unable to parse this into a keyword, ID, or amount: ',lex)
                print('We should probably stop the program here.')
                lex = ''
                
        print(lex)

print(tokens)
        
