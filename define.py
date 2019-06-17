# coding=utf-8
import re

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


stack_offset = -4

tokens = []
token = None
MIDCODES=[]
RESULT=[]

REG_USED=set([])
WHOLE_VALTABLE={}#全局、静态数据区 {'type':T_type,'width':4,'value':initVal,'reg':None,'const':ISCONST,'array':True}
LOCAL_VALTABLE={}#记录局部变量在栈中的位置 LOCAL_VALTABLE[idname]={'type':T_type,'width':4,'offset':str(stack_offset),'value':initVal,'reg':None,'const':False}

FUNCTABLE={}#{'param_num':None,'return_type':tokens[i-1].Name}
NOWFUNC=None

FUNC_CALL='FUNC_CALL'
FUNC_DECLARE='FUNC_DECLARE'

ISLOCAL='islocal'
ISWHOLE='iswhole'
ISCONST=False#是否为const变量
ISBRANCH=False#是否在branch语句块内

WHOLE_STRING={}