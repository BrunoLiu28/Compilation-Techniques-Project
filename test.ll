@actual_max = dso_local global i32 20
declare dso_local void @print_int(i32 noundef) 
declare dso_local void @print_float(float noundef)
declare dso_local void @print_bool(i1 noundef) 
declare dso_local void @print_char(i8 noundef) 
declare dso_local void @print(i8* noundef)
declare dso_local i32 @pow_int(i32, i32)
declare dso_local float @pow_float(float, float)
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%z = alloca i32
%x = alloca i32
%y = alloca i32
%0 = load i32, i32* @actual_max
%biop0 = icmp sgt i32 %0, 5
br i1 %%biop0, label %if.then0, label %if.end0
if.then0:
store i32 2, i32* %z
br label %while.cond0
while.cond0:
%1 = load i32, i32* @actual_max
%biop1 = icmp sgt i32 %1, 5
br i1 %biop1, label %while.body0, label %while.end0
while.body0:
store i32 2, i32* %x
store i32 2, i32* %y
%2 = load i32, i32* @actual_max
%biop2 = sub nsw i32 %2, 2
store i32 %biop2, i32* @actual_max
br label %while.cond0
while.end0:
br label %if.end0
if.end0:
ret void
}