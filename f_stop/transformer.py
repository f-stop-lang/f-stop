from lark import Transformer, v_args

from .fast import String, Open


@v_args(inline=True)
class FStopTransformer(Transformer):
    def open_stmt(self, image, name):
        return Open(image=image, value=name)
    
    def string(self, s: str) -> String:
        val = str(s).strip('"').strip("'")
        return String(s)
