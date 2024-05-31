	.text
	.file	"test.ll"
	.globl	sumMatrix                       # -- Begin function sumMatrix
	.p2align	4, 0x90
	.type	sumMatrix,@function
sumMatrix:                              # @sumMatrix
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movl	%edi, 20(%rsp)
	movl	%esi, 16(%rsp)
	movl	$0, 4(%rsp)
	movl	$0, 8(%rsp)
	movl	$0, (%rsp)
	movl	$1, 12(%rsp)
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_5:                                # %while.end1
                                        #   in Loop: Header=BB0_1 Depth=1
	incl	8(%rsp)
.LBB0_1:                                # %while.cond0
                                        # =>This Loop Header: Depth=1
                                        #     Child Loop BB0_3 Depth 2
	movl	8(%rsp), %eax
	cmpl	16(%rsp), %eax
	jge	.LBB0_6
# %bb.2:                                # %while.body0
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	$0, (%rsp)
	.p2align	4, 0x90
.LBB0_3:                                # %while.cond1
                                        #   Parent Loop BB0_1 Depth=1
                                        # =>  This Inner Loop Header: Depth=2
	movl	(%rsp), %eax
	cmpl	20(%rsp), %eax
	jge	.LBB0_5
# %bb.4:                                # %while.body1
                                        #   in Loop: Header=BB0_3 Depth=2
	movl	4(%rsp), %edi
	callq	print_int
	movl	12(%rsp), %eax
	addl	%eax, 4(%rsp)
	movl	(%rsp), %edi
	incl	%edi
	movl	%edi, (%rsp)
	callq	print_int
	jmp	.LBB0_3
.LBB0_6:                                # %while.end0
	movl	4(%rsp), %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	sumMatrix, .Lfunc_end0-sumMatrix
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
	movl	$3, %edi
	movl	$3, %esi
	callq	sumMatrix
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
