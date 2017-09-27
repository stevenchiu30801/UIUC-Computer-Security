.global _main
.section .text

_main:

push	%ebp
mov	%esp, %ebp

movl $0x0b, %eax # system call number, 11

push $0x0068732f # 0 h s /
push $0x6e69622f # n i b /
movl %esp, %ebx # filename

movl $0x0, %ecx # args = NULL
movl $0x0, %edx # environment = NULL

int $0x80 # call execve

leave
ret