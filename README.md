# compiler

开发环境：vscode+python3  
运行环境：python 3.5  
开发人员：syx  

功能：将基本C语言程序编译为MIPS汇编并且可以在MARS上模拟运行  
包括词法分析、文法分析、中间代码生成、中间代码转汇编等过程。

实现级别：与C0文法难度相似。  

文件简介：  
define.py:定义各种全局变量  
optimize.py:对中间代码进行窥孔优化  
mips.py:负责中间代码转汇编的过程(后端)  
main.py:词法分析、文法分析、中间代码生成(前端)以及main函数  
test文件夹：各种C程序测试文件.txt  
res文件夹：生成对应的汇编结果.asm  

测试:  
只需输入测试文件的名称即可，自动在res文件夹中生成汇编结果  
之后请将汇编结果复制到MARS中模拟运行观察效果  
exp:  
-python main.py  
-array  





