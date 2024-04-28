# CSC 330-100: Final Project - Banking DSL

## Team Members

- [Robert Norlander]
- [Aleksandra Salamonska]
- [Jarod Koenigsfeld]

## Project Description

Our project is a simple banking application that has the ability to withdraw, deposit, and check the balance of an account. The application will be written in a custom built language that will be compiled to Python.
The language will be a simple language that will have the ability to declare accounts, perform arithmetic operations, and print to the console. The language will be compiled to Python and the Python code will be executed to perform the banking operations.

## Project File Structure

```
.
├── examples
│   ├── groupAccounts.banking
├── src
│   ├── tests
│   │   └── test_banking.py  
│   ├── banking.py
│   └── grammar.ebnf
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── shell.py
```

## Features

- Define bank customers with first name, last name, account number, and balance.
- Perform deposit and withdrawal transactions with specified amounts.
- Generate account statements.
- Validate account numbers according to predefined rules.
- Support for error handling and exception reporting.

## Requirements

To run this program you would need to install Python on your machine. 

## How to Run the Program

1. Clone the repository
2. Install the required dependencies by running the following command in the terminal:

``` bash
# For MacOS or Linux
pip3 install -r requirements.txt

# For Windows
pip install -r requirements.txt
```

3. Run the following command in the terminal:

``` bash
# For MacOS or Linux
python3 shell.py

# For Windows
pip install -r requirements.txt
```

4. Follow the instructions in the terminal to perform banking operations.

If you want to run a file run the following command:

``` bash
# For MacOS or Linux
python3 shell.py <filepath>

# For Windows
python shell.py <filepath>
```

## Running specification tests

Make sure that you have installed all the dependencies before running specification tests.

Specification tests utilize the [PyTest](https://docs.pytest.org/en/8.1.x/index.html) framework. To run the tests run the following command:

``` bash
# For MacOS and Linux
python3 -m pytest

# For Windows
python -m pytest
```

## How to define a customer - example

``` bash
CREATE FIRSTNAME Joe LASTNAME Fritz ACCOUNT JF123456 BALANCE 2500
```

## Project Collaboration

- Communication channels: Google Meet, email, GitHub
- Code creation and testing channels: GitHub, Visual Studio
- Note Sharing channels: Google Docs
- Collaboration techniques: active discussion, brainstorming, strategic planning.

## References and Citations

- [EBNF: A Notation to Describe Syntax](https://ics.uci.edu/~pattis/misc/ebnf2.pdf)
- [Building a lexer in python — a tutorial](https://medium.com/@pythonmembers.club/building-a-lexer-in-python-a-tutorial-3b6de161fe84)
- [PyTest: helps you write better programs](https://docs.pytest.org/en/8.1.x/index.html)
- [Code Pulse: Make YOUR OWN Programming Language](https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD)
- [Git](https://git-scm.com/docs)
