from lark import Transformer, v_args

from fast import String, Open  #type: ignore


@v_args(inline=True)
class FStopTransformer(Transformer):
    def open_stmt(self, image: ..., name: str) -> None:
        return Open(image=image, value=name)
    
    def string(self, s: str) -> String:
        val = str(s)[1:-1]
        return String(s)
