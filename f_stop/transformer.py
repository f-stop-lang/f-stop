from lark import Transformer, v_args

from . import ast


@v_args(inline=True)
class FStopTransformer(Transformer):
    def open_stmt(self, image, name):
        return ast.Open(image=image, value=name)
    
    def string(self, s: str) -> ast.String:
        val = str(s).strip('"').strip("'")
        return ast.String(s)
