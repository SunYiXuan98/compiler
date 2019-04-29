def S():
    if(token.Type!='DIGIT'):
        print("ERROR:S")
        exit()
    getNextToken()
    if(token.Name!='='):
        print("ERROR:=")
        exit()
    getNextToken()
    E()
    print("RIGHT")
    exit()

def E():
    if(token.Name=='('):
        getNextToken()
        E1()
        getNextToken()
        if(token.Name!=')'):
            print("ERROR:)")
            exit()
    elif(token.Type=='DIGIT'):
        pass
    else:
        E1()
        getNextToken()
        if(token.Name=='+'):
            getNextToken()
            E2()
        elif(token.Name=='*'):
            getNextToken()
            E2()
        else:
            print("ERROR:E")
            exit()
    
def E1():
    pass

def E2():
    pass