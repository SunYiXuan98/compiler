.data
string0:	.asciiz	" "
.text
j	main
fib:
addi	$sp,$sp,-8
sw	$fp,0($sp)
sw	$ra,4($sp)
move	$fp,$sp
lw	$t0,8($fp)
beq	$t0,0,L1
j	L2
L1:
move	$sp,$fp
lw	$fp,0($sp)
addi	$sp,$sp,4
lw	$ra,0($sp)
addi	$sp,$sp,4
li	$v0,1
jr	$ra
j	L0
L2:
lw	$t0,8($fp)
beq	$t0,1,L3
j	L4
L3:
move	$sp,$fp
lw	$fp,0($sp)
addi	$sp,$sp,4
lw	$ra,0($sp)
addi	$sp,$sp,4
li	$v0,1
jr	$ra
j	L0
L4:
lw	$t0,8($fp)
subi	$t0,$t0,1
addi	$sp,$sp,-4
sw	$t0,0($sp)
jal	fib
addi	$sp,$sp,4
move	$t0,$v0
lw	$t1,8($fp)
subi	$t1,$t1,2
addi	$sp,$sp,-4
sw	$t0,0($sp)
addi	$sp,$sp,-4
sw	$t1,0($sp)
jal	fib
addi	$sp,$sp,4
lw	$t0,0($sp)
addi	$sp,$sp,4
move	$t1,$v0
add	$t1,$t0,$t1
move	$sp,$fp
lw	$fp,0($sp)
addi	$sp,$sp,4
lw	$ra,0($sp)
addi	$sp,$sp,4
move	$v0,$t1
jr	$ra
L0:
move	$sp,$fp
lw	$fp,0($sp)
addi	$sp,$sp,4
lw	$ra,0($sp)
addi	$sp,$sp,4
jr	$ra
main:
addi	$sp,$sp,-8
sw	$fp,0($sp)
sw	$ra,4($sp)
move	$fp,$sp
addi	$sp,$sp,-4
li	$t9,0
sw	$t9,0($sp)
L5:
L7:
lw	$t0,-4($fp)
ble	$t0,10,L8
j	L6
L8:
lw	$t0,-4($fp)
addi	$sp,$sp,-4
sw	$t0,0($sp)
jal	fib
addi	$sp,$sp,4
move	$t0,$v0
li	$v0,1
move	$a0,$t0
syscall
li	$v0,4
la	$a0,string0
syscall
lw	$t0,-4($fp)
addi	$t0,$t0,1
sw	$t0,-4($fp)
L9:
j	L7
L6:
