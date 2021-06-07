from lark import Lark, Transformer, v_args
#from f_stop.transformer import FStopTransformer
#from f_stop.ast import Env
import PIL.Image



with open('grammar.lark') as grammar:
    grammar = grammar.read()
    
f_stop_parser = Lark.open('grammar.lark', rel_to=__file__)
text = "OPEN 'test.png' AS im"
parsed = f_stop_parser.parse(text)
print(parsed.pretty())
#x = FStopTransformer().transform(parsed).eval(Env())


