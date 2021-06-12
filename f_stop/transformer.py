from lark import Transformer, v_args

from fast import String, Open, Start, Tuple, Resize  #type: ignore


@v_args(inline=True)
class FStopTransformer(Transformer):
    def open_stmt(self, image: str, name: str) -> Open:
        return Open(image=image, value=name)

    def resize_stmt(self, image, tup):
        return Resize(image, tup)

    
    def string(self, s: str) -> String:
        val = str(s).strip('"').strip("'")
        return String(s)


    def start(self, *statements):
        return Start(statements)

    def ntuple(self, tup):
        return Tuple(tup)
