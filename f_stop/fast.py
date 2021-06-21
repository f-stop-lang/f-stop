from typing import Any, Dict, List

from PIL import Image, ImageOps, ImageDraw


class String:
    """
    Represents a string.
    """

    def __init__(self, value: str) -> None:
        self.value = value.strip("'").strip('"')

    def __repr__(self) -> str:

        return f'<String "{self.value}">'

    def eval(self, env=None) -> str:
        return self.value


class Env:
    """
    Represents a program environment.
    """

    def __init__(self) -> None:
        self.images: Dict[str, Image.Image] = {}

    # Honestly, these aren't necessary, i'm just very lazy to type env.images a buncha times
    def __setitem__(self, key: str, value: Any) -> None:
        self.images[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.images[key]

    def __delitem__(self, key: str) -> None:
        del self.images[key]

    def get(self, key: str, default: Any = None):
        return self.images.get(key, default)


class Open:
    """
    Represents the open statement.
    """

    def __init__(self, image: ..., value: ...) -> None:
        self.value = String(value)
        self.image = image

    def eval(self, env):
        env[self.value.eval(env)] = Image.open(self.image.eval())


class Resize:
    def __init__(self, image: str, tup) -> None:
        self.image = image
        self.tup = tup

    def eval(self, env):
        if not (x := env.images.get(self.image)):
            raise Exception(f'{self.image} COULD NOT BE FOUND YOU DUMBO')
        env[self.image] = x.resize(tuple(int(i) for i in self.tup.eval(env)))




class Start:
    def __init__(self, statements) -> None:
        self.statements = statements

    def eval(self, env: Env):
        for i in self.statements:
            i.eval(env)


class Tuple:
    def __init__(self, tup) -> None:
        self.tuple = tup
        #print(tup)

    def eval(self, env: Env=None):
        return tuple(i.eval(env) for i in self.tuple)

    def __int__(self):
        return tuple(i.__int__() for i in self.tuple)


class Invert:
    def __init__(self, im: str):
        self.im = im

    def eval(self, env):
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.invert(x.convert('RGB'))


class Solarize:
    def __init__(self, im, thres) -> None:
        self.im = im
        self.thres = thres

    def eval(self, env: Env):
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.solarize(
            x.convert('RGB'), self.thres.eval(env)
        )


class Crop:
    def __init__(self, im, tup) -> None:
        self.im = im
        self.tup = tup

    def eval(self, env):
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        if len(self.tup.eval(env)) != 4:
            raise Exception('Expected a tuple of length 4.')
        env[self.im] = x.crop(self.tup.eval(env))


class Number:
    def __init__(self, value):
        self.value = float(value)

    def eval(self, env=None):
        return self.value


class Integer:
    def __init__(self, value) -> None:
        self.value = int(value)

    def eval(self, env=None):
        return self.value


class Posterize:
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


class Flip:
    def __init__(self, im):
        self.im = im

    def eval(self, env):
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.flip(x.convert('RGB'))


class Grayscale:
    def __init__(self, im):
        self.im = im

    def eval(self, env):
        if not (x := env.get(self.im)):
            raise NameError(f'{self.im} COULD NOT BE FOUND YOU LAXY BIINCH')
        env[self.im] = ImageOps.grayscale(x.convert('RGB'))

class Color:
    def __init__(self, val) -> None:
        self.val = val

    def eval(self, env=None):
        return self.val

class Arc:
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
            raise Exception(f"{x} could not be found :C")
        draw = ImageDraw.Draw(x.convert('RGBA'), 'RGBA')
        print(type(self.xy), self.xy.eval(env))
        print(type(self.start), self.start.eval(env))
        print(type(self.end), self.end.eval(env))
        print(type(self.fill), self.fill)
        print(type(self.width), self.width.eval(env))
        xy = tuple(int(i) for i in self.xy.eval(env))
        fill = tuple(int(i) for i in self.fill) if self.fill else None
        print(fill)
        draw.arc(xy, int(self.start.eval(env)), self.end.eval(env).__int__(), fill, int(self.width.eval())) # type: ignore


class Rectangle:
    ...