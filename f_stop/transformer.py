from typing import List

from PIL.Image import new

from lark import Transformer, v_args

from .fast import *  # type: ignore


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

    def ntuple(self, *tup) -> NTuple:
        return NTuple(tup)

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

    def arc_stmt(self, im, xy, start, end, fill, width=Number(5)):
        return Arc(im, xy, start, end, fill, width)

    def font(self, font, size=Number(10)):
        return Font(font, size)

    def color(self, thing):
        return Color(thing)

    def color_tuple(self, thing):
        return thing.eval()

    def color_int(self, int):
        return int.eval()

    def rectangle_stmt(self, im, xy, fill=None, outline=None, width=Number(1)):
        return Rectangle(im, xy, fill, outline, width)

    def line_stmt(self, im, xy, fill=None, width=Number(1)):
        return Line(im, xy, fill, width)

    def text_stmt(self, im, xy, text, font=None, fill=None):
        return Text(im, xy, text, font, fill)

    def blend_stmt(self, im1, im2, alpha, new_im):
        return Blend(im1, im2, alpha, new_im)

    def convert_stmt(self, im, mode):
        return Convert(im, mode)

    def url_stmt(self, url, name):
        return UrlOpen(url, name)

    def ellipse_stmt(self, im, xy, fill=None, outline=None, width=Integer(1)):
        return Ellipse(im, xy, fill, outline, width)

    def save_stmt(self, im, filename):
        return Save(im, filename)

    def close_stmt(self, im):
        return Close(im)

    def iter_stmt(self, im, name, *statements):
        return Iterate(im, name, statements)

    def new_stmt_no_color(self, mode, size, name):
        return New(mode=mode, size=size, name=name)

    def new_stmt(self, mode, size, color, name):
        return New(mode=mode, size=size, color=color, name=name)

    def echo_stmt(self, string):
        return Echo(string)

    def color_string(self, string):
        return string.eval()

    def putpixel_stmt(self, image, xy, color):
        return Putpixel(image, xy, color)

    def enhance_stmt(self, im, filter_type, number):
        return Enhance(im, filter_type, number)

    def canny_stmt(self, im, thres1, thres2):
        return Canny(im, thres1, thres2)

    def cvt_stmt(self, im, filter):
        return CvtColor(im, filter)

    def cascade(self, path, var):
        return Cascade(path, var)

    def detect_stmt(self, im, casc, scalefactor, minneighbors, minsize):
        return Detect(im, casc, scalefactor, minneighbors, minsize)
