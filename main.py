# coding=utf-8
from define import *
from tool import *
import re
import sys
import os

debug = 0

point_token = 0
point_t=0
point_s=0
point_label=0
class TOKEN:
    def __init__(self,Name=None,Type=None):
        self.Name = Name
        self.Type = Type

    def to_int(self,s):
        r= re.match(r'^-?[1-9]\d*|0',s)
        res = r.group()
        return res,len(res)

    def to_val(self,s):
        r= re.match(r'^[a-zA-Z_]\w*',s)
        res = r.group()
        return res,len(res)

    def to_opr(self,s):
        r= re.match(r'^[\+\-\*/]|[<>=!]=?|\|\||&&',s)
        res = r.group()
        return res,len(res)

    def show(self):
        print((self.Name,self.Type))

    def nextToken(self):
        return tokens[point_token]

    def preToken(self):
        return tokens[point_token-2]

def init_sentence():
    global point_r,point_t
    point_r=0
    point_t=0
    for attr in WHOLE_VALTABLE.values():
        attr['reg']=None
    for attr in LOCAL_VALTABLE.values():
        attr['reg']=None
    REG_USED.clear()

def init_func():
    LOCAL_VALTABLE.clear()
    global stack_offset
    stack_offset = -4

def func_head(func_name):
    gen('label',func_name)
    gen('push','$ra')
    gen('push','$fp')
    gen('=','$fp','$sp')
    

def func_end():
    gen('return',None)
    

def newLable():
    global point_label
    lable = 'L'+str(point_label)
    point_label+=1
    return lable

def getRegt(n):
    global point_t
    if(n==-1):
        reg = '$t'+str(point_t-1)
        return reg
    for _ in range(10):
        reg = '$t'+str(point_t)
        point_t+=1
        if reg not in REG_USED:
            break

    return reg

def getRegs():
    global point_s
    for _ in range(8):
        reg = '$s'+str(point_s)
        point_s+=1
        if reg not in REG_USED:
            break
        
    return reg

def tokenBack():
    global point_token
    point_token-=1

def getTokens(s):
    words = s.split()
    for s in words:
        while(len(s)):
            ch=s[0]
            if ch == ' ':
                s=s[1:]
            
            elif ch in OPR:
                res,i = TOKEN().to_opr(s)
                token = TOKEN(res,'OPR')
                tokens.append(token)
                s=s[i:]
            elif ch in BOUND:
                token = TOKEN(ch,'BOUND')
                tokens.append(token)
                s=s[1:]
            elif ch.isdigit():
                res,i = TOKEN().to_int(s)
                token = TOKEN(res,'DIGIT')
                s = s[i:]
                tokens.append(token)
            elif ch.isalpha():
                res,i = TOKEN().to_val(s)
                if(res in KEY):
                    token = TOKEN(res,'KEY')
                elif(res in FUNCTION):
                    token = TOKEN(res,'SYSCALL')
                elif(res in TYPE):
                    token = TOKEN(res,'TYPE')
                else:
                    token = TOKEN(res,'VAL')
                s=s[i:]
                tokens.append(token)
            else:
                exit(token.Name+'.next is not legal')
    
    for i,t in enumerate(tokens):#处理函数名
        if(t.Name in FUNCTABLE.keys()):
            t.Type=FUNC_CALL
        try:
            if(t.Type=='VAL' and tokens[i+1].Name=='(' and tokens[i-1].Type=='TYPE'):
                t.Type=FUNC_DECLARE
                FUNCTABLE[t.Name]={'param_num':None,'return_type':tokens[i-1].Name}#返回类型在这里处理了
        except:
            pass
                   
def getNextToken():
    global point_token,token
    token = tokens[point_token]
    point_token+=1

def exchange2reg(id):
    if(id in LOCAL_VALTABLE.keys()):
        id = LOCAL_VALTABLE[id]['reg']
    elif(id in WHOLE_VALTABLE.keys()):
        id = WHOLE_VALTABLE[id]['reg']
    return id
    
def gen(opr,des,sou1=None,sou2=None):
    if(opr=='goto'):
        print((opr,des))
        MIDCODES.append((opr,des))
        return
    if(opr == 'label'):
        try:
            if((opr,des)==MIDCODES[-1]):
                return
        except:
            pass
        print(des+':')
        MIDCODES.append((opr,des))
        return
    if(opr in FUNCTION or opr in ['return','push','pop']):
        des=exchange2reg(des)
        print((opr,des))
        MIDCODES.append((opr,des))
        return
    
    if(opr=='load' or opr =='store'):
        des=exchange2reg(des)
    else:   
        sou1=exchange2reg(sou1)
        sou2=exchange2reg(sou2)

    if(sou1 is None and sou2 is None):
        print((opr,des))
        MIDCODES.append((opr,des))
    elif(sou2 is None):
        print((opr,des,sou1))
        MIDCODES.append((opr,des,sou1))
    else:
        print((opr,des,sou1,sou2))
        MIDCODES.append((opr,des,sou1,sou2))

def judgeVAL(idname):
    if(idname in LOCAL_VALTABLE.keys()):
        return LOCAL_VALTABLE[idname]['offset']+'($fp)'
    elif(idname in WHOLE_VALTABLE.keys()):
        return idname
    else:
        exit('val:'+idname+' is not declared')

class ASSIGN:
    def S(self):
        if(debug):
            print('S->',token.Name)

        if(token.Type=='VAL'):
            idname=judgeVAL(token.Name)
            getNextToken()
            if(token.Name=='='):
                getNextToken()
                E_reg=self.E()
                gen('store',E_reg,idname,None)
            else:
                exit("ERROR:ASSGIN.S")
        else:
            exit("ERROR:ASSGIN.S")
        
        getNextToken()
        if(token.Name==';'):
            pass
        else:
            exit("ERROR:ASSGIN.S")

    def E(self):
        if(debug):
            print('E->',token.Name)

        T_reg=self.T()
        #gen('=',E1_reg,T_reg,None)
        E1_val=T_reg
        getNextToken()
        E1_reg=self.E1(E1_val)
        E_reg=E1_reg

        return E_reg

    def E1(self,E1_val):
        if(debug):
            print('E1->',token.Name)

        if(token.Name in ADDOPR):
            opr = token.Name
            getNextToken()
            T_reg=self.T()

            E2_val=T_reg
            E2_reg=getRegt(-1)
            gen(opr,E2_reg,E1_val,T_reg)
            
            E2_val=E2_reg

            getNextToken()
            E2_reg=self.E1(E2_val)
            E1_reg=E2_reg

            return E1_reg
        else:
            E1_reg = E1_val
            tokenBack()
            return E1_reg

    def T(self):
        if(debug):
            print('T->',token.Name)

        Fval=self.F()
        #T1_reg = Fval
        getNextToken()
        T1_val=Fval
        T1_reg=self.T1(T1_val)  
        T_reg=T1_reg

        return T_reg

    def T1(self,T1_val):
        if(debug):
            print('T1->',token.Name)
        

        if(token.Name in MULOPR):
            opr = token.Name
            getNextToken()
            Fval=self.F()
            
            T2_reg = getRegt(-1)
            gen(opr,T2_reg,T1_val,Fval)
            
            T2_val=T2_reg

            getNextToken()
            T2_reg=self.T1(T2_val)
            T1_reg=T2_reg
            return T1_reg
        else:
            T1_reg = T1_val
            tokenBack()
            return T1_reg

    def F(self):
        if(debug):
            print('F->',token.Name)


        if(token.Type==FUNC_CALL):
            FUNC().CALL()
            temp_reg=getRegt(0)
            gen('=',temp_reg,'$v0')
            
            return temp_reg
        elif(token.Type=="VAL"):
            idname=judgeVAL(token.Name)
            temp_reg=getRegt(0)
            gen('load',temp_reg,idname,None)
            
            if(idname==token.Name):#如果是全局变量
                WHOLE_VALTABLE[token.Name]['reg']=temp_reg
            else:
                LOCAL_VALTABLE[token.Name]['reg']=temp_reg
            Fval = token.Name
            return Fval
        elif(token.Type=='DIGIT'):
            Fval = token.Name
            return Fval
        elif(token.Name=='('):
            getNextToken()
            E_reg = self.E()
            F_val = E_reg
            getNextToken()
            if(token.Name==')'):
                return F_val
            else:
                exit('expect )')
        else:
            exit('val:'+token.Name+' is not legal')

class DECLARE:
    def LD(self):
        initVal='0'

        T_type=self.T()
        getNextToken()
        if(token.Type!='VAL'):
            exit("declare:NOT VAL")
        idname = token.Name
        getNextToken()
        if(token.Name==';'):
            pass
        elif(token.Name=='='):
            getNextToken()
            
            if(token.Type=='DIGIT'):
                initVal=token.Name
                getNextToken()
                if(token.Name!=';'):
                    exit('expect ;')
            else:
                exit('declare wrong')
        else:
            exit('declare wrong')

        global stack_offset
        LOCAL_VALTABLE[idname]={'type':T_type,'width':4,'offset':str(stack_offset),'value':initVal,'reg':None}
        gen('push',initVal)
        stack_offset-=4
    
    def WD(self):
        initVal='0'

        T_type=self.T()
        getNextToken()
        if(token.Type!='VAL'):
            exit("declare:NOT VAL")
        idname = token.Name
        getNextToken()
        if(token.Name==';'):
            pass
        elif(token.Name=='='):
            getNextToken()
            
            if(token.Type=='DIGIT'):
                initVal=token.Name
                getNextToken()
                if(token.Name!=';'):
                    exit('expect ;')
            else:
                exit('declare wrong')
        else:
            exit('declare wrong')
        global offset
        WHOLE_VALTABLE[idname]={'type':T_type,'width':4,'offset':offset,'value':initVal,'reg':None}
        MEMTABLE[offset]=idname
        offset+=4

    def T(self):
        if(token.Type=='TYPE'):
            if(token.Name=='int'):
                T_type='int'
                return T_type
        else:
            exit("declare:wrong KEY")
    
    def param_list(self):#(int a,int b,int c) 参数列表
        index=0
        temp_valtable={}
        if(token.Name!='('):
            exit('param_declare list lack (')
        getNextToken()
        while(1):
            if(token.Type=='TYPE'):
                temp_type=token.Name
            elif(token.Name==')'):
                return temp_valtable,index
                break
            else:
                exit('param_declare TYPE wrong')
            getNextToken()
            if(token.Type=='VAL'):
                temp_valtable[token.Name]={'type':temp_type,'width':4,'offset':str(8+4*index),'reg':None}#ret在4($fp),第一个参数在8($fp)
                index=index+1
            else:
                exit('param_declare not VAL')
            
            getNextToken()
            if(token.Name==','):
                getNextToken()
            elif(token.Name==')'):
                return temp_valtable,index
                break
            else:
                exit('param_declare BOUND wrong')

class SYSTEMCALL:
    def S(self):
        opr = token.Name
        para = None
        getNextToken()
        if(token.Name!='('):
            exit('expect (')
        getNextToken()
        E_reg=ASSIGN().E()
        getNextToken()
        if(token.Name!=')'):
            exit('expect )')
        getNextToken()
        if(token.Name!=';'):
            exit('expect ;')
        gen(opr,E_reg)

class IF:
    def S(self,S_next):
        getNextToken()
        if(token.Name!='('):
            exit('if:expect (')

        getNextToken()
        B_true=newLable()
        B_false=S1_next=S_next
        self.B(B_true,B_false)
        gen('label',B_true)

        getNextToken()
        if(token.Name!=')'):
            exit('if:expect )')

        getNextToken()
        if(token.Name!='{'):
            PROGRAM().single_S(S1_next)
            gen('label',S_next)
            
        else:
            getNextToken()
            PROGRAM().multi_S()
            gen('label',S_next)

            getNextToken()
            if(token.Name!='}'):
                exit('if:expect }')

    def S_else(self,S_next):
        getNextToken()
        if(token.Name!='('):
            exit('if:expect (')

        getNextToken()
        B_true=newLable()
        B_false=newLable()
        S1_next=S2_next=S_next
        self.B(B_true,B_false)
        gen('label',B_true)

        getNextToken()
        if(token.Name!=')'):
            exit('if:expect )')

        getNextToken()
        if(token.Name!='{'):
            PROGRAM().single_S(S1_next)

        else:
            getNextToken()
            PROGRAM().multi_S()

            getNextToken()
            if(token.Name!='}'):
                exit('if:expect }')
        
        getNextToken()
        if(token.Name!='else'):
            exit('if:expect else')
        
        getNextToken()
        gen('goto',S_next)
        gen('label',B_false)
        if(token.Name!='{'):
            PROGRAM().single_S(S2_next)
            gen('label',S_next)
            
        else:
            getNextToken()
            PROGRAM().multi_S()
            gen('label',S_next)

            getNextToken()
            if(token.Name!='}'):
                exit('if:expect }')


    def B(self,B_true,B_false):
        if(debug):
            print('B->',token.Name)
        E1_reg=ASSIGN().E()

        getNextToken()

        if(token.Name in COMPOPR):
            cmp=token.Name
        else:
            exit('BOOL:not a cmp opr')

        getNextToken()
        E2_reg=ASSIGN().E()
        gen(cmp,B_true,E1_reg,E2_reg)
        gen('goto',B_false)
    
    def isHaveElse(self):
        p=point_token

        while(tokens[p].Name!=')'):
            p+=1
        if(tokens[p+1].Name=='{'):
            seen=0
            times=0
            for p in range(point_token,len(tokens)):
                now_token=tokens[p]
                if(now_token.Name=='{'):
                    seen=1
                    times+=1
                elif(now_token.Name=='}'):
                    times-=1
                if(seen==1 and times==0):
                    try:
                        if(tokens[p+1].Name=='else'):
                            return True
                        else:
                            return False
                    except:
                        pass
            return False
        else:
            while(1):
                idname=tokens[p].Name
                if(idname=='if'):
                    return False
                if(idname=='else'):
                    return True
                p+=1
                if(p>=len(tokens)):
                    return False
        
class LOOP:
    def W(self,S_next):
        getNextToken()
        if(token.Name!='('):
            exit('if:expect (')

        getNextToken()
        begin=newLable()
        B_true=newLable()
        B_false=S_next
        S1_next=begin
        gen('label',begin)
        IF().B(B_true,B_false)

        getNextToken()
        if(token.Name!=')'):
            exit('if:expect )')

        getNextToken()
        if(token.Name!='{'):
            exit('if:expect {')

        getNextToken()
        gen('label',B_true)
        PROGRAM().multi_S()
        
        gen('goto',begin)
        gen('label',S_next)

        getNextToken()
        if(token.Name!='}'):
            exit('if:expect }')

class FUNC:#函数的寄存器分配与保护还存在问题
    def CALL(self):#解析调用
        if(token.Type==FUNC_CALL):
            Fname=token.Name
        else:
            exit("CALL name wrong")
        
        getNextToken()
        if(token.Name!='('):
            exit("CALL lack (")
        
        getNextToken()
        nums=0
        stack=[]
        while(1):
            E_reg=ASSIGN().E()
            stack.append(E_reg)#参数需要反向压栈
            nums+=1

            getNextToken()
            if(token.Name==')'):
                break
            elif(token.Name==','):
                getNextToken()
        
        if(FUNCTABLE[Fname]['param_num']!=nums):
            exit('func:'+Fname+' param_num not match')
        stack.reverse()
        for E_reg in stack:
            gen('push',E_reg)
        gen('call',Fname)
        
    

class PROGRAM:
    def P(self):
        self.whole_declare()
        self.func_declare()
        self.void_main()

    def func_declare(self):
        init_func()
        if(token.Type!='TYPE'):
            exit('func declare wrong')
        if(token.nextToken().Name=='main'):
            return
        ret_type=token.Name

        getNextToken()
        if(token.Type!=FUNC_DECLARE):
            exit('func name doesn\'t exist')
        Fname=token.Name

        getNextToken()
        global LOCAL_VALTABLE
        LOCAL_VALTABLE,param_num=DECLARE().param_list()#解析参数列表
        FUNCTABLE[Fname]['param_num']=param_num

        getNextToken()
        if(token.Name!='{'):
            exit('func:'+Fname+' lack {')
        
        getNextToken()
        func_head(Fname)

        self.multi_S()
        func_end()
        getNextToken()
        if(token.Name!='}'):
            exit('main func lack {')
        getNextToken()

    def whole_declare(self):#全局定义段
        while(1):
            if(token.Name in TYPE):
                if(token.nextToken().Type==FUNC_DECLARE):
                    print('whole_declare end')
                    break
                DECLARE().WD()
            else:
                exit('whole_declare wrong')
        
            if(point_token<len(tokens)):
                getNextToken()
            else:
                exit('lack main func')

    def void_main(self):#主程序段
        init_func()
        if(token.Name!='void'):
            exit('main must be void')
        getNextToken()
        if(token.Name!='main'):
            exit('main func name wrong')
        getNextToken()
        global LOCAL_VALTABLE
        LOCAL_VALTABLE,param_num=DECLARE().param_list()#解析参数列表
        FUNCTABLE['main']['param_num']=param_num
        getNextToken()
        if(token.Name!='{'):
            exit('main func lack {')
        getNextToken()

        func_head('main')
        
        self.multi_S()

        getNextToken()
        if(token.Name!='}'):
            exit('main func lack {')

    def multi_S(self):#P为多个语句序列，被{}包裹
        if(debug):
            print('P->',token.Name)
        while(1):
            S_next=newLable()
            self.S(S_next)
            gen('label',S_next)
            
            if(point_token<len(tokens)):
                getNextToken()
                if(token.Name=='}'):
                    tokenBack()
                    break
            else:
                break
        
    
    def S(self,S_next):#S为一个语句序列，比如一个连续的赋值语句块，或者一个if块、while块
        if(debug):
            print('S->',token.Name)
        init_sentence()

        if(token.Name=='if'):
            i = IF()
            if(i.isHaveElse()):
                i.S_else(S_next)
            else:
                i.S(S_next)

        
        elif(token.Name=='while'):
            LOOP().W(S_next)

        else:
            while(1):
                init_sentence()
                if(token.Name=='return'):
                    getNextToken()
                    E_reg=ASSIGN().E()
                    gen('return',E_reg)
                    getNextToken()
                    if(token.Name!=';'):
                        exit('expect ;')

                elif(token.Name in TYPE):
                    DECLARE().LD()

                elif(token.Type=='SYSCALL'):
                    SYSTEMCALL().S()

                elif(token.Type=='VAL'):
                    ASSIGN().S()
                if(point_token<len(tokens)):
                    getNextToken()
                    if(token.Name in ['}','if','while','return']):
                        tokenBack()
                        break
                else:
                    break
    
    def single_S(self,S_next):#一条赋值语句，或者一个if块、while块
        if(debug):
            print('S->',token.Name)
        init_sentence()

        if(token.Name=='if'):
            i = IF()
            if(i.isHaveElse()):
                i.S_else(S_next)
            else:
                i.S(S_next)

        
        elif(token.Name=='while'):
            LOOP().W(S_next)

        else:
            if(token.Name=='return'):
                getNextToken()
                E_reg=ASSIGN().E()
                gen('return',E_reg)
                getNextToken()
                if(token.Name!=';'):
                    exit('expect ;')

            elif(token.Name in TYPE):
                DECLARE().LD()

            elif(token.Type=='SYSCALL'):
                SYSTEMCALL().S()
            elif(token.Type=='VAL'):
                ASSIGN().S()
        


with open('test/c.txt','r') as f:
    s=f.read()
getTokens(s)
# for i in tokens:
#     i.show()

if(tokens[-1].Name!=';' and tokens[-1].Name!='}'):
    exit('expect Last BOUND')
getNextToken()

PROGRAM().P()


print(WHOLE_VALTABLE)
print(LOCAL_VALTABLE)

seg_show()
