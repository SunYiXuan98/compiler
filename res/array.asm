.data
b:	.space	80
string0:	.asciiz	" "
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
L0:
L2:
lw	$t0,-4($fp)
blt	$t0,20,L3
j	L1
L3:
lw	$t0,-4($fp)
beq	$t0,0,L5
j	L6
L5:
lw	$t0,-4($fp)
la	$t1,b
mul	$t0,$t0,4
add	$t1,$t1,$t0
li	$t9,1
sw	$t9,0($t1)
j	L4
L6:
lw	$t0,-4($fp)
beq	$t0,1,L7
j	L8
L7:
lw	$t0,-4($fp)
la	$t1,b
mul	$t0,$t0,4
add	$t1,$t1,$t0
li	$t9,1
sw	$t9,0($t1)
j	L4
L8:
lw	$t0,-4($fp)
la	$t1,b
mul	$t0,$t0,4
add	$t1,$t1,$t0
lw	$t2,-4($fp)
subi	$t2,$t2,1
la	$t3,b
mul	$t2,$t2,4
add	$t3,$t3,$t2
lw	$t4,0($t3)
lw	$t5,-4($fp)
subi	$t5,$t5,2
la	$t6,b
mul	$t5,$t5,4
add	$t6,$t6,$t5
lw	$t7,0($t6)
add	$t7,$t4,$t7
sw	$t7,0($t1)
L4:
lw	$t0,-4($fp)
la	$t1,b
mul	$t0,$t0,4
add	$t1,$t1,$t0
lw	$t2,0($t1)
li	$v0,1
move	$a0,$t2
syscall
li	$v0,4
la	$a0,string0
syscall
lw	$t0,-4($fp)
addi	$t0,$t0,1
sw	$t0,-4($fp)
L9:
j	L2
L1:
