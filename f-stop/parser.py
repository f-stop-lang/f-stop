from lark import Lark, 
grammer = open('grammar.lark').read()
f_stop_parser = Lark(grammer)
text = 'OPEN "test.png" AS im'
parsed = f_stop_parser.parse(text)
print(parsed.pretty())