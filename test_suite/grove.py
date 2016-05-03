exec(open("grove_parse.py").read())
import importlib
while True:
    try:
        ln = input("Grove>> ")
        root = parse(ln)
        res = root.eval()
        if not res is None:
            print(res)
    except GroveError as err:
        print(str(err))