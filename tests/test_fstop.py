from f_stop.transformer import FStopTransformer
from f_stop.fast import Env
from lark import Lark
from PIL import Image, ImageDraw


if __name__ == '__main__':
    with open('test1.fstop') as ft:
        text = ft.read()
    f_stop_parser = Lark.open(
        '../f_stop/grammar.lark', rel_to=__file__)
    parsed = f_stop_parser.parse(text)
    print(parsed.pretty())
    env = Env()
    env['img'] = Image.new('RGBA', (300, 300), (255, 0, 0))
    x = FStopTransformer().transform(parsed)
    x.eval(env)
#source.python meta.qualified-name.python meta.generic-name.python
#source.python meta.statement.with.python meta.generic-name.python
