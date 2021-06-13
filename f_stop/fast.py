from typing import Any, Dict, List, Tuple

from PIL import Image, ImageOps

class String:
    """ 
    Represents a string.
    """
    def __init__(self, value: str) -> None:
        self.value = value.strip("'").strip('"')
    
    def __repr__(self) -> str:
        # Backwards compatibility for Python <3.5
        return f'<String "{self.value}">'
    
    def eval(self, env=None) -> str:
        return self.value

    


class Env:
    """ 
    Represents a program environment.
    """
    def __init__(self) -> None:
        self.images: Dict[str, Image.Image] = {}

    #Honestly, these aren't necessary, i'm just very lazy to type env.images a buncha times
    def __setitem__(self, key: str, value: Any) -> None:
        self.images[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.images[key]

    def __delitem__(self, key: str) -> None:
        del self.images[key]

    def get(self, key: str, default: Any=None):
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
            raise Exception(F"{self.image} COULD NOT BE FOUND YOU DUMBO")
        env[self.image] = x.resize(self.tup.eval(env))



class Start:
    def __init__(self, statements: Tuple) -> None:
        self.statements = statements

    def eval(self, env: Env):
        for i in self.statements:
            i.eval(env)

class Tuple_:
    def __init__(self, tup: str) -> None:
        self.tuple = eval(tup)


    def eval(self, env: Env):
        return self.tuple

class Invert:
    def __init__(self, im: str):
        self.im = im

    def eval(self, env):
        if not (x := env.get(self.im)):
            raise NameError(f"{self.im} COULD NOT BE FOUND YOU LAXY BIINCH")
        env[self.im] = ImageOps.invert(x)