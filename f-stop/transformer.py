from lark import Transformer, v_args
from . import ast
@v_args(inline=True)
class FStopTransformer(Transformer):
    def open_stmt(self, image, name):
        pass
    def string(self, s):
        val = str(s).replace('"', '')
        return ast.String(s)

