declare dso_local void @print_int(i32) 
declare dso_local void @print_float(float)
declare dso_local void @print_bool(i1)
declare dso_local void @print_char(i8)
declare dso_local void @print(i8*)
declare dso_local i32 @pow_int(i32, i32)
declare dso_local float @pow_float(float, i32)
declare dso_local i1 @and(i1, i1)
declare dso_local i1 @or(i1, i1)
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%biop0 = add nsw i32 -1, 1
call void @print_int(i32 noundef %biop0)
ret void
}