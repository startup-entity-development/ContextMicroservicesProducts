import json


def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except Exception:
        return False
