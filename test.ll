@actual_min = dso_local global i32 -10
@actual_max = dso_local global i32 20
declare dso_local void @print_int(i32 noundef) 
declare dso_local void @print_float(float noundef)
declare dso_local void @print_bool(i1 noundef) 
declare dso_local void @print_char(i8 noundef) 
declare dso_local void @print(i8* noundef) #0
define dso_local i32 @maxRangeSquared(i32 noundef %mi,i32 noundef %ma){
entry:
%mi.addr = alloca i32
store i32 %mi, i32* %mi.addr
%ma.addr = alloca i32
store i32 %ma, i32* %ma.addr
%maxRangeSquared = alloca i32
store i32 -1, i32* %maxRangeSquared
%current_max = alloca i32
%0 = load i32, i32* %mi
%1 = load i32, i32* %mi
%biop0 = mul nsw i32 %%0, %1
store i32 biop0, i32* %current_max
br label %while.cond0
while.cond0:
%2 = load i32, i32* %mi
%3 = load i32, i32* %ma
%biop1 = icmp sle i32 %%2, %3
br i1 %biop1, label %while.body0, label %while.end0
while.body0:
%current_candidate = alloca i32
%4 = load i32, i32* %mi
%5 = load i32, i32* %mi
%biop2 = mul nsw i32 %%4, %5
store i32 biop2, i32* %current_candidate
%6 = load i32, i32* %current_candidate
%7 = load i32, i32* %current_max
%biop3 = icmp sgt i32 %%6, %7
br i1 %biop3, label %if.then0, label %if.end0
if.then0:
%8 = load i32, i32* %current_candidate
store i32 %8, i32* %current_max
br label %if.end0
if.end0:
%9 = load i32, i32* %mi
%biop4 = add nsw i32 %%9, 1
store i32 biop4, i32* %mi
br label %while.cond0
while.end0:
%10 = load i32, i32* %current_max
store i32 %10, i32* %maxRangeSquared
store i32 0, i32* %maxRangeSquared
%11 = load i32, i32* %maxRangeSquared
ret i32 %11
}
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%result2 = alloca i32
%0 = load i32, i32* @actual_max
%call0 = call i32 @maxRangeSquared(i32 noundef 2,i32 noundef %0)
store i32 %call0, i32* %result2
%1 = load i32, i32* %result2
call void @print_int(i32 noundef %1)
ret void
}