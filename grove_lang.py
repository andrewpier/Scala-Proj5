exec(open("GroveError.py").read())
import sys
import importlib
import types
var_table = {}

class Expr:
    pass

class StringLiteral(Expr):
    def __init__(self,name):
        if not (" "  in name) and not ("." in name):
            newName = name.strip("\"")
            self.name = newName        
        else:
            raise GroveError("GROVE-Eval: Improper string literal")       
    
            
    def eval(self):
        return self.name
    
    

class Name(Expr):
    def __init__(self,name):
        if (name[0].isalpha or name[0] == "_" and name[1:].isalnum() ):
            self.name =  name
        else:
            raise GroveError("GROVE-Eval: Variable name incorrect")
    
    def getName(self):
        return self.name
    
    def eval(self):
        if self.name in var_table:
            return var_table[self.name]
        else:
            raise GroveError("GROVE-Eval: Name not in the var table: " + str(self.name))
            
            
            
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
                raise GroveError("GROVE-Eval: method " + str(self.secondName) + " is not defined for: " + str(self.firstName) )
        else:
            raise GroveError("GROVE-Eval: name not found in var table, METHOD")
        
                       
            
class Addition(Expr):
    def __init__(self,child1,child2):
        self.child1 = child1
        self.child2 = child2
            
    def eval(self):
        if not type(self.child1.eval()) == type(self.child2.eval()):
            raise GroveError("GROVE-Eval: cannot add two different types type 1:" + str(type(self.child1.eval())) + " type 2:" + str(type(self.child2.eval())))
        else:
            return self.child1.eval() + self.child2.eval()

        
        
        
        
        
class Call(Expr):
    def __init__(self,child1,child2, *args):
        self.name = child1
        self.method = child2
        self.args = args
        
        if not isinstance(self.name, Name):
            raise GroveError("GROVE-Eval: expected expression but recieved " + str(type(self.name)))
        if not isinstance(self.method, Name):
            raise GroveError("GROVE-Eval: expected expression but recieved " + str(type(self.method)))
        
    def eval(self):
        if not self.name.getName() in var_table:
            raise GroveError("GROVE-Eval: variable not defined in var_table: " + str(self.name.getName()))
        if not self.method.getName() in dir(var_table[self.name.getName()]):
            print(dir(self.name.getName())) 
            raise GroveError("GROVE-Eval: method not defined in var_table: " + str(self.method.getName()))
            
        theFunction = getattr(var_table[self.name.getName()], self.method.getName())
        return theFunction(*self.args)
        
        
        
        
    
            
class Num(Expr):
    def __init__(self,value):
        self.value = value
        
    def eval(self):
        return self.value
                                                     
                                                     
    
    
class Stmt:
    # I think that we should use the *args here in order to be able to take 0, 1, 2 names
    def __init__(self,keyword,*args):
        self.keyword = keyword
        self.args = args
        #if not isinstance(self.args[0], Name):
         #   raise GroveError("GROVE: expected expression but recieved " + str(type(self.args[0])))
        
            
        
    def eval(self):
        if(self.keyword == "quit" or self.keyword == "exit"):
            sys.exit()
        elif self.keyword == "import":
            try:
                module = importlib.import_module(self.args[0].getName())
                globals()[self.args[0].getName()] = module
            except:
                raise GroveError("Grove-Eval: Import module not defined: " + str(self.args[0].getName()))
            
        elif self.keyword == "set":
            if not self.args[0] == "new":
                var_table[self.args[0].getName()] = self.args[1].eval()
            else:
                #is they the value is expressions
                if(len(self.args) > 3):
                    #var_table[self.args[0].getName()] = new args[1].eval()
                    #we need to be able to . another name 
                    #varName, objName, methodName
                    if not self.args[2].getName() in globals():
                        raise GroveError("Grove-Eval: object does not exist in globals: " + str(self.args[2].getName()))
                    myClass = globals()[self.args[2].getName()]
                    
                    if not self.args[3].getName() in dir(globals()[self.args[2].getName()]):
                        #print("this is a stupid error")
                        raise GroveError("Grove-Eval: method of object does not exist: " + str(self.args[3].getName()))
                        
                    myObj = getattr(myClass,self.args[3].getName())
                    var_table[self.args[1].getName()] = myObj()
                else:
                    if not self.args[2].getName() in globals():
                        raise GroveError("Grove-Eval: object does not exist in globals: " + str(self.args[2].getName()))
                    myClass = globals()[self.args[2].getName()]
                    var_table[self.args[1].getName()] = myClass()  
                
        else:
            raise GroveError("GROVE-Eval: invalid keyword " + str(self.keyword))  