#-------------------------------------------------------------------------------
# Name:        SSQLT
# Purpose:     Simple SQL Tokenizer with GUI
#
# Author:      Walit
#
# Created:     30/06/2024
# Copyright:   (c) walit 2024
# Licence:     MIT License
#-------------------------------------------------------------------------------

import ply.lex as lex
import customtkinter as ctk

class SimpleSQLTokenizer:
    """
    SimpleSQLTokenizer class uses PLY to tokenize SQL statements.

    Attributes:
        tokens (list): List of token types to be recognized by the lexer.
        keywords (set): Set of SQL keywords to be recognized.
        lexer (Lexer): PLY lexer instance for tokenizing input SQL statements.

    Methods:
        t_IDENTIFIER(t): Tokenizes identifiers and keywords.
        t_INTEGER(t): Tokenizes integer literals.
        t_STRING(t): Tokenizes string literals.
        t_COMMENT(t): Ignores comments in the SQL input.
        t_newline(t): Tracks new lines in the input for accurate line numbers.
        t_error(t): Handles illegal characters in the input.
        tokenize(sql_statement): Tokenizes the input SQL statement and returns a list of tokens.
    """

    # Define tokens
    tokens = [
        'KEYWORD', 'ASTERISK', 'COMMA', 'SEMICOLON', 'EQUALS', 'LESS',
        'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL', 'INTEGER',
        'STRING', 'COMMENT', 'LPAREN', 'RPAREN', 'IDENTIFIER',
    ]

    # List of SQL keywords
    keywords = {
        'SELECT', 'UPDATE', 'CREATE', 'DROP', 'TABLE', 'ORDER', 'BY', 'FROM', 'INSERT',
        'INTO', 'VALUES', 'WHERE', 'AND', 'OR', 'JOIN', 'ON', 'NULL', 'INT', 'NOT',
        'DATETIME', 'PRIMARY', 'KEY', 'CHAR', 'IDENTITY', 'VARCHAR', 'ALTER', 'FOREIGN',
        'ADD', 'CONSTRAINT', 'UNIQUE'
    }

    # Token definitions using regular expressions for symbols
    t_ASTERISK = r'\*'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_EQUALS = r'='
    t_LESS = r'<'
    t_GREATER = r'>'
    t_LESS_EQUAL = r'<='
    t_GREATER_EQUAL = r'>='
    t_NOT_EQUAL = r'!='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    t_ignore = ' \t'  # Ignored characters

    def t_IDENTIFIER(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        token_value_upper = t.value.upper()
        if token_value_upper in self.keywords:
            t.type = 'KEYWORD'  # Assign KEYWORD token type
        else:
            t.type = 'IDENTIFIER'
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\'[^\']*\''
        t.value = t.value[1:-1]  # Remove the surrounding quotes
        return t

    def t_COMMENT(self, t):
        r'--.*'
        pass  # Ignore comments

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        """
        Handles illegal characters in the input.

        Parameters:
            t (Token): The illegal token encountered.
        """
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def __init__(self):
        """
        Initializes the SimpleSQLTokenizer with a PLY lexer instance.
        """
        self.lexer = lex.lex(module=self)

    def tokenize(self, sql_statement):
        """
        Tokenizes the input SQL statement.

        Parameters:
            sql_statement (str): The SQL statement to be tokenized.

        Returns:
            list: A list of tuples where each tuple contains a token type and its value.
        """
        self.lexer.input(sql_statement)
        tokens = []

        while True:
            token = self.lexer.token()
            if not token:
                break
            tokens.append((token.type, token.value))

        return tokens


class App:
    """
    App class provides a GUI for the SQL tokenizer using CustomTkinter.

    Attributes:
        tokenizer (SimpleSQLTokenizer): Instance of the SQL tokenizer.
        root (CTk): The main window of the application.
        sql_entry (CTkTextbox): Text area for inputting SQL statements.
        output (CTkTextbox): Text area for displaying the tokenized output.

    Methods:
        tokenize_input(): Tokenizes the SQL statement from the input text area and displays the tokens.
        clear_output(): Clears the input and output text areas.
        run(): Starts the main event loop of the application.
    """

    def __init__(self):
        """
        Initializes the App with a SimpleSQLTokenizer and sets up the GUI.
        """
        self.tokenizer = SimpleSQLTokenizer()
        self.root = ctk.CTk()
        self.root.title("Simple SQL Tokenizer")

        # SQL input text area
        sql_label = ctk.CTkLabel(self.root, text="Enter SQL statement:")
        sql_label.pack(padx=10, pady=(10, 0), anchor='w')

        self.sql_entry = ctk.CTkTextbox(self.root, height=100)
        self.sql_entry.pack(padx=10, pady=10, fill="both", expand=True)

        # Frame for buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(padx=10, pady=(5, 0), anchor='w', fill='x')

        # Tokenize button
        tokenize_button = ctk.CTkButton(button_frame, text="Tokenize", command=self.tokenize_input, height=40)
        tokenize_button.pack(side='left', padx=(0, 10), pady=5, fill='x', expand=True)

        # Clear button
        clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_output, height=40)
        clear_button.pack(side='right', pady=5, fill='x', expand=True)

        # Output text area
        output_label = ctk.CTkLabel(self.root, text="Tokens:")
        output_label.pack(padx=10, pady=(10, 0), anchor='w')

        self.output = ctk.CTkTextbox(self.root, height=200)
        self.output.pack(padx=10, pady=10, fill="both", expand=True)

    def tokenize_input(self):
        """
        Tokenizes the SQL statement from the input text area and displays the tokens in the output area.
        """
        sql = self.sql_entry.get("1.0", "end-1c")
        tokens = self.tokenizer.tokenize(sql)
        self.output.delete("1.0", ctk.END)
        for token_type, value in tokens:
            self.output.insert(ctk.END, f"{token_type}: {value}\n")

    def clear_output(self):
        """
        Clears the input and output text areas.
        """
        self.output.delete("1.0", ctk.END)
        self.sql_entry.delete("1.0", ctk.END)

    def run(self):
        self.root.mainloop()


# Start the application
if __name__ == "__main__":
    app = App()
    app.run()
