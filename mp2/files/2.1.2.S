.global your_asm_fn
.section .text

your_asm_fn:

push	%ebp
mov	%esp, %ebp
sub $12, %esp
push $0xc001f00d
push $0xc105ed
push $0xacce55ed
# movl $0xc001f00d, 8(%esp)
# movl $0xc105ed, 4(%esp)
# movl $0xacce55ed, (%esp)
call practice
leave
ret
