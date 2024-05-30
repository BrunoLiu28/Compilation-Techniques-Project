	.text
	.file	"test.ll"
	.globl	isPrime                         # -- Begin function isPrime
	.p2align	4, 0x90
	.type	isPrime,@function
isPrime:                                # @isPrime
	.cfi_startproc
# %bb.0:                                # %entry
	movl	%edi, -8(%rsp)
	movb	$1, -13(%rsp)
	cmpl	$1, %edi
	jg	.LBB0_2
# %bb.1:                                # %if.then0
	movb	$0, -13(%rsp)
.LBB0_2:                                # %if.end0
	movl	$2, -12(%rsp)
	jmp	.LBB0_3
	.p2align	4, 0x90
.LBB0_6:                                # %if.end1
                                        #   in Loop: Header=BB0_3 Depth=1
	incl	-12(%rsp)
.LBB0_3:                                # %while.cond0
                                        # =>This Inner Loop Header: Depth=1
	movl	-12(%rsp), %eax
	imull	%eax, %eax
	cmpl	-8(%rsp), %eax
	jg	.LBB0_7
# %bb.4:                                # %while.body0
                                        #   in Loop: Header=BB0_3 Depth=1
	movl	$2, -4(%rsp)
	movl	-8(%rsp), %eax
	cltd
	idivl	-12(%rsp)
	testl	%edx, %edx
	jne	.LBB0_6
# %bb.5:                                # %if.then1
                                        #   in Loop: Header=BB0_3 Depth=1
	movb	$0, -13(%rsp)
	jmp	.LBB0_6
.LBB0_7:                                # %while.end0
	movb	-13(%rsp), %al
	retq
.Lfunc_end0:
	.size	isPrime, .Lfunc_end0-isPrime
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
	movl	$18, %edi
	callq	isPrime
	movzbl	%al, %edi
	andb	$1, %al
	movb	%al, 15(%rsp)
	callq	print_bool
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
