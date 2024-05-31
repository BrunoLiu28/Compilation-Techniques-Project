declare dso_local void @print_int(i32) 
declare dso_local void @print_float(float)
declare dso_local void @print_bool(i1)
declare dso_local void @print_char(i8)
declare dso_local void @print(i8*)
declare dso_local i32 @pow_int(i32, i32)
declare dso_local float @pow_float(float, i32)
declare dso_local i1 @and(i1, i1)
declare dso_local i1 @or(i1, i1)
define dso_local i32 @sumMatrix(i32 noundef %f,i32 noundef %i){
entry:
%f.addr = alloca i32
store i32 %f, i32* %f.addr
%i.addr = alloca i32
store i32 %i, i32* %i.addr
%sumMatrix = alloca i32
store i32 -1, i32* %sumMatrix
%i1 = alloca i32
%f1 = alloca i32
%a = alloca i32
store i32 0, i32* %sumMatrix
store i32 0, i32* %i1
store i32 0, i32* %f1
store i32 1, i32* %a
br label %while.cond0
while.cond0:
%0 = load i32, i32* %i1
%1 = load i32, i32* %i.addr
%biop0 = icmp slt i32 %0, %1
br i1 %biop0, label %while.body0, label %while.end0
while.body0:
store i32 0, i32* %f1
br label %while.cond1
while.cond1:
%2 = load i32, i32* %f1
%3 = load i32, i32* %f.addr
%biop1 = icmp slt i32 %2, %3
br i1 %biop1, label %while.body1, label %while.end1
while.body1:
%4 = load i32, i32* %sumMatrix
%5 = load i32, i32* %a
%biop2 = add nsw i32 %4, %5
store i32 %biop2, i32* %sumMatrix
%6 = load i32, i32* %f1
%biop3 = add nsw i32 %6, 1
store i32 %biop3, i32* %f1
br label %while.cond1
while.end1:
%7 = load i32, i32* %i1
%biop4 = add nsw i32 %7, 1
store i32 %biop4, i32* %i1
br label %while.cond0
while.end0:
%8 = load i32, i32* %sumMatrix
ret i32 %8
}
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%result = alloca i32
%call0 = call i32 @sumMatrix(i32 noundef 3,i32 noundef 3)
store i32 %call0, i32* %result
%0 = load i32, i32* %result
call void @print_int(i32 noundef %0)
ret void
}