exec(open("grove_parse.py").read())

while True:
    ln = input("Grove>> ")
    root = parse(ln)
    res = root.eval()
    if not res is None:
        print(res)