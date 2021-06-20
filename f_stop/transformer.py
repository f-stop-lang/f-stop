from lark import Transformer, v_args

from .fast import *  # type: ignore

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

    def start(self, *statements) -> Start:
        return Start(statements)

    def ntuple(self, tup) -> Tuple:
        return Tuple(tup)

    def invert_stmt(self, var) -> Invert:
        return Invert(var)

    def solarize_stmt(self, im, threshold: Number = Number(128)):
        return Solarize(im, threshold)

    def crop_stmt(self, im, size):
        return Crop(im, size)

    def NUMBER(self, val):
        return Number(val)

    def posterize_stmt(self, im, bits):
        return Posterize(im, bits)

    def INTEGER(self, val):
        return Integer(val)

    def flip_stmt(self, im):
        return Flip(im=im)

    def grayscale_stmt(self, im):
        return Grayscale(im=im)