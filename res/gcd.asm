.data
.text
j	main
gcd:
addi	$sp,$sp,-8
sw	$fp,0($sp)
sw	$ra,4($sp)
move	$fp,$sp
addi	$sp,$sp,-4
li	$t9,0
sw	$t9,0($sp)
L0:
L2:
lw	$t0,12($fp)
bne	$t0,0,L3
j	L1
L3:
lw	$t0,8($fp)
sw	$t0,-4($fp)
L4:
L6:
lw	$t0,-4($fp)
lw	$t1,12($fp)
bge	$t0,$t1,L7
j	L5
L7:
lw	$t0,-4($fp)
lw	$t1,12($fp)
sub	$t1,$t0,$t1
sw	$t1,-4($fp)
L8:
j	L6
L5:
lw	$t0,12($fp)
sw	$t0,8($fp)
lw	$t0,-4($fp)
sw	$t0,12($fp)
L9:
j	L2
L1:
lw	$t0,8($fp)
move	$sp,$fp
lw	$fp,0($sp)
addi	$sp,$sp,4
lw	$ra,0($sp)
addi	$sp,$sp,4
move	$v0,$t0
jr	$ra
L10:
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
addi	$sp,$sp,-4
li	$t9,0
sw	$t9,0($sp)
L11:
L13:
lw	$t0,-12($fp)
ble	$t0,3,L14
j	L12
L14:
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
jal	gcd
addi	$sp,$sp,8
move	$t1,$v0
li	$v0,1
move	$a0,$t1
syscall
lw	$t0,-12($fp)
addi	$t0,$t0,1
sw	$t0,-12($fp)
L15:
j	L13
L12:
