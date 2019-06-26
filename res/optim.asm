.data
.text
j	main
main:
addi	$sp,$sp,-8
sw	$fp,0($sp)
sw	$ra,4($sp)
move	$fp,$sp
addi	$sp,$sp,-4
li	$t9,3
sw	$t9,0($sp)
addi	$sp,$sp,-4
li	$t9,0
sw	$t9,0($sp)
lw	$t0,-4($fp)
sll	$t0,$t0,1
sw	$t0,-4($fp)
lw	$t0,-4($fp)
sra	$t0,$t0,1
sw	$t0,-4($fp)
lw	$t0,-4($fp)
li	$v0,1
move	$a0,$t0
syscall
L0:
