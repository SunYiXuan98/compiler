def E():
    global token
    print("E->",token[0])

    T()
    getNextToken()
    E1()
    getNextToken()
    if(token[0]!="$"):
        print("ERROR:E")
        exit()
    else:
        print("RIGHT")
        exit()

def E1():
    global token
    print("E1->",token[0])

    if(token[0] in ['+','-']):
        getNextToken()
        T()
        getNextToken()
        E1()
    else:
        global point
        point-=1
        return
    

def T():
    global token
    print("T->",token[0])

    F()
    getNextToken()
    T1()

def T1():
    global token
    print("T1->",token[0])

    if(token[0] in ['*','/']):
        getNextToken()
        F()
        getNextToken()
        T1()
    else:
        global point
        point-=1
        return

def F():
    global token
    print("F->",token[0])

    if (token[1]!='DIGIT'):
        print('ERROR:F')
        exit()










#1=2+3
def S():
    global token
    print("S->",token.Name)
    if(token.Type=='DIGIT'):
        getNextToken()
        if(token.Name=='='):
            getNextToken()
            E()
            getNextToken()
            if(token.Name=="$"):
                print("RIGHT")
                exit()
            else:
                #tokenBack()
                print("ERROR:E")
                exit()
        else:
            print("ERROR:E")
            exit()
    else:
        print("ERROR:E")
        exit()


def E():
    global token
    print("E->",token.Name)

    T()
    getNextToken()
    E1()
    getNextToken()




def E1():
    global token
    print("E1->",token.Name)

    if(token.Name in ['+','-']):
        getNextToken()
        T()
        getNextToken()
        E1()
    else:
        print('E1 choose null')
        tokenBack()
        return
    

def T():
    global token
    print("T->",token.Name)

    F()
    getNextToken()
    T1()

def T1():
    global token
    print("T1->",token.Name)

    if(token.Name in ['*','/']):
        getNextToken()
        F()
        getNextToken()
        T1()
    else:
        print('T1 choose null')
        tokenBack()
        return

def F():
    global token
    print("F->",token.Name)
    # if(token.Name=='('):
    #     getNextToken()
    #     E()
    #     getNextToken()
    #     if(token.Name!=')'):
    #         print('ERROR:F')
    #         exit()
    if (token.Type!='DIGIT'):
        print('ERROR:F')
        exit()