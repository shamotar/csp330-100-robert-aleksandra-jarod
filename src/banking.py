# =================================================================================================
#    Title:          Banking DSL
#
#    Description:    This module is used to create a simple banking system that allows
#                    users to create accounts, deposit money, withdraw money, and check
#                    their balance.
#
#    Authors:        Norlander, Robert       (Primary)
#                    Koenigsfeld, Jarod      (Debugging)
#                    Salamonska, Aleksandra  (Documentation)
#
#    Class:          CSC 330-100 Language Design and Implementation
#    Date:           2024-04-28
#    Version:        1.0
# =================================================================================================

import re
import os
from enum import Enum
import random
from dotenv import load_dotenv

load_dotenv()

# =================================================================================================
#    ERRORS
#
#    The error classes are used to represent different types
#    of errors that can occur during the lexing and parsing process.
#
#    @param error_name: The name of the error
#    @param details: The details of the error
# =================================================================================================
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def __str__(self):
        return f"EXCEPTION! -- {self.error_name}: {self.details}"

# =================================================================================================
#    IllegalCharError is raised when an illegal character is found
#
#    @param details: The details of the error
# =================================================================================================
class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__("Illegal Character", details)

# =================================================================================================
#    InvalidSyntaxError is raised when an invalid syntax is found
#
#    @param details: The details of the error
# =================================================================================================
class InvalidSyntaxError(Error):
    def __init__(self, details):
        super().__init__("Invalid Syntax", details)



# =================================================================================================
#    TYPES and CONSTANTS
#
#    The TokenType class is used to represent the different types
#    of tokens that can be found in the source code. Various constants
#    are defined as specified per EBNF grammar.
# =================================================================================================
class TokenType(Enum):
    TT_STR = "TT_STR"
    TT_INT = "TT_INT"
    TT_FLOAT = "TT_FLOAT"
    TT_EOF = "TT_EOF"
    TT_KEYWORD = "TT_KEYWORD"


WHITESPACE = " \t\n\r"
LETTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGIT = "0123456789"
DECIMAL_POINT = "."
KEYWORDS = [
    "DEPOSIT",
    "WITHDRAW",
    "BALANCE",
    "CREATE",
    "FIRSTNAME",
    "LASTNAME",
    "ACCOUNT",
]
ACCOUNT_NUMBER_FORMAT = "^[A-Z]{2}[0-9]{6}"

# =================================================================================================
#    TOKEN
#
#    The Token class is used to represent a token in the source code.
#    A token consists of a type and a value.
#
#    @param type: The type of the token
#    @param value: The value of the token
# =================================================================================================
class Token:
    def __init__(self, type: TokenType, value: any):
        self.type: TokenType = type
        self.value = value

    def __str__(self):
        return f"Token({self.type.value}, '{self.value}')"

    def __repr__(self):
        return self.__str__()

# =================================================================================================
#    LEXER
#
#    The Lexer class is used to tokenize the source code.
#    It reads the source code character by character and
#    creates tokens based on the characters it reads.
#
#    @param source: The source code to tokenize
# =================================================================================================
class Lexer:
    def __init__(self, source):
        self.source = source
        self.current_char = None
        self.index = -1
        self.tokens = []

    # Advance the index and set the current character
    def advance(self):
        self.index += 1
        if self.index < len(self.source):
            self.current_char = self.source[self.index]
        else:
            self.current_char = None

    # Tokenize the source code
    # @return: The tokens and an error if one occurred
    def lex(self) -> tuple[list[Token], Error]:
        self.advance()
        while self.index < len(self.source):
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char in LETTER:
                token, error = self.lex_word()
                if error:
                    return [], error
                self.tokens.append(token)
            elif self.current_char in DIGIT + DECIMAL_POINT:
                token, error = self.lex_number()
                if error:
                    return [], error
                self.tokens.append(token)
            else:
                return [], IllegalCharError(self.current_char)
            self.advance()

        return self.tokens, None

    # Tokenize a word
    # @return: The word token and an error if one occurred
    def lex_word(self) -> tuple[Token, Error]:
        word = ""
        while self.current_char is not None and self.current_char not in WHITESPACE:
            word += self.current_char
            self.advance()
        if word in KEYWORDS:
            return Token(TokenType.TT_KEYWORD, word), None
        return Token(TokenType.TT_STR, word), None

    # Tokenize a number
    # @return: The number token and an error if one occurred
    def lex_number(self) -> tuple[Token, Error]:
        number = ""
        decimal_count = 0
        while (
            self.current_char is not None
            and self.current_char not in WHITESPACE
            and self.current_char in DIGIT + DECIMAL_POINT
        ):
            if self.current_char == DECIMAL_POINT:
                decimal_count += 1
                if decimal_count > 1:
                    return InvalidSyntaxError("More than one decimal point in number")
            number += self.current_char
            self.advance()
        if "." in number:
            return Token(TokenType.TT_FLOAT, float(number)), None
        else:
            return Token(TokenType.TT_INT, int(number)), None

# =================================================================================================
#    NODES (AST)
#
#    The Node class is used to represent the different types of nodes
#    that can be found in the Abstract Syntax Tree (AST).
# =================================================================================================
class Node:
    pass

# =================================================================================================
#    CREATE NODE
#
#    The CreateNode class is used to represent the CREATE keyword in the source code.
#    It is used to create a new account.
#
#    @param firstname: The first name of the account holder
#    @param lastname: The last name of the account holder
#    @param balance: The initial balance of the account
#    @param account_identifier: The account identifier of the account
# =================================================================================================
class CreateNode(Node):
    def __init__(
        self,
        firstname,
        lastname,
        balance=Token(TokenType.TT_INT, 0),
        account_identifier=None,
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.account_identifier = account_identifier
        if not account_identifier:
            self.account_identifier = self.build_account_identifier()
        self.balance = balance

    # Generate a random account number if not provided
    # @return: The account identifier
    def build_account_identifier(self):
        # First letter of the first name and first letter of the last name and 6 random digits
        return Token(
            TokenType.TT_STR,
            self.firstname.value[0]
            + self.lastname.value[0]
            + str(random.randint(100000, 999999)),
        )

    def __repr__(self):
        return (
            f"CreateNode({self.firstname}, {self.lastname}, {self.account_identifier})"
        )

# =================================================================================================
#    DEPOSIT NODE
#
#    The DepositNode class is used to represent the DEPOSIT keyword in the source code.
#    It is used to deposit money into an account.
#
#    @param account_identifier: The account identifier to deposit money into
#    @param amount: The amount to deposit
# =================================================================================================
class DepositNode(Node):
    def __init__(self, account_identifier, amount):
        self.account_identifier = account_identifier
        self.amount = amount

    def __repr__(self):
        return f"DepositNode({self.account_identifier}, {self.amount})"

# =================================================================================================
#   WITHDRAW NODE
#
#   The WithdrawNode class is used to represent the WITHDRAW keyword in the source code.
#   It is used to withdraw money from an account.
#
#   @param account_identifier: The account identifier to withdraw money from
#   @param amount: The amount to withdraw
# =================================================================================================
class WithdrawNode(Node):
    def __init__(self, account_identifier, amount):
        self.account_identifier = account_identifier
        self.amount = amount

    def __repr__(self):
        return f"WithdrawNode({self.account_identifier}, {self.amount})"

# =================================================================================================
#   BALANCE NODE
#
#   The BalanceNode class is used to represent the BALANCE keyword in the source code. 
#   It is used to check the balance of an account.
#
#   @param account_identifier: The account identifier to check the balance of
# =================================================================================================
class BalanceNode(Node):
    def __init__(self, account_identifier):
        self.account_identifier = account_identifier

    def __repr__(self):
        return f"BalanceNode({self.account_identifier})"

# =================================================================================================
#   PARSER
#
#   The Parser class is used to parse the tokens and build the AST.
# =================================================================================================
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1

    # Advance the index and set the current token
    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    # Parse the tokens
    # @return: The AST and an InvalidSyntaxError if one occurred
    def parse(self):
        statements = []
        self.advance()
        while self.current_token is not None:
            statement = self.parse_statement()
            if type(statement) == InvalidSyntaxError:
                return [], statement
            statements.append(statement)
            self.advance()
        return statements, None

    # Parse a statement
    # @return: A statement node or an InvalidSyntaxError
    def parse_statement(self):
        if self.current_token.type == TokenType.TT_KEYWORD:
            if self.current_token.value == "CREATE":
                return self.parse_create()
            elif self.current_token.value == "DEPOSIT":
                return self.parse_deposit()
            elif self.current_token.value == "WITHDRAW":
                return self.parse_withdraw()
            elif self.current_token.value == "BALANCE":
                return self.parse_balance()
        return InvalidSyntaxError(
            "Expected keyword CREATE, DEPOSIT, WITHDRAW, or BALANCE"
        )

    # Parse a DEPOSIT statement
    # @return: The DEPOSIT node
    def parse_deposit(self):
        self.advance()
        if self.current_token is None or self.current_token.type != TokenType.TT_STR:
            return InvalidSyntaxError("Expected a string")
        account_identifier = self.current_token

        self.advance()
        if self.current_token is None and (
            self.current_token.type != TokenType.TT_FLOAT
            or self.current_token.type != TokenType.TT_INT
        ):
            return InvalidSyntaxError("Expected a number")
        amount = self.current_token
        return DepositNode(account_identifier, amount)

    # Parse a WITHDRAW statement
    # @return: The WITHDRAW node
    def parse_withdraw(self):
        self.advance()
        if self.current_token is None or self.current_token.type != TokenType.TT_STR:
            return InvalidSyntaxError("Expected a string")
        account_identifier = self.current_token

        self.advance()
        if self.current_token is None and (
            self.current_token.type != TokenType.TT_FLOAT
            or self.current_token.type != TokenType.TT_INT
        ):
            return InvalidSyntaxError("Expected a number")
        amount = self.current_token
        return WithdrawNode(account_identifier, amount)

    # Parse a BALANCE statement
    # @return: The BALANCE node
    def parse_balance(self):
        self.advance()
        if self.current_token.type == TokenType.TT_STR:
            account_identifier = self.current_token
        else:
            return InvalidSyntaxError("Expected a string")
        # Validate the account number format
        if not re.match(ACCOUNT_NUMBER_FORMAT, account_identifier.value):
            return InvalidSyntaxError("Invalid account number format. Should be XX123456")

        return BalanceNode(account_identifier)

    # Parse a CREATE statement
    # @return: The CREATE node
    def parse_create(self):
        # Check if the next token is the keyword FIRSTNAME
        self.advance()
        if self.current_token is None or (
            self.current_token.type != TokenType.TT_KEYWORD
            and self.current_token.value != "FIRSTNAME"
        ):
            return InvalidSyntaxError("Expected keyword FIRSTNAME")
        self.advance()

        # Check if the next token is a string, this will represent the first name
        if self.current_token is None and self.current_token.type == TokenType.TT_STR:
            return InvalidSyntaxError("Expected a string")
        first_name = self.current_token
        self.advance()

        # Check if the next token is the keyword LASTNAME
        if self.current_token is None or (
            self.current_token.type != TokenType.TT_KEYWORD
            and self.current_token.value != "LASTNAME"
        ):
            return InvalidSyntaxError("Expected the keyword LASTNAME")
        self.advance()

        # Check if the next token is a string, this will represent the last name
        if self.current_token is None and self.current_token.type == TokenType.TT_STR:
            return InvalidSyntaxError("Expected a string")
        last_name = self.current_token

        # Check for optional keywords BALANCE and ACCOUNT
        balance = Token(TokenType.TT_INT, 0)
        account_identifier = None

        self.advance()
        while self.current_token is not None:
            if self.current_token.type == TokenType.TT_KEYWORD:
                # Should be either BALANCE or ACCOUNT
                if self.current_token.value == "BALANCE":
                    # Check if the next token is a number, return SyntaxError if not
                    self.advance()
                    if (
                        self.current_token.type == TokenType.TT_INT
                        or self.current_token.type == TokenType.TT_FLOAT
                    ):
                        balance = self.current_token
                    else:
                        return InvalidSyntaxError("Expected a number")
                elif self.current_token.value == "ACCOUNT":
                    # Check if the next token is a string, return SyntaxError if not
                    self.advance()
                    if self.current_token.type == TokenType.TT_STR:
                        # Check if the account number is in the correct format
                        if re.match(ACCOUNT_NUMBER_FORMAT, self.current_token.value):
                            account_identifier = self.current_token
                        else:
                            return InvalidSyntaxError("Invalid account number format")
                    else:
                        return InvalidSyntaxError("Expected a string")

            self.advance()

        return CreateNode(first_name, last_name, balance, account_identifier)

# =================================================================================================
#    ACCOUNT TABLE
#
#    The AccountTable class is used to store the accounts created by the user.
# =================================================================================================
class AccountTable:
    def __init__(self):
        self.accounts = {}

    # Add an account to the account table
    # @param account: The account to add
    # @return: The account that was added
    def add_account(self, account):
        result = self.get_account(account.account_identifier.value)
        if not result:
            self.accounts[account.account_identifier.value] = account
            return account

        return "Account already exists... picking a new account number"

    # Get an account from the account table
    # @param account_identifier: The account identifier to search for
    # @return: The account if it exists, otherwise None
    def get_account(self, account_identifier):
        if account_identifier in self.accounts:
            return self.accounts[account_identifier]
        else:
            return None

# =================================================================================================
#   INTERPRETER
#
#   The Interpreter class is used to interpret the AST and execute the commands.
#
#   @param account_table: The account table to use
# =================================================================================================
class Interpreter:
    def __init__(self, account_table):
        self.account_table = account_table

    # Interpret the AST
    # @param statements: Array of statements to interpret
    def interpret(self, statements):
        for statement in statements:
            return self.visit(statement)

    # Visit a node
    # @param node: The node to visit
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)

    # Visit a CREATE node and add the account to the account table
    # @param node: The CREATE node\
    # @return: A string indicating the result of the account creation
    def visit_CreateNode(self, node) -> str:
        self.account_table.add_account(node)
        return f"Account created: {node.account_identifier.value}" 

    # Visit a DEPOSIT node and update the account balance
    # @param node: The DEPOSIT node
    # @return: A string indicating the result of the deposit
    def visit_DepositNode(self, node: DepositNode) -> str:
        account = self.account_table.get_account(node.account_identifier.value)
        if account:
            account.balance.value += node.amount.value
            return f"Deposit of ${node.amount.value} into account {node.account_identifier.value} successful"
        return "Account not found"

    # Visit a WITHDRAW node and update the account balance
    # @param node: The WITHDRAW node
    # @return: A string indicating the result of the withdrawal
    def visit_WithdrawNode(self, node: WithdrawNode) -> str:
        account = self.account_table.get_account(node.account_identifier.value)
        if account:
            if account.balance.value < node.amount.value:
                return f"Insufficient funds in account {node.account_identifier.value}"
            else:
                account.balance.value -= node.amount.value
                return f"Withdrawal of ${node.amount.value} from account {node.account_identifier.value} successful"
        else:
            return "Account not found"

    # Visit a BALANCE node and print the account balance
    # @param node: The BALANCE node
    # @return: A string indicating the account balance
    def visit_BalanceNode(self, node: BalanceNode) -> str:
        account = self.account_table.get_account(node.account_identifier.value)
        if account:
            return f"Balance for account {node.account_identifier.value}: ${account.balance.value}"
        else:
            return "Account not found"

# Initialize the global account table
global_account_table = AccountTable()

# =================================================================================================
#    RUN
#
#    The run function is used to run the banking system.
#    @param stream: The source code to run
# =================================================================================================
def run(stream):
    # Initialize the lexer
    lexer = Lexer(stream)

    # Tokenize the source code
    tokens, error = lexer.lex()

    # Return an error if one occurred
    if error:
        return error
    if os.getenv("DEBUG") == "1":
        print(tokens)

    # Initialize the parser
    parser = Parser(tokens)

    # Parse the tokens and build the AST
    ast, error = parser.parse()

    # Return an error if one occurred
    if error:
        return error
    if os.getenv("DEBUG") == "1":
        print(ast)

    # Initialize the interpreter
    interpreter = Interpreter(global_account_table)

    # Interpret the AST and execute the commands
    result = interpreter.interpret(ast)
    return result
