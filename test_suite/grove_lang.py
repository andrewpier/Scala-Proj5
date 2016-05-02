exec(open("GroveError.py").read())
import sys
import importlib
import types
var_table = {}

class Expr:
    pass

class StringLiteral:
    def __init(self,name):
        if not (" "  in name) and not("." in name):
            self.name = name
        else:
            raise GroveError("GROVE: Improper string literal")
            
    def eval(self):
        return self.name
    
    

class Name(Expr):
    def __init__(self,name):
        if (name[0].isalpha or name[0] == "_" and name[1:].isalnum() ):
            self.name = name
        else:
            raise GroveError("variable name incorrect")
    
    def getName(self):
        return self.name
    
    def eval(self):
        if self.name in var_table:
            return var_table[self.name]
        else:
            raise GroveError("error?")
            
            
            
class Method(Expr):
    def __init__(self,keyWord, firstName,secName, *args):
        self.keyWord = keyWord
        self.firstName = firstName
        self.secName = secName
        self.arguments = args
        
    def __eval__(self):
        if self.firstName in var_table:
            methodList = [methodName for methodName in dir(self.firstName) if callable(getattr(self.firstName,methodName))]
            if self.secondName in methodList:
                getattr(self.firstName.eval(),methodName.eval())(*arguments)
            else:
                raise GroveError("GROVE: method " + str(self.secondName) + " is not defined for: " + str(self.firstName) )
        else:
            raise GroveError("GROVE: name not found in var table, METHOD")
        
                       
            
class Addition(Expr):
    def __init__(self,child1,child2):
        self.child1 = child1
        self.child2 = child2
            
    def eval(self):
        if not type(self.child1) == type(self.child2):
            raise GroveError("GROVE: cannot add two different types type 1:" + str(type(self.child1)) + " type 2:" + str(type(self.child2)))
        else:
            return self.child1.eval() + self.child2.eval()

        
        
        
        
        
class Call(Expr):
    def __init__(self,child1,child2, child3):
        self.name = child1
        self.method = child2
        self.args = child3
        
        if not isinstance(self.name, Name):
            raise GroveError("GROVE: expected expression but recieved " + str(type(self.name)))
        if not isinstance(self.method, Name):
            raise GroveError("GROVE: expected expression but recieved " + str(type(self.method)))
        
        
    def eval(self):
        theFunction = getattr(var_table[self.name], self.method)
        theFunction(*self.args)
        
        
        
        
    
            
class Num(Expr):
    def __init__(self,value):
        self.value = value
        
    def eval(self):
        return self.value
                                                     
                                                     
    
    
class Stmt:
    # I think that we should use the *args here in order to be able to take 0, 1, 2 names
    def __init__(self, keyword, name, value):
        self.keyword = args[0]
        self.args = args[1:]
        if not isinstance(self.args[0], Name):
            raise GroveError("GROVE: expected expression but recieved " + str(type(self.args[0])))
        
            
        
    def eval(self):
        if(self.keyword == "quit" or self.keyword == "exit"):
            sys.exit()
        elif self.keyword == "import":
            module = importlib.import_module(self.args[0])
            globals()[keyword] = module
            #call = getattr(mod,)
            #call()
        elif self.keyword == "set":
            if isinstance(self.args[1], Expr):
                var_table[self.args[0].getName()] = self.args[1].eval()
            else:
                #is they the value is expressions
                if(self.args.count >= 3):
                    #var_table[self.args[0].getName()] = new args[1].eval()
                    #we need to be able to . another name 
                    myClass = globals()[args[1]]()
                    myObj = getattr(myClass,self.args[2])
                    var_table[self.args[0].getName()] = myObj
                else:
                    myClass = globals()[args[1]]()
                    var_table[self.args[0].getName()] = myClass  
                
        else:
            raise GroveError("GROVE: invalid keyword " + str(self.keyword))  