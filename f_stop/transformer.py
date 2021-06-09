from lark import Transformer, v_args

from fast import String, Open  #type: ignore


@v_args(inline=True)
class FStopTransformer(Transformer):
    def open_stmt(self, image: str, name: str) -> Open:
        print(image)
        print(name)
        return Open(image=image, value=name)

    def resize_stmt(self, image: str, coord1: int, coord2: int):
        print(image)
        print(coord1)
        print(coord2)

    
    def string(self, s: str) -> String:
        val = str(s).strip('"').strip("'")
        return String(s)
