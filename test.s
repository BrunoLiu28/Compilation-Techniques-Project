	.text
	.file	"test.ll"
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$40, %rsp
	.cfi_def_cfa_offset 48
	movq	%rdi, 32(%rsp)
	movl	$5, 12(%rsp)
	callq	getArrayRandomFloatsSize5
	movq	%rax, 16(%rsp)
	movl	$0, 8(%rsp)
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_4:                                # %if.end0
                                        #   in Loop: Header=BB0_1 Depth=1
	incl	8(%rsp)
.LBB0_1:                                # %while.cond0
                                        # =>This Inner Loop Header: Depth=1
	movl	12(%rsp), %eax
	decl	%eax
	cmpl	%eax, 8(%rsp)
	jge	.LBB0_5
# %bb.2:                                # %while.body0
                                        #   in Loop: Header=BB0_1 Depth=1
	movslq	8(%rsp), %rax
	movq	16(%rsp), %rcx
	movss	(%rcx,%rax,4), %xmm0            # xmm0 = mem[0],zero,zero,zero
	ucomiss	4(%rcx,%rax,4), %xmm0
	jbe	.LBB0_4
# %bb.3:                                # %if.then0
                                        #   in Loop: Header=BB0_1 Depth=1
	movq	16(%rsp), %rax
	movslq	8(%rsp), %rcx
	movss	(%rax,%rcx,4), %xmm0            # xmm0 = mem[0],zero,zero,zero
	movss	%xmm0, 28(%rsp)
	movss	4(%rax,%rcx,4), %xmm0           # xmm0 = mem[0],zero,zero,zero
	movss	%xmm0, (%rax,%rcx,4)
	movss	28(%rsp), %xmm0                 # xmm0 = mem[0],zero,zero,zero
	movslq	8(%rsp), %rax
	movq	16(%rsp), %rcx
	movss	%xmm0, 4(%rcx,%rax,4)
	jmp	.LBB0_4
.LBB0_5:                                # %while.end0
	movl	$0, 8(%rsp)
	.p2align	4, 0x90
.LBB0_6:                                # %while.cond1
                                        # =>This Inner Loop Header: Depth=1
	movl	8(%rsp), %eax
	cmpl	12(%rsp), %eax
	jge	.LBB0_8
# %bb.7:                                # %while.body1
                                        #   in Loop: Header=BB0_6 Depth=1
	movslq	8(%rsp), %rax
	movq	16(%rsp), %rcx
	movss	(%rcx,%rax,4), %xmm0            # xmm0 = mem[0],zero,zero,zero
	callq	print_float
	incl	8(%rsp)
	jmp	.LBB0_6
.LBB0_8:                                # %while.end1
	addq	$40, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
