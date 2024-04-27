# =================================================================================================
#    Title:          Test Banking DSL
#
#    Description:    This file contains the tests for the banking DSL
#
#    Authors:        Norlander, Robert       (Primary)
#                    Koenigsfeld, Jarod      (Debugging)
#                    Salamonska, Aleksandra  (Documentation)
#
#    Class:          CSC 330-100 Language Design and Implementation
#    Date:           2024-04-28
#    Version:        1.0
# =================================================================================================

import src.banking as banking
import re

def test_create_account():
    # It should return a string with the account number
    syntax = "CREATE FIRSTNAME John LASTNAME Doe BALANCE 1000 ACCOUNT JD123456"
    assert banking.run(syntax) == "Account created: JD123456"

def test_create_account_no_balance():
    # It should return a string with the account number
    syntax = "CREATE FIRSTNAME John LASTNAME Doe ACCOUNT JD123456"
    assert banking.run(syntax) == "Account created: JD123456"

def test_create_account_no_account():
    # It should return a string with a valid account number
    syntax = "CREATE FIRSTNAME John LASTNAME Doe BALANCE 1000"
    regex_string = r"Account created: [A-Z]{2}\d{6}"
    assert re.match(regex_string, banking.run(syntax))

def test_create_account_no_balance_no_account():
    # It should return a string with a valid account number
    syntax = "CREATE FIRSTNAME John LASTNAME Doe"
    regex_string = r"Account created: [A-Z]{2}\d{6}"
    assert re.match(regex_string, banking.run(syntax))

def test_create_account_and_deposit():
    # It should return a string with the account number
    syntax = "CREATE FIRSTNAME John LASTNAME Doe BALANCE 1000 ACCOUNT JD123456"
    assert banking.run(syntax) == "Account created: JD123456"
    syntax = "DEPOSIT JD123456 1000"
    assert banking.run(syntax) == "Deposit of $1000 into account JD123456 successful"


# Feel free to add more tests for WITHDRAW and BALANCE commands...

def test_invalid_syntax_error():
    # If someone asks the program to do something silly, the program shouldn't entertain them by trying to comply.
    syntax = "CREATE FIRSTNAME John LASTNAME Doe BALANCE 1000 ACCOUNT JD123456"
    assert banking.run(syntax) == "Account created: JD123456"
    syntax = "FUNGALINFECTION JD123456 1000"
    output = banking.run(syntax)
    assert isinstance(output, banking.InvalidSyntaxError)
    
def test_illegal_char_error():
    # If someone passes a garbled command, the program shouldn't try to do anything with it.
    syntax = "CREATE FIRSTNAME John LASTNAME Doe BALANCE 1000 ACCOUNT JD123456"
    assert banking.run(syntax) == "Account created: JD123456"
    syntax = "%EPOSIT JD123456 1000"
    output = banking.run(syntax)
    assert isinstance(output, banking.IllegalCharError)
    
def test_illegal_char_error_negatives():
    # When I was a little kid I tried this in my parents' bank account to give them a billion dollars. It didn't work then, shouldn't now.
    syntax = "CREATE FIRSTNAME John LASTNAME Doe BALANCE 1000 ACCOUNT JD123456"
    assert banking.run(syntax) == "Account created: JD123456"
    syntax = "WITHDRAW JD123456 -1000"
    output = banking.run(syntax)
    assert isinstance(output, banking.IllegalCharError)
    
def test_illegal_char_error_in_deposit():
    # If someone adds more than one decimal point, the program shouldn't lose it.
    syntax = "CREATE FIRSTNAME John LASTNAME Doe BALANCE 1000 ACCOUNT JD123456"
    assert banking.run(syntax) == "Account created: JD123456"
    syntax = "DEPOSIT JD123456 1.0350.00"
    output = banking.run(syntax)
    assert isinstance(output, banking.IllegalCharError)    