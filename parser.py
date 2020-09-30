from lexer import tokenize
import sys

"""
    Grammar:
    
    SEN -> LIT :- CONJ. | LIT.
    DISJ -> CONJ ; DISJ | CONJ
    CONJ -> LIT , CONJ | LIT
    LIT -> [a-zA-Z_][A-Za-z_0-9]* | (DISJ)

"""

class Node:
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name

    def pr(node):
        a = "("
        if node.left != None:
            a += node.left.pr()
        a += " " + node.name + " "
        if node.right != None:
            a += node.right.pr()
        a+=')'
        return a

class Parser:
    def __init__(self, tokens, pos):
        self.toks = tokens
        self.current = pos

    def accept(self, token_type):
        if self.toks[self.current].type == token_type:
            self.current += 1
            return True
        return False

    def expect(self, token_type):
        t = self.toks[self.current]
        if t.type == token_type:
            self.current += 1
            return True
        print("Unexpected character: {0} at line {1} pos {2} instead of {3}".format(t.type, t.lineno, t.lexpos, token_type))
        return False

    def sen(self):
        try:
            l = self.toks[self.current]
            self.current += 1
            if l.type == 'LIT':
                if self.accept('SEN'):
                    r = self.disj()
                    if r == None:
                        return None, -1
                    if self.expect('DOT'):
                        return Node(Node(None, None, l.value), r, 'def'), self.current
                    return None, -1
                if self.expect('DOT'):
                    return Node(None, None, l.value), self.current
            return None, -1
        except IndexError:
            return None, -1

    def lit(self):
        if self.accept('OPENBR'):
            r = self.disj()
            if self.expect('CLOSEBR'):
                return r
            return None
        l = self.toks[self.current]
        self.current += 1
        if l.type != 'LIT':
            return None
        return Node(None, None, l.value)

    def conj(self):
        l = self.lit()
        if self.accept('CONJ'):
            r = self.conj()
            if r == None:
                return None
            return Node(l, r, "and")
        return l

    def disj(self):
        l = self.conj()
        if self.accept('DISJ'):
            r = self.disj()
            if r == None:
                return None
            return Node(l, r, "or")
        return l


def parse(file_name):
    lex_error, tokens = tokenize(file_name)
    if not lex_error:
        if len(tokens) == 0:
            print("The program is correct")
            return True
        pos = 0
        while pos < len(tokens):
            p = Parser(tokens, pos)
            tree, pos = p.sen()
            if tree == None:
                print("Can't parse program")
                return False
        print("The program is correct")
        return True
    print("Can't lex program")
    return False

if __name__ == "__main__":
    parse(sys.argv[1])
