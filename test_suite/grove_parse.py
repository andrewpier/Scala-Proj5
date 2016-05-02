exec(open("grove_lang.py").read())

# Utility methods for handling parse errors
def check(condition, message = "Unexpected end of expression"):
    """ Checks if condition is true, raising a ValueError otherwise """
    if not condition:
        raise ValueError("GROVE: " + message)
        
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
            (esprName,tokens) = parse_tokens(tokens[2:])
            check(len(tokens) > 1)
            return (Stmt(varName, esprName), tokens)
        expect(tokens[1],"new")
        (objName,tokens) = parse_tokens(tokens[2:])
        if tokens[0] == ".":
            (methodName,tokens) = parse_tokens(tokens[1:])
            check(len(tokens) > 1)
            return (Stmt("new", varName, objName, methodName), tokens)
        else:
            return (Stmt("new", varName, objName), tokens)
        
    elif start == "quit" or start == "exit":
        return (Stmt(start,Name("quit"),0),tokens[1:])
    
    elif start == "import":
        (varname,tokens) = parse_tokens(tokens[1:]) # get the import name
        return (Stmt(start,varname),tokens) # made a change here
    
    elif start == "call":
        #"call" "(" <Name> <Name> <Expr>* ")" 
        expect(tokens[1],"(")
        (child1,tokens) = parse_tokens(tokens[2:])
        check(len(tokens) > 1)
        (child2,tokens) = parse_tokens(tokens)
        check(len(tokens) > 1)
        
        myArgs = list()
        
        while tokens[1] != ")":
            (child1,tokens) = parse_tokens(tokens[2:])
            if not isinstance(child1, Expr):
                raise GroveError("Andrew Sucks!")
            myArgs.append(child1)
        
        expect(tokens[1],")")
   
        return()
    else:
        if start == "\"":
            return(StringLiteral(tokens[1],tokens[3:])) # return string literal
        else:
            return(Name(start), tokens[1:])#return name
        