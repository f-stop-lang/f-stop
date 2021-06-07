from lark import Lark, Transformer, v_args
from PIL import Image

from .transformer import FStopTransformer
from .fast import Env

if __name__ == '__main__':
    with open('grammar.lark') as grammar:
        grammar = grammar.read()
    
    f_stop_parser = Lark.open('grammar.lark', rel_to=__file__)
    text = "OPEN 'test.png' AS im"
    parsed = f_stop_parser.parse(text)
    print(parsed.pretty())
    x = FStopTransformer().transform(parsed).eval(Env())

