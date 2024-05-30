	.text
	.file	"test.ll"
	.globl	isLeapYear                      # -- Begin function isLeapYear
	.p2align	4, 0x90
	.type	isLeapYear,@function
isLeapYear:                             # @isLeapYear
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
                                        # kill: def $edi killed $edi def $rdi
	movl	%edi, 4(%rsp)
	movb	$0, 3(%rsp)
	leal	3(%rdi), %ecx
	testl	%edi, %edi
	cmovnsl	%edi, %ecx
	andl	$-4, %ecx
	xorl	%eax, %eax
	cmpl	%ecx, %edi
	sete	%al
	imull	$-1030792151, %edi, %ecx        # imm = 0xC28F5C29
	addl	$85899344, %ecx                 # imm = 0x51EB850
	rorl	$2, %ecx
	xorl	%esi, %esi
	cmpl	$42949673, %ecx                 # imm = 0x28F5C29
	setae	%sil
	movl	%eax, %edi
	callq	and
	imull	$-1030792151, 4(%rsp), %ecx     # imm = 0xC28F5C29
	addl	$85899344, %ecx                 # imm = 0x51EB850
	rorl	$4, %ecx
	xorl	%esi, %esi
	cmpl	$10737419, %ecx                 # imm = 0xA3D70B
	setb	%sil
	movzbl	%al, %edi
	callq	or
	testb	$1, %al
	je	.LBB0_2
# %bb.1:                                # %if.then0
	movb	$1, 3(%rsp)
	jmp	.LBB0_3
.LBB0_2:                                # %if.else0
	movb	$0, 3(%rsp)
.LBB0_3:                                # %if.end0
	movb	3(%rsp), %al
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	isLeapYear, .Lfunc_end0-isLeapYear
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
	movl	$2023, 12(%rsp)                 # imm = 0x7E7
	movl	$2023, %edi                     # imm = 0x7E7
	callq	isLeapYear
	andb	$1, %al
	movb	%al, 11(%rsp)
	je	.LBB1_2
# %bb.1:                                # %if.then1
	movl	$.L.str.0, %edi
	jmp	.LBB1_3
.LBB1_2:                                # %if.else1
	movl	$.L.str.1, %edi
.LBB1_3:                                # %if.end1
	callq	print
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	.L.str.0,@object                # @.str.0
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str.0:
	.asciz	"Leap year"
	.size	.L.str.0, 10

	.type	.L.str.1,@object                # @.str.1
.L.str.1:
	.asciz	"Not a leap year"
	.size	.L.str.1, 16

	.section	".note.GNU-stack","",@progbits
