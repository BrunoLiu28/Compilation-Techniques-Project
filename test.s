	.text
	.file	"test.ll"
	.globl	ola                             # -- Begin function ola
	.p2align	4, 0x90
	.type	ola,@function
ola:                                    # @ola
	.cfi_startproc
# %bb.0:                                # %entry
	movl	$18, -4(%rsp)
	movl	$18, %eax
	retq
.Lfunc_end0:
	.size	ola, .Lfunc_end0-ola
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
	callq	ola
	movl	%eax, 12(%rsp)
	movl	%eax, %edi
	callq	print_int
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
