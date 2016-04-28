exec(open("grove_parse.py").read())

while True:
    try:
        ln = input("Grove>> ")
        root = parse(ln)
        res = root.eval()
        if not res is None:
            print(res)
    except:
        raise GroveError("ERROR!!")