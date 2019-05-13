# coding=utf-8
import re

     

class MIPS:
    def __init__(self,opr,des,r1=None,r2=None):
        self.opr = opr
        self.des = des
        self.r1 = r1
        self.r2 = r2
    
    def show(self):
        if(self.r1 is None):
            if(self.opr=='call'):
                print('jal\t'+self.des)
            elif(self.opr=='protect'):
                self.des.reverse()
                num_reg = len(self.des)
                if(num_reg==0):
                    return
                print('addi\t$sp,$sp,'+str(-4*num_reg))
                for t in range(num_reg):
                    reg=self.des[t]
                    try:
                        int(reg)
                        print('li\t$t9,'+reg)
                        print('sw\t$t9,'+str(t*4)+'($sp)')
                    except:
                        print('sw\t'+reg+','+str(t*4)+'($sp)')
            
            elif(self.opr=='free'):
                if(isinstance(self.des,int)):
                    print('addi\t$sp,$sp,'+str(4*self.des))
                else:
                    num_reg = len(self.des)
                    if(num_reg==0):
                        return
                    for t in range(num_reg):
                        reg=self.des[t]
                        print('lw\t'+reg+','+str(t*4)+'($sp)')
                    print('addi\t$sp,$sp,'+str(4*num_reg))

            elif(self.opr=='return'):
                print('move\t$sp,$fp')
                print('lw\t$fp,0($sp)')
                print('addi\t$sp,$sp,4')
                print('lw\t$ra,0($sp)')
                print('addi\t$sp,$sp,4')
                if(self.des):
                    try:
                        int(self.des)
                        print('li\t$v0,'+self.des)
                    except:
                        print('move\t$v0,'+self.des)
                            
                print('jr\t$ra')                    
            elif(self.opr=='push'):
                print('addi\t$sp,$sp,-4')
                try:
                    int(self.des)
                    print('li\t$t9,'+self.des)
                    print('sw\t$t9,'+'0($sp)')
                except:
                    print('sw\t'+self.des+',0($sp)')
            elif(self.opr=='pop'):
                print('lw\t'+self.des+',0($sp)')
                print('addi\t$sp,$sp,4')
            elif(self.opr=='label'):
                print(self.des+':')
            elif(self.opr=='goto'):
                print('j\t'+self.des)
            elif(self.opr=='scanf'):
                print('li\t$v0,5')
                print('syscall')
                print('sw\t$v0'+','+self.des)
        elif(self.r2 is None):#I
            if(self.opr=='='):#mov
                print('move\t'+self.des+','+self.r1)
            
            elif(self.opr=='printf'):#printf
                if(self.r1=='string'):
                    print('li\t$v0,4')
                    print('la\t$a0,'+self.des)
                    print('syscall')
                else:
                    print('li\t$v0,1')
                    print('move\t$a0,'+self.des)
                    print('syscall')

            elif(self.opr=='load'):#lw
                print('lw\t'+self.des+','+self.r1)

            elif(self.opr=='store'):#sw
                try:
                    int(self.des)
                    print('li\t$t9,'+self.des)
                    print('sw\t$t9,'+self.r1)
                except:
                    print('sw\t'+self.des+','+self.r1)

        else:#J
            try:
                int(self.r1)
                print('li\t$t8,'+self.r1)
                self.r1='$t8'
            except:
                pass
            if(self.opr=='+'):#add
                try:
                    int(self.r2)
                    print('addi\t'+self.des+','+self.r1+','+self.r2)
                except:
                    print('add\t'+self.des+','+self.r1+','+self.r2)

            elif(self.opr=='-'):#sub
                try:
                    int(self.r2)
                    print('subi\t'+self.des+','+self.r1+','+self.r2)
                except:
                    print('sub\t'+self.des+','+self.r1+','+self.r2)
            
            else:
                try:
                    int(self.r2)
                    print('li\t$s2,'+self.r2)
                    self.r2='$s2'
                except:
                    pass

                if(self.opr=='*'):#mult
                    print('mult\t'+self.r1+','+self.r2)
                    print('mflo\t'+self.des)
                    
                elif(self.opr=='/'):#div
                    print('div\t'+self.r1+','+self.r2)
                    print('mflo\t'+self.des)
                
                elif(self.opr=='=='):#beq
                    print('beq\t'+self.r1+','+self.r2+','+self.des)

                elif(self.opr=='!='):#bne
                    print('bne\t'+self.r1+','+self.r2+','+self.des)
                
                elif(self.opr=='>='):#bge
                    print('bge\t'+self.r1+','+self.r2+','+self.des)

                elif(self.opr=='<='):#ble
                    print('ble\t'+self.r1+','+self.r2+','+self.des)
                
                elif(self.opr=='>'):#bgt
                    print('bgt\t'+self.r1+','+self.r2+','+self.des)
                
                elif(self.opr=='<'):#blt
                    print('blt\t'+self.r1+','+self.r2+','+self.des)


def seg_show():
    print('\n'*2)
    print('.data')
    for val in WHOLE_VALTABLE.keys():
        Type = '.word' if WHOLE_VALTABLE[val]['width']==4 else '.byte'
        print(val+':\t'+Type+'\t'+WHOLE_VALTABLE[val]['value'])
    for name in WHOLE_STRING.keys():
        print(name+':\t.ascii\t'+WHOLE_STRING[name])
    print('.text')
    print('j\tmain')
    for four in MIDCODES:
        mips_code = Tran2Mips(four)
        mips_code.show()

def Tran2Mips(FourCode):
    mips = MIPS(*FourCode)
    return mips



'''
VAL : abc,a1,a_s2
SCA : 12,1.2
KEY : if,else,when
OPR : +,-,*,/
BOUND:(),{},=
'''
OPR = ['+','-','*','/','<','>','<=','>=','==','!=','!','||','&&','=']
ADDOPR = ['+','-']
MULOPR = ['*','/']
COMPOPR = ['<','>','<=','>=','==','!=']
LOGICOPR = ['!','||','&&']

KEY = ['auto','break','case','const','continue','default','do','else','enum','extern','for','goto','if',
    'long','register','return','short','signed','sizeof','static','struct','switch','typedef','unsigned','union','volatile','while']
DIGIT = ['0','1','2','3','4','5','6','7','8','9']
BOUND = ['(',')','{','}','[',']',';',',']
FUNCTION = ['printf','scanf']
TYPE = ['int','void']
WS = [' ','\n','\t']


offset = 0
stack_offset = -4

tokens = []
token = None
MIDCODES=[]

REG_USED=set([])
WHOLE_VALTABLE={}#全局、静态数据区 {'type':T_type,'width':4,'offset':offset,'value':initVal,'reg':None,'const':False}
LOCAL_VALTABLE={}#记录局部变量在栈中的位置 LOCAL_VALTABLE[idname]={'type':T_type,'width':4,'offset':str(stack_offset),'value':initVal,'reg':None,'const':False}
MEMTABLE={}#MEMTABLE[offset]=idname
FUNCTABLE={}#{'param_num':None,'return_type':tokens[i-1].Name}
NOWFUNC=None

FUNC_CALL='FUNC_CALL'
FUNC_DECLARE='FUNC_DECLARE'

ISLOCAL='islocal'
ISWHOLE='iswhole'
ISCONST=False

WHOLE_STRING={}