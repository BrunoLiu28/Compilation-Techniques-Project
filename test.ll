@actual_min = dso_local global i32 -9
@actual_max = dso_local global i32 9
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
%biop0 = add nsw i32 %0, 2
store i32 %biop0, i32* %current_max
br label %while.cond0
while.cond0:
%1 = load i32, i32* %mi
%2 = load i32, i32* %ma
%biop1 = icmp sle i32 %1, %2
br i1 %%biop1, label %while.body0, label %while.end0
while.body0:
%current_candidate = alloca i32
%3 = load i32, i32* %mi
%biop2 = add nsw i32 %3, 2
store i32 %biop2, i32* %current_candidate
%4 = load i32, i32* %current_candidate
%5 = load i32, i32* %current_max
%biop3 = icmp sgt i32 %4, %5
br i1 %%biop3, label %if.then0, label %if.end0
if.then0:
%6 = load i32, i32* %current_candidate
store i32 %6, i32* %current_max
br label %if.end0
if.end0:
br label %while.cond0
while.end0:
%7 = load i32, i32* %current_max
store i32 %7, i32* %maxRangeSquared
%8 = load i32, i32* %maxRangeSquared
ret i32 %8
}
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%result = alloca i32
%0 = load i32, i32* @actual_min
%1 = load i32, i32* @actual_max
%call0 = call i32 @maxRangeSquared(i32 noundef %0,i32 noundef %1)
store i32 %call0, i32* %result
%2 = load i32, i32* %result
call void @print_int(i32 noundef %2)
ret void
}