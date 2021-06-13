from lark import Transformer, v_args

from .fast import *  #type: ignore

from typing import List
@v_args(inline=True)
class FStopTransformer(Transformer):
    def open_stmt(self, image: str, name: str) -> Open:
        return Open(image=image, value=name)

    def resize_stmt(self, image: str, tup: str) -> Resize:
        return Resize(image, tup)

    
    def string(self, s: str) -> String:
        val = str(s).strip('"').strip("'")
        return String(s)


    def start(self, *statements: Tuple) -> Start:
        return Start(statements)

    def ntuple(self, tup) -> Tuple:
        return Tuple(tup)

    def invert_stmt(self, var) -> Invert:
        return Invert(var)

    def solarize_stmt(self, im, threshold: int=128):
        return Solarize(im, threshold)
