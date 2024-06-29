import ply.lex as lex
import customtkinter as ctk

class SimpleSQLTokenizer:
    # Define tokens
    tokens = [
        'SELECT', 'UPDATE', 'CREATE', 'DROP', 'TABLE', 'ORDER', 'BY', 'FROM', 'INSERT',
        'INTO', 'VALUES', 'WHERE', 'AND', 'OR', 'JOIN', 'ON', 'ASTERISK', 'COMMA',
        'SEMICOLON', 'EQUALS', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL',
        'NOT_EQUAL', 'NUMBER', 'STRING', 'COMMENT', 'LPAREN', 'RPAREN',
        'NULL', 'INT', 'NOT', 'DATETIME', 'PRIMARY', 'KEY', 'CHAR', 'IDENTITY',
        'VARCHAR', 'ALTER', 'FOREIGN', 'ADD', 'CONSTRAINT', 'UNIQUE', 'IDENTIFIER'
    ]

    # Token definitions using regular expressions
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
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NULL = r'NULL'
    t_INT = r'INT'
    t_NOT = r'NOT'
    t_DATETIME = r'DATETIME'
    t_PRIMARY = r'PRIMARY'
    t_KEY = r'KEY'
    t_CHAR = r'CHAR'
    t_IDENTITY = r'IDENTITY'
    t_VARCHAR = r'VARCHAR'
    t_ALTER = r'ALTER'
    t_FOREIGN = r'FOREIGN'
    t_ADD = r'ADD'
    t_CONSTRAINT = r'CONSTRAINT'
    t_UNIQUE = r'UNIQUE'

    # Regular expression rules for complex tokens
    t_ignore = ' \t'  # Ignored characters (spaces and tabs)

    def t_IDENTIFIER(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        if t.value.upper() in self.tokens_map:
            t.type = self.tokens_map[t.value.upper()]
        else:
            t.type = 'IDENTIFIER'
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\'[^\']*\''
        t.value = t.value[1:-1]  # Remove quotes
        return t

    def t_COMMENT(self, t):
        r'--.*'
        pass  # Ignore comments

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    tokens_map = {
        'SELECT': 'SELECT',
        'UPDATE': 'UPDATE',
        'CREATE': 'CREATE',
        'DROP': 'DROP',
        'TABLE': 'TABLE',
        'ORDER': 'ORDER',
        'BY': 'BY',
        'FROM': 'FROM',
        'INSERT': 'INSERT',
        'INTO': 'INTO',
        'VALUES': 'VALUES',
        'WHERE': 'WHERE',
        'AND': 'AND',
        'OR': 'OR',
        'JOIN': 'JOIN',
        'ON': 'ON',
        '*': 'ASTERISK',
        ',': 'COMMA',
        ';': 'SEMICOLON',
        '=': 'EQUALS',
        '<': 'LESS',
        '>': 'GREATER',
        '<=': 'LESS_EQUAL',
        '>=': 'GREATER_EQUAL',
        '!=': 'NOT_EQUAL',
        'NULL': 'NULL',
        'INT': 'INT',
        'NOT': 'NOT',
        'DATETIME': 'DATETIME',
        'PRIMARY': 'PRIMARY',
        'KEY': 'KEY',
        'CHAR': 'CHAR',
        'IDENTITY': 'IDENTITY',
        'VARCHAR': 'VARCHAR',
        'ALTER': 'ALTER',
        'FOREIGN': 'FOREIGN',
        'ADD': 'ADD',
        'CONSTRAINT': 'CONSTRAINT',
        'UNIQUE': 'UNIQUE'
    }

    def __init__(self):
        # Build the lexer
        self.lexer = lex.lex(module=self)

    def tokenize(self, sql_statement):
        # Tokenize the SQL statement
        self.lexer.input(sql_statement)
        tokens = []

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append((tok.type, tok.value))

        return tokens


class App:
    def __init__(self):
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
        button_frame.pack(padx=10, pady=(5, 0), anchor='w',fill='x')

        # Tokenize button
        tokenize_button = ctk.CTkButton(button_frame, text="Tokenize", command=self.tokenize_input,height=40)
        tokenize_button.pack(side='left', padx=(0, 10), pady=5,fill='x',expand='true')

        # Clear button
        clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_output,height=40)
        clear_button.pack(side='right', pady=5,fill='x',expand='true')

        # Output text area
        output_label = ctk.CTkLabel(self.root, text="Tokens:")
        output_label.pack(padx=10, pady=(10, 0), anchor='w')

        self.output = ctk.CTkTextbox(self.root, height=200)
        self.output.pack(padx=10, pady=10, fill="both", expand=True)

    def tokenize_input(self):
        sql = self.sql_entry.get("1.0", "end-1c")
        tokens = self.tokenizer.tokenize(sql)
        self.output.delete("1.0", ctk.END)
        for token_type, value in tokens:
            self.output.insert(ctk.END, f"{token_type}: {value}\n")

    def clear_output(self):
        self.output.delete("1.0", ctk.END)
        self.sql_entry.delete("1.0", ctk.END)

    def run(self):
        self.root.mainloop()

# Run the GUI
app = App()
app.run()
