.data
.text
j	main
factor:
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
L3:
j	L0
L2:
lw	$t0,8($fp)
subi	$t0,$t0,1
addi	$sp,$sp,-4
sw	$t0,0($sp)
jal	factor
addi	$sp,$sp,4
move	$t0,$v0
lw	$t1,8($fp)
mul	$t1,$t0,$t1
move	$sp,$fp
lw	$fp,0($sp)
addi	$sp,$sp,4
lw	$ra,0($sp)
addi	$sp,$sp,4
move	$v0,$t1
jr	$ra
L4:
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
li	$v0,5
syscall
sw	$v0,-4($fp)
lw	$t0,-4($fp)
addi	$sp,$sp,-4
sw	$t0,0($sp)
jal	factor
addi	$sp,$sp,4
move	$t0,$v0
li	$v0,1
move	$a0,$t0
syscall
L5:
