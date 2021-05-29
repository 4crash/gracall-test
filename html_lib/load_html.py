
import codecs

def load_html(file:str) -> str:
    f = codecs.open(f"html_lib\{file}", "r")
    return f.read()
