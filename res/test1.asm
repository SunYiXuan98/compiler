.data
.text
j	main
ad:
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
addi	$sp,$sp,-4
li	$t9,0
sw	$t9,0($sp)
li	$t9,0
sw	$t9,8($fp)
li	$t9,1
sw	$t9,-16($fp)
L0:
L2:
lw	$t0,-16($fp)
bne	$t0,10,L3
j	L1
L3:
lw	$t0,8($fp)
lw	$t1,-16($fp)
mul	$t1,$t0,$t1
sw	$t1,8($fp)
lw	$t0,-16($fp)
addi	$t0,$t0,1
sw	$t0,-16($fp)
L4:
j	L2
L1:
lw	$t0,8($fp)
sw	$t0,12($fp)
li	$t9,0
sw	$t9,-16($fp)
L5:
L7:
lw	$t0,12($fp)
bne	$t0,100,L8
j	L6
L8:
lw	$t0,12($fp)
lw	$t1,-16($fp)
add	$t1,$t0,$t1
sw	$t1,12($fp)
lw	$t0,-16($fp)
addi	$t0,$t0,1
sw	$t0,-16($fp)
L9:
j	L7
L6:
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
addi	$sp,$sp,-12
li	$t9,1
sw	$t9,0($sp)
li	$t9,2
sw	$t9,4($sp)
li	$t9,3
sw	$t9,8($sp)
jal	ad
addi	$sp,$sp,12
L10:
