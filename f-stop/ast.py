class String:
    def __init__(self, value: str) -> None:
        self.value = value
    
    def eval(self):
        return self.value
    
class Env:
    def __init__(self) -> None:
        self.images = {}

class Open:
    def __init__(self) -> None:
        pass

