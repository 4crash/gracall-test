import os
import codecs

dirname, filename = os.path.split(os.path.abspath(__file__))
def load_html(file:str) -> str:
    f = codecs.open(dirname+f"/{file}", "r")
    return f.read()
