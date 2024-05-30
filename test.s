	.text
	.file	"test.ll"
	.globl	fibonacci                       # -- Begin function fibonacci
	.p2align	4, 0x90
	.type	fibonacci,@function
fibonacci:                              # @fibonacci
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rbx
	.cfi_def_cfa_offset 16
	subq	$16, %rsp
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -16
	movl	%edi, 12(%rsp)
	movl	$-1, 8(%rsp)
	cmpl	$1, %edi
	jg	.LBB0_2
# %bb.1:                                # %if.then0
	movl	12(%rsp), %eax
	jmp	.LBB0_3
.LBB0_2:                                # %if.else0
	movl	12(%rsp), %edi
	decl	%edi
	callq	fibonacci
	movl	%eax, %ebx
	movl	12(%rsp), %edi
	addl	$-2, %edi
	callq	fibonacci
	addl	%ebx, %eax
.LBB0_3:                                # %if.end0
	movl	%eax, 8(%rsp)
	movl	8(%rsp), %eax
	addq	$16, %rsp
	.cfi_def_cfa_offset 16
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	fibonacci, .Lfunc_end0-fibonacci
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, 16(%rsp)
	movl	num(%rip), %edi
	callq	fibonacci
	movl	%eax, 12(%rsp)
	movl	$.L.str.0, %edi
	callq	print
	movl	12(%rsp), %edi
	callq	print_int
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	num,@object                     # @num
	.data
	.globl	num
	.p2align	2
num:
	.long	15                              # 0xf
	.size	num, 4

	.type	.L.str.0,@object                # @.str.0
	.section	.rodata.str1.16,"aMS",@progbits,1
	.p2align	4
.L.str.0:
	.asciz	"The fibonacci of the number you entered is:"
	.size	.L.str.0, 44

	.section	".note.GNU-stack","",@progbits
