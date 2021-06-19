from f_stop.transformer import FStopTransformer
from f_stop.fast import Env
from lark import Lark

print(__name__)


if __name__ == '__main__':
    with open('test.ft') as ft:
        text = ft.read()
    f_stop_parser = Lark.open(
        '../f_stop/grammar.lark', rel_to=__file__, parser='lalr'
    )
    print(f_stop_parser)
    parsed = f_stop_parser.parse(text)
    print(parsed.pretty())
    env = Env()
    x = FStopTransformer().transform(parsed)
    x.eval(env)
    assert 'im' in env.images
    env['im'].show('thing.png')
