from define import *

# MIDCODE
# Index   Attribute
# 0       opr
# 1       des
# 2       sou1
# 3       sou2

def remove_duplicate():#窥孔优化消除冗余的加载和保存指令
    i=0
    while(1):
        if(i>=len(MIDCODES)-1):
            break
        firstcode=MIDCODES[i]
        secondcode=MIDCODES[i+1]
        if(firstcode[0]=='load' and secondcode[0]=='store'):
            if(firstcode[1]==secondcode[1] and firstcode[2]==secondcode[2]):
                MIDCODES.pop(i)
                MIDCODES.pop(i)
                i-=1
        i+=1

def judge(num):#判断是不是2的幂
    try:
        num = int(num)
        if num == 0 or num & (num - 1) == 0:
            res=0
            while(num>1):
                num=num>>1
                res+=1
            return res
        else:
            return False
    except:
        return False

def judge_nums(a,b):
    try:
        int(a)
        int(b)
        return True
    except:
        return False

def algebra_simplify():#代数化简
    i=0
    while(1):
        if(i>=len(MIDCODES)):
            break
        code=MIDCODES[i]
        if(code[0]=='+'):
            #+0删除
            if((code[1]==code[2] and code[3]=='0') or(code[1]==code[3] and code[2]=='0')):
                MIDCODES.pop(i)
                i-=1
            #表达式直接求值
            if(judge_nums(code[2],code[3])):
                res=str(int(code[2])+int(code[3]))
                MIDCODES[i]=('=',code[1],res)
        
        elif(code[0]=='-'):
            #-0删除
            if((code[1]==code[2] and code[3]=='0') or(code[1]==code[3] and code[2]=='0')):
                MIDCODES.pop(i)
                i-=1
            #表达式直接求值
            if(judge_nums(code[2],code[3])):
                res=str(int(code[2])-int(code[3]))
                MIDCODES[i]=('=',code[1],res)

        elif(code[0]=='*'):
            #*1删除
            if((code[1]==code[2] and code[3]=='1') or(code[1]==code[3] and code[2]=='1')):
                MIDCODES.pop(i)
                i-=1
            #*2优化
            if(judge(code[3])):
                MIDCODES[i]=('<<',code[1],code[2],str(judge(code[3])))
            if(judge(code[2])):
                MIDCODES[i]=('<<',code[1],code[3],str(judge(code[2])))
            #表达式直接求值
            if(judge_nums(code[2],code[3])):
                res=str(int(code[2])*int(code[3]))
                MIDCODES[i]=('=',code[1],res)

        elif(code[0]=='/'):
            #/1删除
            if((code[1]==code[2] and code[3]=='1') or(code[1]==code[3] and code[2]=='1')):
                MIDCODES.pop(i)
                i-=1
            #/2优化
            if(judge(code[3])):
                MIDCODES[i]=('>>',code[1],code[2],str(judge(code[3])))
            if(judge(code[2])):
                MIDCODES[i]=('>>',code[1],code[3],str(judge(code[2])))
            #表达式直接求值
            if(judge_nums(code[2],code[3])):
                res=str(int((int(code[2])/int(code[3]))))
                MIDCODES[i]=('=',code[1],res)
        i+=1


def window_optimize():
    algebra_simplify()
    while(1):
        lastlen=len(MIDCODES)
        remove_duplicate()
        nowlen=len(MIDCODES)
        if(lastlen==nowlen):
            break