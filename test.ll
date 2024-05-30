declare dso_local void @print_int(i32 noundef) 
declare dso_local void @print_float(float noundef)
declare dso_local void @print_bool(i1 noundef) 
declare dso_local void @print_char(i8 noundef) 
declare dso_local void @print(i8* noundef)
declare dso_local i32 @pow_int(i32, i32)
declare dso_local float @pow_float(float, i32)
declare dso_local i1 @and(i1, i1)
declare dso_local i1 @or(i1, i1)
declare dso_local float* @teste()
declare dso_local float** @createMatrix()
declare dso_local i32** @createMatrix2()
define dso_local i1 @isPrime(i32 noundef %num){
entry:
%num.addr = alloca i32
store i32 %num, i32* %num.addr
%isPrime = alloca i1
store i1 0, i1* %isPrime
%i = alloca i32
%f = alloca i32
store i1 1, i1* %isPrime
%0 = load i32, i32* %num.addr
%biop0 = icmp sle i32 %0, 1
br i1 %biop0, label %if.then0, label %if.end0
if.then0:
store i1 0, i1* %isPrime
br label %if.end0
if.end0:
store i32 2, i32* %i
br label %while.cond0
while.cond0:
%1 = load i32, i32* %i
%2 = load i32, i32* %i
%biop1 = mul nsw i32 %1, %2
%3 = load i32, i32* %num.addr
%biop2 = icmp sle i32 %biop1, %3
br i1 %biop2, label %while.body0, label %while.end0
while.body0:
store i32 2, i32* %f
%4 = load i32, i32* %num.addr
%5 = load i32, i32* %i
%biop3 = srem i32 %4, %5
%biop4 = icmp eq i32 %biop3, 0
br i1 %biop4, label %if.then1, label %if.end1
if.then1:
store i1 0, i1* %isPrime
br label %if.end1
if.end1:
%6 = load i32, i32* %i
%biop5 = add nsw i32 %6, 1
store i32 %biop5, i32* %i
br label %while.cond0
while.end0:
%7 = load i1, i1* %isPrime
ret i1 %7
}
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%_ult = alloca i1
%call0 = call i1 @isPrime(i32 noundef 18)
store i1 %call0, i1* %_ult
%0 = load i1, i1* %_ult
call void @print_bool(i1 noundef %0)
ret void
}