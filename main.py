from ply.lex import lex

states = (
    ('slash', 'exclusive'),
    ('paren', 'exclusive'),
)
tokens = (
    'NAME',
    'TIMES',
    'NUMBER'
)

t_NAME = r'[a-zA-Z]'
# t_ignore_COMMENT =r'[/]{1}[*]{1}[a-zA-Z0-9()*/ \n]*[*]{1}[/]{1}|[(]{1}[*]{1}[a-zA-Z0-9*/() \n]*[*]{1}[)]{1}'
t_ignore = ' '


def t_NUMBER(t):
    r'\d'
    t.value = int(t.value)
    return t


def t_ignore_newline(t):
    r'\n+'

    t.lexer.lineno += len(t.value)


def t_slash(t):
    r'[/]{1}[*]{1}'
    t.lexer.push_state('slash')


def t_paren(t):
    r'[(]{1}[*]{1}'
    t.lexer.push_state('paren')


def t_slash_again(t):
    r'[/]{1}[*]{1}'
    t.lexer.push_state('slash')


def t_slash_parenagain(t):
    r'[(]{1}[*]{1}'
    t.lexer.push_state('paren')


def t_slash_close(t):
    r'[*]{1}[/]{1}'
    if (t.lexer.current_state() == 'slash'):
        t.lexer.pop_state()
    else:
        exit('error')


def t_slash_middle(t):
    r'[a-zA-Z0-9 \n]'
    pass


# <===========================================================>
def t_paren_again(t):
    r'[(]{1}[*]{1}'
    t.lexer.push_state('paren')


def t_paren_slashagain(t):
    r'[/]{1}[*]{1}'
    t.lexer.push_state('slash')


def t_paren_close(t):
    r'[*]{1}[)]{1}'
    if (t.lexer.current_state() == 'paren'):
        t.lexer.pop_state()
    else:
        exit('error')


def t_paren_middle(t):
    r'[a-zA-Z0-9 \n]'
    pass


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex()

data = '''(* comment in /*dep
th*/*) eyo whatsup
 
 (*bye*) sa'''
lexer.input(data)
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
