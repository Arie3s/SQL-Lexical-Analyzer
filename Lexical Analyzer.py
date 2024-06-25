import customtkinter as ctk
import ply.lex as lex

class Tokeniser:
    tokens = (
        'SELECT', 'UPDATE', 'CREATE', 'DROP', 'TABLE', 'ORDER', 'BY', 'FROM',
        'INSERT', 'INTO', 'VALUES', 'WHERE', 'AND', 'OR', 'JOIN', 'ON',
        'IDENTIFIER', 'NUMBER', 'STRING',
        'ASTERISK', 'COMMA', 'SEMICOLON',
        'EQUALS', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL'
    )

    t_SELECT = r'SELECT'
    t_UPDATE = r'UPDATE'
    t_CREATE = r'CREATE'
    t_DROP = r'DROP'
    t_TABLE = r'TABLE'
    t_ORDER = r'ORDER'
    t_BY = r'BY'
    t_FROM = r'FROM'
    t_INSERT = r'INSERT'
    t_INTO = r'INTO'
    t_VALUES = r'VALUES'
    t_WHERE = r'WHERE'
    t_AND = r'AND'
    t_OR = r'OR'
    t_JOIN = r'JOIN'
    t_ON = r'ON'
    t_ASTERISK = r'\*'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_EQUALS = r'='
    t_LESS = r'<'
    t_GREATER = r'>'
    t_LESS_EQUAL = r'<='
    t_GREATER_EQUAL = r'>='
    t_NOT_EQUAL = r'!='

    t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_NUMBER = r'\d+'
    t_STRING = r'\'[^\']*\''

    t_ignore = ' \t'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def input(self, sql_statement):
        self.lexer.input(sql_statement)

    def analyse(self):
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(f"{tok.type}: {tok.value}")
        return tokens

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMMENT(self, t):
        r'--.*'
        pass

    def t_MULTI_LINE_COMMENT(self, t):
        r'/\*.*?\*/'
        pass

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
        t.lexer.skip(1)


class App:

    def __init__(self):
        self.tokeniser = Tokeniser()
        self.root = ctk.CTk()
        self.root.title("SQL Tokenizer")

        # SQL input text area
        sql_label = ctk.CTkLabel(self.root, text="Enter SQL statement:")
        sql_label.pack(padx=10, pady=(10, 0))

        self.sql_entry = ctk.CTkTextbox(self.root, height=100)
        self.sql_entry.pack(padx=10, pady=10, fill="both", expand=True)

        # Tokenize button
        tokenize_button = ctk.CTkButton(self.root, text="Tokenize", command=self.tokenize_input)
        tokenize_button.pack(pady=(5, 0))

        # Clear button
        clear_button = ctk.CTkButton(self.root, text="Clear", command=self.clear_output)
        clear_button.pack(pady=(5, 10))

        # Output text area
        output_label = ctk.CTkLabel(self.root, text="Tokens:")
        output_label.pack(padx=10, pady=(10, 0))

        self.output = ctk.CTkTextbox(self.root, height=200)
        self.output.pack(padx=10, pady=10, fill="both", expand=True)

    def tokenize_input(self):
        sql = self.sql_entry.get("1.0", "end-1c")
        self.tokeniser.input(sql)
        tokens = self.tokeniser.analyse()
        self.output.delete("1.0", ctk.END)
        self.output.insert(ctk.END, "\n".join(tokens))

    def clear_output(self):
        self.output.delete("1.0", ctk.END)
        self.sql_entry.delete("1.0", ctk.END)

    def run(self):
        self.root.mainloop()

# Run the GUI
app = App()
app.run()
