exec(open("grove_lang.py").read())

# Utility methods for handling parse errors
def check(condition, message = "Unexpected end of expression"):
    """ Checks if condition is true, raising a ValueError otherwise """
    if not condition:
        raise GroveError("GROVE-Parse: " + message)
        
def expect(token, expected):
    """ Checks that token matches expected
        If not, throws a ValueError with explanatory message """
    if token != expected:
        check(False, "Expected '" + expected + "' but found '" + token + "'")
        
def is_expr(x):
    if not isinstance(x, Expr):
        check(False, "Expected expression but found " + str(type(x)))        
# Checking for integer        
def is_int(s):
    """ Takes a string and returns True if in can be converted to an integer """
    try:
        int(s)
        return True
    except ValueError:
        return False
       
def parse(s):
    """ Return an object representing a parsed command
        Throws ValueError for improper syntax """
    
    (root, remaining_tokens) = parse_tokens(s.split())
    #the parse call should have used all the tokens
    check(len(remaining_tokens) == 0, "expcted end of command but found '" + " ".join(remaining_tokens) + "'" )
    return root
        
        
        
def parse_tokens(tokens):
    """ Returns a tuple:
        (an object representing the next part of the expression,
         the remaining tokens)
    """
    check(len(tokens) > 0)
    start = tokens[0]
    
    # TODO: parse the next part of the expression
    if is_int(start):
        return(Num(int(start)),tokens[1:])
    
    elif start in ["+"]:
        #"+" "(" <Expr> ")" "(" <Expr> ")" 
        expect(tokens[1],"(")
        (child1,tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 1)
        expect(tokens[0], ")")
        expect(tokens[1],"(")
        (child2,tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 0)
        expect(tokens[0],")")
        return (Addition(child1,child2),tokens[1:])
    
    elif start == "set":
        # "set" <Name> "=" "new" <Name>      | "set" <Name> "=" "new" <Name>"."<Name>
        (varName,tokens) = parse_tokens(tokens[1:])
        check(len(tokens) > 1)
        expect(tokens[0], "=")
        
        if not tokens[1] == "new":
            (esprName,tokens) = parse_tokens(tokens[1:])
            return (Stmt(start, varName, esprName), tokens)

        
        if "." in tokens[2]:
            names = tokens[2]
            myNames = names.split(".")
            return (Stmt(start, "new", varName, Name(myNames[0]), Name(myNames[1])), tokens[3:])
        else:
            return (Stmt(start, "new", varName, Name(tokens[2])), tokens[3:])
        
        
        
        
    elif start == "quit" or start == "exit":
        return (Stmt(start,"quit",0),tokens[1:])
    
    elif start == "import":
        (varname,tokens) = parse_tokens(tokens[1:]) # get the import name
        return (Stmt(start,varname),tokens) # made a change here
    
    elif start == "call":
        #"call" "(" <Name> <Name> <Expr>* ")" 
        check(len(tokens) > 1)
        expect(tokens[1],"(")
        
        (child1,tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 1)
        
        (child2,tokens) = parse_tokens(tokens)
        check(len(tokens) > 0)
        
        myArgs = list()
            
        while tokens[0] != ")":
            (child3,tokens) = parse_tokens(tokens)
            if not isinstance(child3, Expr):
                raise GroveError("Andrew Sucks!")
            myArgs.append(child3.eval())
        
        expect(tokens[0],")")
   
        return(Call(child1,child2, *myArgs),tokens[1:])


    else:
        if start[0] == "\"" :
            if not start[len(start)-1] == "\"":
                raise GroveError("Grove-Parse: Invalid String Literal: " + str(start) )
            if "\"" in start[1:len(start)-2]:
                raise GroveError("Grove-Parse: invalid string literal quotes were found: " + str(start) )
            return (StringLiteral(start), tokens[1:]) # return string literal
        else:
            
            #check(start[0].isalpha() or start[0] == "_" )
            isValidName(start)
            return (Name(start), tokens[1:])#return name
        
        
def isValidName(strs):
    for s in strs:
        if not s.isalnum(): 
            if not s == "_":
                raise GroveError("Grove-Parse: Name contains invalid character: " + str(strs))
        
            
        