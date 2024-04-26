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