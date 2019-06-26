.data
string0:	.asciiz	" "
string1:	.asciiz	"\n"
.text
j	main
main:
addi	$sp,$sp,-8
sw	$fp,0($sp)
sw	$ra,4($sp)
move	$fp,$sp
addi	$sp,$sp,-4
li	$t9,0
sw	$t9,0($sp)
addi	$sp,$sp,-4
li	$t9,0
sw	$t9,0($sp)
L0:
L2:
lw	$t0,-8($fp)
blt	$t0,10,L3
j	L1
L3:
li	$t9,0
sw	$t9,-4($fp)
L4:
L6:
lw	$t0,-4($fp)
blt	$t0,10,L7
j	L5
L7:
lw	$t0,-8($fp)
lw	$t1,-4($fp)
add	$t1,$t0,$t1
li	$v0,1
move	$a0,$t1
syscall
li	$v0,4
la	$a0,string0
syscall
lw	$t0,-4($fp)
addi	$t0,$t0,1
sw	$t0,-4($fp)
L8:
j	L6
L5:
li	$v0,4
la	$a0,string1
syscall
lw	$t0,-8($fp)
addi	$t0,$t0,1
sw	$t0,-8($fp)
L9:
j	L2
L1:
