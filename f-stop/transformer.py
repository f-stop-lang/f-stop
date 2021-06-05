from lark import Transformer

class FStopTransformer(Transformer):
    def open_stmt(self, image, name):
        pass
    def string(self, s):
        (s,) = s
        