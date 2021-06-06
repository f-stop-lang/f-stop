class String:
    def __init__(self, value: str) -> None:
        self.value = value
    
    def __repr__(self) -> str:
        # Backwards compatibility for Python <3.5
        return '<String "{}">'.format(self.value)
    
    def eval(self, env) -> str:
        return self.value
    
    
class Coordinate:
    """
    Equivalent of a tuple in Python.
    """
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
    
    
class Env:
    def __init__(self) -> None:
        self.images: dict = {}

        
class Open:
    def __init__(self, env) -> None:
        pass
