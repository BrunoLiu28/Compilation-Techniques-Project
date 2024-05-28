declare dso_local void @print_int(i32 noundef) #0
declare dso_local i32 @getArrayRandomFloats() #0
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%call0 = call i32 @getArrayRandomFloats()
call void @print_int(i32 noundef %call0)
ret void
}