	.text
	.file	"test.ll"
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, 16(%rsp)
	cmpl	$6, actual_max(%rip)
	jl	.LBB0_3
	.p2align	4, 0x90
.LBB0_2:                                # %while.body0
                                        # =>This Inner Loop Header: Depth=1
	movl	$2, 12(%rsp)
	addl	$-2, actual_max(%rip)
	cmpl	$6, actual_max(%rip)
	jge	.LBB0_2
.LBB0_3:                                # %while.end0
	movl	actual_max(%rip), %edi
	callq	print_int
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	actual_max,@object              # @actual_max
	.data
	.globl	actual_max
	.p2align	2
actual_max:
	.long	20                              # 0x14
	.size	actual_max, 4

	.section	".note.GNU-stack","",@progbits
