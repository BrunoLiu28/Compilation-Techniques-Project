@.str.0 = private unnamed_addr constant [4 x i8] c"ola\00"
declare dso_local void @print_int(i32 noundef) 
declare dso_local void @print_float(float noundef)
declare dso_local void @print_bool(i1 noundef) 
declare dso_local void @print_char(i8 noundef) 
declare dso_local void @print(i8* noundef) #0
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%s = alloca i8*
store i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.0, i64 0, i64 0), i8** %s
%0 = load i8*, i8** %s
call void @print(i8* noundef %0)
ret void
}