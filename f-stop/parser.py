from lark import Lark

with open('grammar.lark') as grammar:
    grammar = grammar.read()
    
f_stop_parser = Lark(grammar)
text = 'OPEN "test.png" AS im'
parsed = f_stop_parser.parse(text)

print(parsed.pretty())
