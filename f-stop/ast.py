class String:
    def __init__(self, value: str) -> None:
        self.value = value
    
    def eval(self, env) -> str:
        return self.value
    
class Env:
    def __init__(self) -> None:
        self.images = {}

class Open:
    def __init__(self, env) -> None:
        pass

