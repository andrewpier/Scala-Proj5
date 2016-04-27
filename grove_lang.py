exec(open("GroveError.py").read())
import sys
var_table = {}

class Expr:
    pass

class StringLiteral:
    def __init(self,name):
        if(name[0].isalpha() or name[0] == '_' and name[1:].isalnum()):
            self.name = name
        else:
            raise GroveError("GROVE: Improper string literal")
        
        
    def eval(self):
        return "\"" + self.name + "\""

class Name(Expr):
    def __init__(self,name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def eval(self):
        if(self.name == "quit" || self.name == "exit"):
            return sys.exit()
        if self.name in var_table:
            return var_table[self.name]
        else:
            raise GroveError("error?")
            
            
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
            
        var_table[self.name.getName()] = self.value.eval()