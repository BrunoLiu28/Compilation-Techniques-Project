@num = dso_local global i32 15
@.str.0 = private unnamed_addr constant [44 x i8] c"The fibonacci of the number you entered is:\00"
declare dso_local void @print_int(i32) 
declare dso_local void @print_float(float)
declare dso_local void @print_bool(i1)
declare dso_local void @print_char(i8)
declare dso_local void @print(i8*)
declare dso_local i32 @pow_int(i32, i32)
declare dso_local float @pow_float(float, i32)
declare dso_local i1 @and(i1, i1)
declare dso_local i1 @or(i1, i1)
define dso_local i32 @fibonacci(i32 noundef %n){
entry:
%n.addr = alloca i32
store i32 %n, i32* %n.addr
%fibonacci = alloca i32
store i32 -1, i32* %fibonacci
%0 = load i32, i32* %n.addr
%biop0 = icmp sle i32 %0, 1
br i1 %biop0, label %if.then0, label %if.else0
if.then0:
%1 = load i32, i32* %n.addr
store i32 %1, i32* %fibonacci
br label %if.end0
if.else0:
%2 = load i32, i32* %n.addr
%biop1 = sub nsw i32 %2, 1
%call0 = call i32 @fibonacci(i32 noundef %biop1)
%3 = load i32, i32* %n.addr
%biop2 = sub nsw i32 %3, 2
%call1 = call i32 @fibonacci(i32 noundef %biop2)
%biop3 = add nsw i32 %call0, %call1
store i32 %biop3, i32* %fibonacci
br label %if.end0
if.end0:
%4 = load i32, i32* %fibonacci
store i32 %4, i32* %fibonacci
%5 = load i32, i32* %fibonacci
ret i32 %5
}
declare dso_local float* @getArrayRandomFloatsSize5()
define dso_local i1 @isLeapYear(i32 noundef %year){
entry:
%year.addr = alloca i32
store i32 %year, i32* %year.addr
%isLeapYear = alloca i1
store i1 0, i1* %isLeapYear
%0 = load i32, i32* %year.addr
%biop4 = srem i32 %0, 4
%biop5 = icmp eq i32 %biop4, 0
%1 = load i32, i32* %year.addr
%biop6 = srem i32 %1, 100
%biop7 = icmp ne i32 %biop6, 0
%biop8 = call i1 @and(i1 %biop5, i1 %biop7)
%2 = load i32, i32* %year.addr
%biop9 = srem i32 %2, 400
%biop10 = icmp eq i32 %biop9, 0
%biop11 = call i1 @or(i1 %biop8, i1 %biop10)
br i1 %biop11, label %if.then1, label %if.else1
if.then1:
store i1 1, i1* %isLeapYear
br label %if.end1
if.else1:
store i1 0, i1* %isLeapYear
br label %if.end1
if.end1:
%3 = load i1, i1* %isLeapYear
ret i1 %3
}
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%result = alloca i32
%0 = load i32, i32* @num
%call2 = call i32 @fibonacci(i32 noundef %0)
store i32 %call2, i32* %result
call void @print(i8* noundef getelementptr inbounds ([44 x i8], [44 x i8]* @.str.0, i64 0, i64 0))
%1 = load i32, i32* %result
call void @print_int(i32 noundef %1)
ret void
}