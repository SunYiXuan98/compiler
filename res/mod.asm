.data
.text
j	main
mod:
addi	$sp,$sp,-8
sw	$fp,0($sp)
sw	$ra,4($sp)
move	$fp,$sp
L1:
lw	$t0,8($fp)
lw	$t1,12($fp)
bge	$t0,$t1,L2
j	L0
L2:
lw	$t0,8($fp)
lw	$t1,12($fp)
sub	$t1,$t0,$t1
sw	$t1,8($fp)
L3:
j	L1
L0:
lw	$t0,8($fp)
move	$sp,$fp
lw	$fp,0($sp)
addi	$sp,$sp,4
lw	$ra,0($sp)
addi	$sp,$sp,4
move	$v0,$t0
jr	$ra
L4:
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
addi	$sp,$sp,-4
li	$t9,0
sw	$t9,0($sp)
li	$v0,5
syscall
sw	$v0,-4($fp)
li	$v0,5
syscall
sw	$v0,-8($fp)
lw	$t0,-4($fp)
lw	$t1,-8($fp)
addi	$sp,$sp,-8
sw	$t0,0($sp)
sw	$t1,4($sp)
jal	mod
addi	$sp,$sp,8
move	$t1,$v0
li	$v0,1
move	$a0,$t1
syscall
L5:
