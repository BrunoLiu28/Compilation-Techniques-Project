@.str.0 = private unnamed_addr constant [10 x i8] c"Leap year\00"
@.str.1 = private unnamed_addr constant [16 x i8] c"Not a leap year\00"
declare dso_local void @print_int(i32) 
declare dso_local void @print_float(float)
declare dso_local void @print_bool(i1)
declare dso_local void @print_char(i8)
declare dso_local void @print(i8*)
declare dso_local i32 @pow_int(i32, i32)
declare dso_local float @pow_float(float, i32)
declare dso_local i1 @and(i1, i1)
declare dso_local i1 @or(i1, i1)
define dso_local i1 @isLeapYear(i32 noundef %year){
entry:
%year.addr = alloca i32
store i32 %year, i32* %year.addr
%isLeapYear = alloca i1
store i1 0, i1* %isLeapYear
%0 = load i32, i32* %year.addr
%biop0 = srem i32 %0, 4
%biop1 = icmp eq i32 %biop0, 0
%1 = load i32, i32* %year.addr
%biop2 = srem i32 %1, 100
%biop3 = icmp ne i32 %biop2, 0
%biop4 = call i1 @and(i1 %biop1, i1 %biop3)
%2 = load i32, i32* %year.addr
%biop5 = srem i32 %2, 400
%biop6 = icmp eq i32 %biop5, 0
%biop7 = call i1 @or(i1 %biop4, i1 %biop6)
br i1 %biop7, label %if.then0, label %if.else0
if.then0:
store i1 1, i1* %isLeapYear
br label %if.end0
if.else0:
store i1 0, i1* %isLeapYear
br label %if.end0
if.end0:
%3 = load i1, i1* %isLeapYear
ret i1 %3
}
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%year = alloca i32
%leap = alloca i1
store i32 2023, i32* %year
%0 = load i32, i32* %year
%call0 = call i1 @isLeapYear(i32 noundef %0)
store i1 %call0, i1* %leap
%1 = load i1, i1* %leap
br i1 %1, label %if.then1, label %if.else1
if.then1:
call void @print(i8* noundef getelementptr inbounds ([10 x i8], [10 x i8]* @.str.0, i64 0, i64 0))
br label %if.end1
if.else1:
call void @print(i8* noundef getelementptr inbounds ([16 x i8], [16 x i8]* @.str.1, i64 0, i64 0))
br label %if.end1
if.end1:
ret void
}