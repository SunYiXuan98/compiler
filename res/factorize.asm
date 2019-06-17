.data
string0:	.asciiz	"="
string1:	.asciiz	"*"
string2:	.asciiz	"*"
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
factorize:
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
li	$t9,2
sw	$t9,-4($fp)
li	$t9,1
sw	$t9,-8($fp)
lw	$t0,8($fp)
li	$v0,1
move	$a0,$t0
syscall
li	$v0,4
la	$a0,string0
syscall
L5:
L7:
lw	$t0,8($fp)
lw	$t1,-4($fp)
lw	$t2,-4($fp)
mul	$t2,$t1,$t2
bge	$t0,$t2,L8
j	L6
L8:
L10:
lw	$t0,8($fp)
lw	$t1,-4($fp)
addi	$sp,$sp,-8
sw	$t0,0($sp)
sw	$t1,4($sp)
jal	mod
addi	$sp,$sp,8
move	$t1,$v0
beq	$t1,0,L11
j	L9
L11:
lw	$t0,-8($fp)
bne	$t0,0,L13
j	L14
L13:
lw	$t0,-4($fp)
li	$v0,1
move	$a0,$t0
syscall
li	$t9,0
sw	$t9,-8($fp)
L15:
j	L12
L14:
li	$v0,4
la	$a0,string1
syscall
lw	$t0,-4($fp)
li	$v0,1
move	$a0,$t0
syscall
L16:
L12:
lw	$t0,8($fp)
lw	$t1,-4($fp)
div	$t1,$t0,$t1
sw	$t1,8($fp)
L17:
j	L10
L9:
lw	$t0,-4($fp)
addi	$t0,$t0,1
sw	$t0,-4($fp)
L18:
j	L7
L6:
lw	$t0,8($fp)
bne	$t0,1,L20
j	L19
L20:
lw	$t0,-8($fp)
bne	$t0,0,L22
j	L23
L22:
lw	$t0,8($fp)
li	$v0,1
move	$a0,$t0
syscall
li	$t9,0
sw	$t9,-8($fp)
L24:
j	L21
L23:
li	$v0,4
la	$a0,string2
syscall
lw	$t0,8($fp)
li	$v0,1
move	$a0,$t0
syscall
L25:
L21:
L19:
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
jal	factorize
addi	$sp,$sp,4
L26:
