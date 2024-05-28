declare dso_local void @print_int(i32 noundef) #0
declare dso_local void @getArrayRandomFloats(i32*)#0
declare dso_local i32* @teste() #0
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%numbers = alloca i32*
%call0 = call i32* @teste()
store i32* %call0, i32** %numbers
%0 = load i32*, i32** %numbers
call void @getArrayRandomFloats(i32* noundef %0)
ret void
}