exec(open("GroveError.py").read())
import sys
import importlib
var_table = {}

class Expr:
    pass

class StringLiteral:
    def __init(self,name):
        if not (" "  in name) and not("." is in name):
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
            raise GroveError("variable anme in correct")
    
    def getName(self):
        return self.name
    
    def eval(self):
        if(self.name == "quit" || self.name == "exit"):
            return sys.exit()
        if self.name in var_table:
            return var_table[self.name]
        else:
            raise GroveError("error?")
            
class Method(Expr):
    def __init__(self,keyWord, firstName,secName, *args):
        self.keyWord = keyWord
        self.firstName = firstName
        self.secName = secName
    def __eval__(self):
         if self.firstName in var_table:
            methodList = [methodName for methodName in dir(self.firstName) if callable(getattr(self.firstName,methodName))]
            if self.secondName in methodList:
                #not sure what goes here
                self.firstName.eval()
            else:
                raise GroveError("GROVE: method " + str(self.secondName) + " is not defined for: " + str(self.firstName) )
        else:
            raise GroveError("GROVE: name not found in var table, METHOD")
        
            
            
class Addition(Expr):
    
    def __init__(self,child1,child2):
        self.child1 = child1
        self.child2 = child2
        
        if not isinstance(self.child1,Expr):
            raise GroveError("CALC: expected expression but recieved " + str(type(self.child1)))
            
        if not isinstance(self.child2,Expr):
            raise GroveError("CALC: expected expression but recieved " + str(type(self.child2)))
            
    def eval(self):
        if not isinstance(self.child2,self.child1):
            raise GroveError("GROVE: expected" + str(type(self.child1) + " but found " + str(type(self.child2))
        else:
            return self.child1.eval() + self.child2.eval()
    
    
            
class Num(Expr):
    def __init__(self,value):
        self.value = value
        
    def eval(self):
        return self.value
    
    
class Stmt:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        if not isinstance(self.name,Name):
            raise GroveError("CALC: expected expression but recieved " + str(type(self.name)))
        if not isinstance(self.value,Expr):
            raise GroveError("CALC: expected expression but recieved " + str(type(self.value)))
            
        
    def eval(self):
        if(self.name == "quit" || self.name == "exit"):
            sys.exit()
        elif self.name == "import":
            module = importlib.import_module(self.value)
            #call = getattr(mod,)
            #call()
        else:
            var_table[self.name.getName()] = self.value.eval()
                                                     
                                                     
                                                     
                                                     
                                                     