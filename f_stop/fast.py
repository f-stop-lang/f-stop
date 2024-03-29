
import re
import urllib.request as requests
from abc import ABC
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple, TypeVar

from PIL import (Image, ImageDraw, ImageEnhance, ImageFont, ImageOps,
                 ImageSequence)

import cv2 
import numpy


class Env:
    """
    Represents a program environment.
    """

    def __init__(self) -> None:
        self.images: Dict[str, Image.Image] = {}
        self.cascade_cache: Dict[str, cv2.CascadeClassifier] = {}

    # Honestly, these aren't necessary, i'm just very lazy to type env.images a buncha times
    def __setitem__(self, key: str, value: Any) -> None:
        self.images[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.images[key]

    def __delitem__(self, key: str) -> None:
        del self.images[key]

    def get(self, key: str, default: Any = None):
        return self.images.get(key, default)


class Token(ABC):
    def eval(self, env: Optional[Env] = None) -> Any:   # type: ignore
        raise NotImplementedError


T = TypeVar('T', bound=Token)


class String(Token):
    """
    Represents a string.
    """

    def __init__(self, value: str) -> None:
        self.value = value.strip("'").strip('"')

    def __repr__(self) -> str:

        return f'<String "{self.value}">'

    def eval(self, env=None) -> str:   # type: ignore
        return self.value


class Number(Token):
    def __init__(self, value):
        self.value = float(value)

    def eval(self, env=None):
        return self.value


class Integer(Token):
    def __init__(self, value) -> None:
        self.value = int(value)

    def eval(self, env=None):
        return self.value


class NTuple(Token):
    def __init__(self, tup: Tuple[int, ...]) -> None:
        self.tuple: Tuple[int, ...] = tup
        # print(tup)

    def eval(self, env: Optional[Env] = None) -> Tuple[int, ...]:
        return tuple(i.eval(env) for i in self.tuple)   # type: ignore


class Open:
    """
    Represents the open statement.
    """

    def __init__(self, image: str, value: str) -> None:
        self.value = String(value)
        self.image = image

    def eval(self, env: Env) -> Any:
        env[self.value.eval(env)] = Image.open(
            self.image.eval()
        )   # type: ignore


class Resize(Token):
    def __init__(self, image: str, tup: NTuple) -> None:
        self.image: str = image
        self.tup: NTuple = tup

    def eval(self, env) -> Any:
        x = env.images.get(self.image)
        if not x:
            raise Exception(f'{self.image} COULD NOT BE FOUND YOU DUMBO')
        env[self.image] = x.resize(tuple(int(i) for i in self.tup.eval(env)))


class Start(Token):
    def __init__(self, statements) -> None:
        self.statements = statements

    def eval(self, env) -> Any:
        for i in self.statements:
            print(i)
            i.eval(env)


class Invert(Token):
    def __init__(self, im: str):
        self.im: str = im

    def eval(self, env: Env) -> None:
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.invert(x.convert('RGB'))


class Solarize(Token):
    def __init__(self, im: str, thres: Number) -> None:
        self.im: str = im
        self.thres: Number = thres

    def eval(self, env: Env) -> None:
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.solarize(
            x.convert('RGB'), self.thres.eval(env)
        )


class Crop(Token):
    def __init__(self, im, tup) -> None:
        self.im = im
        self.tup = tup

    def eval(self, env):
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        if len(self.tup.eval(env)) != 4:
            raise Exception('Expected a tuple of length 4.')
        env[self.im] = x.crop(self.tup.eval(env))


class Posterize(Token):
    def __init__(self, im, bits) -> None:
        self.im = im
        self.bits = bits

    def eval(self, env: Env):
        print(type(self.bits.eval(env)))
        bits = int(self.bits.eval(env))
        if bits < 1 or bits > 8:
            raise Exception('Bits must be and integer between 1 and 8')
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.posterize(x.convert('RGB'), int(bits))


class Flip(Token):
    def __init__(self, im):
        self.im = im

    def eval(self, env):
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.flip(x.convert('RGB'))


class Grayscale(Token):
    def __init__(self, im):
        self.im = im

    def eval(self, env):
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.grayscale(x.convert('RGB'))


class Color(Token):
    def __init__(self, val) -> None:
        self.val = val

    def eval(self, env=None):
        return self.val


class Arc(Token):
    def __init__(self, im, xy, start, end, fill=None, width=0):
        self.im = im
        self.xy = xy
        self.start = start
        self.end = end
        self.fill = fill
        self.width = width

    def eval(self, env):
        x = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        x = x.convert('RGBA')
        draw = ImageDraw.Draw(x)
        xy = tuple(int(i) for i in self.xy.eval(env))
        fill = tuple(int(i) for i in self.fill) if self.fill else None
        print(fill)
        draw.arc(
            xy,
            int(self.start.eval(env)),
            int(self.end.eval(env)),
            fill,  # type: ignore
            int(self.width.eval()),
        )   # type: ignore
        env[self.im] = x


class Rectangle(Token):
    def __init__(self, image, xy, fill=None, outline=None, width=1) -> None:
        self.im = image
        self.xy = xy
        self.fill = fill
        self.outline = outline
        self.width = width

    def eval(self, env: Env) -> Any:
        x = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        draw = ImageDraw.Draw(x)
        xy = tuple(map(int, self.xy.eval()))
        fill = tuple(map(int, self.fill))   # type: ignore
        outline = tuple(map(int, self.outline))   # type: ignore
        draw.rectangle(
            xy,
            fill,
            outline,
            int(self.width.eval()),
        )   # type: ignore
        env[self.im] = x


class Line(Token):
    def __init__(self, im, xy, color=None, width=Number(1)) -> None:
        self.im = im
        self.xy = xy
        self.color = color
        self.width = width

    def eval(self, env):
        x = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        draw = ImageDraw.Draw(x)
        xy = tuple(map(int, self.xy.eval()))
        fill = tuple(map(int, self.color))   # type: ignore
        draw.line(
            xy,
            fill,
            int(self.width.eval()),
        )
        env[self.im] = x


class Font(Token):
    def __init__(self, font, size) -> None:
        self.font = font
        self.size = size

    def eval(self, env=None):
        return ImageFont.truetype(font=self.font.eval(), size=self.size.eval())


class Text(Token):
    def __init__(self, im, xy, text, font=None, color=None) -> None:
        self.im = im
        self.xy = xy
        self.text = text
        self.font = font
        self.color = color

    def eval(self, env: ...) -> Any:
        x = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        draw = ImageDraw.Draw(x)
        xy = tuple(map(int, self.xy.eval()))
        fill = tuple(map(int, self.color))   # type: ignore
        draw.text(
            xy, self.text.eval(), fill, self.font.eval()
        )   # type: ignore
        env[self.im] = x


class Blend(Token):
    def __init__(self, im1, im2, alpha, new_im):
        self.im1 = im1
        self.im2 = im2
        self.alpha = alpha
        self.new_im = new_im

    def eval(self, env):
        x, y = env.get(self.im1), env.get(self.im2)
        if not x:
            raise Exception(f'{self.im1} could not be found :C')
        if not y:
            raise Exception(f'{self.im2} could not be found :C')
        z = Image.blend(x, y, self.alpha.eval())
        env[self.new_im] = z


class Convert(Token):
    def __init__(self, im, mode):
        self.im = im
        self.mode = mode

    def eval(self, env):
        x = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        env[self.im] = x.convert(self.mode.eval())


class UrlOpen(Token):
    def __init__(self, url, name):
        self.url = url
        self.name = name
        print(self.name)

    def eval(self, env):
        if not re.match(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            self.url.eval(),
        ):
            raise Exception('Not a valid URL >:(.')
        req = requests.Request(
            self.url.eval(),
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
            },
        )
        resp = requests.urlopen(req)
        byt = resp.read()
        io = BytesIO(byt)
        x = Image.open(io)
        env[self.name] = x


class Ellipse(Token):
    def __init__(self, im, xy, fill, outline, width=Number(1)) -> None:
        self.im = im
        self.xy = xy
        self.fill = fill
        self.outline = outline
        self.width = width

    def eval(self, env):
        x = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        draw = ImageDraw.Draw(x)
        xy = tuple(map(int, self.xy.eval()))
        fill = tuple(map(int, self.fill))   # type: ignore
        outline = tuple(map(int, self.outline))
        draw.ellipse(
            xy, fill, outline, width=int(self.width.eval())
        )   # type: ignore
        env[self.im] = x


class Save(Token):
    def __init__(self, im, filename) -> None:
        self.im = im
        self.filename = filename

    def eval(self, env):
        x: Image.Image = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        if isinstance(x, list):
            x[0].save(
                self.filename.eval(),
                append_images=x[1:],
                save_all=True,
                loop=0,
                duration=20,
            )
        else:
            x.save(self.filename.eval())


class Close(Token):
    def __init__(self, im):
        self.im = im

    def eval(self, env):
        x = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        return x.close()


class Iterate(Token):
    def __init__(self, image, name, statements) -> None:
        self.image = image
        self.name = name
        self.statements = statements

    def eval(self, env):
        x = env.get(self.image)
        if not x:
            raise Exception(f'{self.image} could not be found :C')
        frames = []
        for j, i in enumerate(ImageSequence.Iterator(x)):
            env[self.name] = i
            for statement in self.statements:
                statement.eval(env)
            frames.append(env.get(self.name))

        try:
            del env[self.name]
        except KeyError:
            pass

        env[self.image] = frames


class New(Token):
    def __init__(self, *, mode, size, color=0, name):
        self.mode = mode
        self.size = size
        self.color = color
        self.name = name

    def eval(self, env):
        size = tuple(map(int, self.size.eval()))
        if not isinstance(self.color, (int, str)):
            self.color = (
                tuple(map(int, self.color.eval()))
                if isinstance(self.color, NTuple)
                else self.color
            )
        im = Image.new(
            self.mode.eval(), size, self.color  # type: ignore
        )   # type: ignore
        env[self.name] = im


class Echo(Token):
    def __init__(self, string):
        self.string = string

    def eval(self, env):
        print(self.string.eval())


class Putpixel(Token):
    def __init__(self, image, xy, color) -> None:
        self.image = image
        self.xy = xy
        self.color = color

    def eval(self, env):
        x: Image.Image = env.get(self.image)
        if not x:
            raise Exception(f'{self.image} could not be found :C')
        color = (
            tuple(map(int, self.color))
            if isinstance(self.color, tuple)
            else int(self.color)
        )
        xy = tuple(map(int, self.xy.eval()))
        x.putpixel(xy, color)


class Enhance(Token):
    def __init__(self, im, filter_type: String, number) -> None:
        self.image = im
        self.filter_type = filter_type
        self.number = number

    def eval(self, env: Env):
        x: Image.Image = env.get(self.image)
        if not x:
            raise Exception(f'{self.image} could not be found :C')

        filter = getattr(ImageEnhance, self.filter_type.eval().title())
        enhance = filter(x)
        enhance.enhance(self.number.eval())


class Canny(Token):
    def __init__(self, im, thres1, thres2):
        self.im = im
        self.thres1 = thres1
        self.thres2 = thres2

    def eval(self, env: Env):
        x: Image.Image = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        arr = numpy.asarray(x)
        im = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        thing = cv2.Canny(im, self.thres1.eval(), self.thres2.eval())
        env[self.im] = Image.fromarray(cv2.cvtColor(thing, cv2.COLOR_BGR2RGB))


class CvtColor(Token):
    def __init__(self, im, filter) -> None:
        self.im = im
        self.filter: String = filter

    def eval(self, env):
        x: Image.Image = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        arr = numpy.asarray(x)
        im = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        thing = cv2.cvtColor(
            im,
            getattr(
                cv2,
                self.filter.eval()
                if self.filter.eval().startswith('COLOR_')
                else 'COLOR_' + self.filter.eval(),
            ),
        )
        env[self.im] = Image.fromarray(thing)


class Cascade(Token):
    def __init__(self, path, var) -> None:
        self.path = path
        self.var = var

    def eval(self, env: Env):
        thing = cv2.CascadeClassifier(self.path.eval())
        env.cascade_cache[self.var] = thing

class Detect(Token):
    def __init__(self, im, casc, scalefactor, minneighbors, minsize, color) -> None:
        self.im = im
        self.casc = casc
        self.scalefactor = scalefactor
        self.minneighbors = minneighbors
        self.minsize = minsize
        self.color  = color

    def eval(self, env: Env):
        x: Image.Image = env.get(self.im)
        if not x:
            raise Exception(f'{self.im} could not be found :C')
        casc = env.cascade_cache.get(self.casc)
        if not casc:
            raise Exception(f'{self.casc} could not be found :C')
        arr = numpy.asarray(x)
        im = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        minsize = tuple(int(i) for i in self.minsize.eval())
        detected = casc.detectMultiScale(gray, scaleFactor=self.scalefactor.eval(), minNeighbors=int(self.minneighbors.eval()), minSize=minsize)
        for (x, y, w, h) in detected:
            cv2.rectangle(im, (x, y), (x+w, y+h), self.color, 2)
        env[self.im] = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))


