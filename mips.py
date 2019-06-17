# coding=utf-8
# 中间代码与MIPS汇编的转换

from define import *
from optimize import *


def writeANDprint(s):
    print(s)
    RESULT.append(s)

#中间代码转MIPS汇编
class MIPS:
    def __init__(self,opr,des,r1=None,r2=None):
        self.opr = opr
        self.des = des
        self.r1 = r1
        self.r2 = r2
    
    def show(self):
        if(self.r1 is None):
            if(self.opr=='call'):
                writeANDprint('jal\t'+self.des)
            elif(self.opr=='protect'):
                self.des.reverse()
                num_reg = len(self.des)
                if(num_reg==0):
                    return
                writeANDprint('addi\t$sp,$sp,'+str(-4*num_reg))
                for t in range(num_reg):
                    reg=self.des[t]
                    try:
                        int(reg)
                        writeANDprint('li\t$t9,'+reg)
                        writeANDprint('sw\t$t9,'+str(t*4)+'($sp)')
                    except:
                        writeANDprint('sw\t'+reg+','+str(t*4)+'($sp)')
            
            elif(self.opr=='free'):
                if(isinstance(self.des,int)):
                    writeANDprint('addi\t$sp,$sp,'+str(4*self.des))
                else:
                    num_reg = len(self.des)
                    if(num_reg==0):
                        return
                    for t in range(num_reg):
                        reg=self.des[t]
                        writeANDprint('lw\t'+reg+','+str(t*4)+'($sp)')
                    writeANDprint('addi\t$sp,$sp,'+str(4*num_reg))
            elif(self.opr=='newstack'):
                writeANDprint('addi\t$sp,$sp,'+str(-4*int(self.des)))
            elif(self.opr=='return'):
                writeANDprint('move\t$sp,$fp')
                writeANDprint('lw\t$fp,0($sp)')
                writeANDprint('addi\t$sp,$sp,4')
                writeANDprint('lw\t$ra,0($sp)')
                writeANDprint('addi\t$sp,$sp,4')
                if(self.des):
                    try:
                        int(self.des)
                        writeANDprint('li\t$v0,'+self.des)
                    except:
                        writeANDprint('move\t$v0,'+self.des)
                            
                writeANDprint('jr\t$ra')                    
            elif(self.opr=='push'):
                writeANDprint('addi\t$sp,$sp,-4')
                try:
                    int(self.des)
                    writeANDprint('li\t$t9,'+self.des)
                    writeANDprint('sw\t$t9,'+'0($sp)')
                except:
                    writeANDprint('sw\t'+self.des+',0($sp)')
            elif(self.opr=='pop'):
                writeANDprint('lw\t'+self.des+',0($sp)')
                writeANDprint('addi\t$sp,$sp,4')
            elif(self.opr=='label'):
                writeANDprint(self.des+':')
            elif(self.opr=='goto'):
                writeANDprint('j\t'+self.des)
            elif(self.opr=='scanf'):
                writeANDprint('li\t$v0,5')
                writeANDprint('syscall')
                writeANDprint('sw\t$v0'+','+self.des)
        elif(self.r2 is None):#I
            if(self.opr=='='):#mov
                writeANDprint('move\t'+self.des+','+self.r1)
            
            elif(self.opr=='printf'):#printf
                if(self.r1=='string'):
                    writeANDprint('li\t$v0,4')
                    writeANDprint('la\t$a0,'+self.des)
                    writeANDprint('syscall')
                else:
                    writeANDprint('li\t$v0,1')
                    try:
                        int(self.des)
                        writeANDprint('li\t$a0,'+self.des)
                    except:
                        writeANDprint('move\t$a0,'+self.des)
                    writeANDprint('syscall')

            elif(self.opr=='load'):#lw
                writeANDprint('lw\t'+self.des+','+self.r1)

            elif(self.opr=='store'):#sw
                try:
                    int(self.des)
                    writeANDprint('li\t$t9,'+self.des)
                    writeANDprint('sw\t$t9,'+self.r1)
                except:
                    writeANDprint('sw\t'+self.des+','+self.r1)

        else:#J
            try:
                int(self.r1)
                writeANDprint('li\t$t8,'+self.r1)
                self.r1='$t8'
            except:
                pass
            if(self.opr=='+'):#add
                try:
                    int(self.r2)
                    writeANDprint('addi\t'+self.des+','+self.r1+','+self.r2)
                except:
                    writeANDprint('add\t'+self.des+','+self.r1+','+self.r2)

            elif(self.opr=='-'):#sub
                try:
                    int(self.r2)
                    writeANDprint('subi\t'+self.des+','+self.r1+','+self.r2)
                except:
                    writeANDprint('sub\t'+self.des+','+self.r1+','+self.r2)
            
            else:
                if(self.opr=='*'):#mul
                    writeANDprint('mul\t'+self.des+','+self.r1+','+self.r2)
                    
                elif(self.opr=='/'):#div
                    writeANDprint('div\t'+self.des+','+self.r1+','+self.r2)
                
                elif(self.opr=='<<'):#sll
                    writeANDprint('sll\t'+self.des+','+self.r1+','+self.r2)

                elif(self.opr=='>>'):#sra
                    writeANDprint('sra\t'+self.des+','+self.r1+','+self.r2)
                
                elif(self.opr=='=='):#beq
                    writeANDprint('beq\t'+self.r1+','+self.r2+','+self.des)

                elif(self.opr=='!='):#bne
                    writeANDprint('bne\t'+self.r1+','+self.r2+','+self.des)
                
                elif(self.opr=='>='):#bge
                    writeANDprint('bge\t'+self.r1+','+self.r2+','+self.des)

                elif(self.opr=='<='):#ble
                    writeANDprint('ble\t'+self.r1+','+self.r2+','+self.des)
                
                elif(self.opr=='>'):#bgt
                    writeANDprint('bgt\t'+self.r1+','+self.r2+','+self.des)
                
                elif(self.opr=='<'):#blt
                    writeANDprint('blt\t'+self.r1+','+self.r2+','+self.des)
                
                elif(self.opr=='arraylocal'):
                    writeANDprint("la\t"+self.des+','+self.r1)
                    try:
                        int(self.r2)
                        self.r2=str(int(self.r2)*4)
                    except:
                        writeANDprint('mul\t'+self.r2+','+self.r2+',4')
                    
                    writeANDprint('sub\t'+self.des+','+self.des+','+self.r2)
                
                elif(self.opr=='arraywhole'):
                    writeANDprint("la\t"+self.des+','+self.r1)
                    try:
                        int(self.r2)
                        self.r2=str(int(self.r2)*4)
                    except:
                        writeANDprint('mul\t'+self.r2+','+self.r2+',4')
                    
                    writeANDprint('add\t'+self.des+','+self.des+','+self.r2)

#段信息以及窥孔优化
def seg_show(filename):
    window_optimize()#窥孔优化
    print('窥孔优化后:')
    for i in MIDCODES:
        print(i)
    
    print('\n'*2)
    writeANDprint('.data')
    #全局变量以及string声明
    for val in WHOLE_VALTABLE.keys():
        if(WHOLE_VALTABLE[val]['array']):
            writeANDprint(val+':\t.space\t'+str(WHOLE_VALTABLE[val]['width']))
        else:
            Type = '.word' if WHOLE_VALTABLE[val]['width']==4 else '.byte'
            writeANDprint(val+':\t'+Type+'\t'+WHOLE_VALTABLE[val]['value'])
    for name in WHOLE_STRING.keys():
        writeANDprint(name+':\t.asciiz\t'+WHOLE_STRING[name])
    writeANDprint('.text')
    writeANDprint('j\tmain')

    #四元式转MIPS汇编
    for four in MIDCODES:
        mips_code = Tran2Mips(four)
        mips_code.show()

    with open('res/'+filename+'.asm','w') as f:
        for i in RESULT:
            f.write(i+"\n")

def Tran2Mips(FourCode):
    mips = MIPS(*FourCode)
    return mips