from typing import Any

import PIL.Image

class String:
    """ 
    Represents a string.
    """
    def __init__(self, value: str) -> None:
        self.value = value.strip("'").strip('"')
    
    def __repr__(self) -> str:
        # Backwards compatibility for Python <3.5
        return '<String "{}">'.format(self.value)
    
    def eval(self, env=None) -> str:
        return self.value

    
"""
class Coordinate:
    Equivalent of a tuple in Python.
    def __init__(self, value: tuple) -> None:
        self.value: tuple = value
        
    @property
    def x(self) -> int:
        return self.value[0]
    
    @property
    def y(self) -> int:
        return self.value[1]
    
    def __repr__(self) -> str: 
        # Backwards compatibility for Python <3.5
        return '<Coordinate {!r}>'.format(self.value)
""" 
    
class Env:
    """ 
    Represents a program environment.
    """
    def __init__(self) -> None:
        self.images: dict = {}

    def __setitem__(self, key, value) -> None:
        self.images[key] = value

    def __getitem__(self, key) -> Any:
        return self.images[key]

    def __delitem__(self, key) -> None:
        del self.images[key]

    def get(self, key, default=None):
        return self.images.get(key, default)

class Open:
    """ 
    Represents the open statement.
    """
    def __init__(self, image: ..., value: ...) -> None:
        self.value = String(value)
        self.image = image
        

    def eval(self, env):
        env[self.value.eval(env)] = PIL.Image.open(self.image.eval())
        print("OPEN STATMENT: " , env[self.value.eval()])

class Resize:
    def __init__(self, image, tup) -> None:
        self.image = image
        self.tup = tup
        print(type(self.tup))

    def eval(self, env):
        if not (x := env.images.get(self.image)):
            raise Exception(F"{self.image} COULD NOT BE FOUND YOU DUMBO")
        env[self.image] = x.resize(self.tup.eval(env))
        print("resized image :D")


class Start:
    def __init__(self, statements) -> None:
        self.statements = statements

    def eval(self, env):
        for i in self.statements:
            i.eval(env)

class Tuple:
    def __init__(self, tup) -> None:
        self.tuple = eval(tup)
        print(self.tuple)
        print(type(self.tuple))

    def eval(self, env):
        return self.tuple