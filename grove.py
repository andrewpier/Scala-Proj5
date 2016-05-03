'''

Is your Grove interpreter using a static or dynamic type system? Briefly explain what aspects of the
interpreter make it so.
    This is a dynamic type system, since we do not know what the type is until run time, and variables can refer to different types at different points in the program this all makes it dynamic. 

'''
exec(open("grove_parse.py").read())
import importlib
if __name__ == "__main__":
    while True:
        try:
            ln = input("Grove>> ")
            root = parse(ln)
            res = root.eval()
            if not res is None:
                print(res)
        except GroveError as err:
            print(str(err))