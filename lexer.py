import ply.lex as lex 

tokens = [
    'LIT',  
    'SEN',
    'CONJ',
    'DISJ',
    'OPENBR',
    'CLOSEBR',
    'DOT'
]

t_LIT = r'[a-zA-Z_][A-Za-z_0-9]*'
t_SEN = r'\:\-'
t_CONJ = r'\,'
t_DISJ = r'\;'
t_OPENBR = r'\('
t_CLOSEBR = r'\)'
t_DOT = r'\.'

t_ignore = ' \t'

def t_newline(t): 
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t): 
    print("Illegal character {0} at line {1} in pos {2}".format(t.value[0], t.lineno, t.lexpos))
    tokenize.lex_error = True
    t.lexer.skip(1)

def tokenize(file_name):
    input_file = open(file_name)
    lexer = lex.lex() 
    lexer.input(input_file.read()) 
    input_file.close()
    toks = []
    tokenize.lex_error = False

    while True: 
        tok = lexer.token() 
        if not tok:
            break
        toks.append(tok)

    return tokenize.lex_error, toks
