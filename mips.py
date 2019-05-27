# coding=utf-8
# 中间代码与MIPS汇编的转换

from define import *
from optimize import *

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
            elif(self.opr=='newstack'):
                print('addi\t$sp,$sp,'+str(-4*int(self.des)))
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
                    try:
                        int(self.des)
                        print('li\t$a0,'+self.des)
                    except:
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
                if(self.opr=='*'):#mul
                    print('mul\t'+self.des,self.r1+','+self.r2)
                    
                elif(self.opr=='/'):#div
                    print('div\t'+self.des,self.r1+','+self.r2)
                
                elif(self.opr=='<<'):#sll
                    print('sll\t'+self.des,self.r1+','+self.r2)

                elif(self.opr=='>>'):#sra
                    print('sra\t'+self.des,self.r1+','+self.r2)
                
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
                
                elif(self.opr=='arraylocal'):
                    print("la\t"+self.des+','+self.r1)
                    try:
                        int(self.r2)
                        self.r2=str(int(self.r2)*4)
                    except:
                        print('mul\t'+self.r2+','+self.r2+',4')
                    
                    print('sub\t'+self.des+','+self.des+','+self.r2)
                
                elif(self.opr=='arraywhole'):
                    print("la\t"+self.des+','+self.r1)
                    try:
                        int(self.r2)
                        self.r2=str(int(self.r2)*4)
                    except:
                        print('mul\t'+self.r2+','+self.r2+',4')
                    
                    print('add\t'+self.des+','+self.des+','+self.r2)

def seg_show():
    window_optimize()#窥孔优化
    print('窥孔优化后:')
    for i in MIDCODES:
        print(i)
    
    print('\n'*2)
    print('.data')
    for val in WHOLE_VALTABLE.keys():
        if(WHOLE_VALTABLE[val]['array']):
            print(val+':\t.space\t'+str(WHOLE_VALTABLE[val]['width']))
        else:
            Type = '.word' if WHOLE_VALTABLE[val]['width']==4 else '.byte'
            print(val+':\t'+Type+'\t'+WHOLE_VALTABLE[val]['value'])
    for name in WHOLE_STRING.keys():
        print(name+':\t.asciiz\t'+WHOLE_STRING[name])
    print('.text')
    print('j\tmain')

    
    for four in MIDCODES:
        mips_code = Tran2Mips(four)
        mips_code.show()

def Tran2Mips(FourCode):
    mips = MIPS(*FourCode)
    return mips