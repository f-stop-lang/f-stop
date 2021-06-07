import PIL
class String:
    def __init__(self, value: str) -> None:
        self.value = value.strip('"').strip("'")
    
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
    def __init__(self) -> None:
        self.images: dict = {}

        
class Open:
    def __init__(self, image, value) -> None:
        self.value = String(value)
        self.image = image
        print(self.value)
        print(self.image)
        

    def eval(self, env):
            env[self.value.eval(env)] = PIL.Image.open(self.image.eval())
            print(env[self.value.eval()])