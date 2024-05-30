declare dso_local void @print_int(i32) 
declare dso_local void @print_float(float)
declare dso_local void @print_bool(i1)
declare dso_local void @print_char(i8)
declare dso_local void @print(i8*)
declare dso_local i32 @pow_int(i32, i32)
declare dso_local float @pow_float(float, i32)
declare dso_local i1 @and(i1, i1)
declare dso_local i1 @or(i1, i1)
declare dso_local float* @getArrayRandomFloatsSize5()
define dso_local void @main(i8** noundef %argv) {
entry:
%argv.addr = alloca i8**
store i8** %argv, i8*** %argv.addr
%n = alloca i32
%sorted = alloca float*
%i = alloca i32
%temp = alloca float
store i32 5, i32* %n
%call0 = call float* @getArrayRandomFloatsSize5()
store float* %call0, float** %sorted
store i32 0, i32* %i
br label %while.cond0
while.cond0:
%0 = load i32, i32* %i
%1 = load i32, i32* %n
%biop0 = sub nsw i32 %1, 1
%biop1 = icmp slt i32 %0, %biop0
br i1 %biop1, label %while.body0, label %while.end0
while.body0:
%2 = load i32, i32* %i
%idxprom0 = sext i32 %2 to i64
%3 = load float*, float** %sorted
%arrayidx0 = getelementptr inbounds float, float* %3, i64 %idxprom0
%4 = load i32, i32* %i
%biop2 = add nsw i32 %4, 1
%idxprom1 = sext i32 %biop2 to i64
%5 = load float*, float** %sorted
%arrayidx1 = getelementptr inbounds float, float* %5, i64 %idxprom1
%6 = load float, float* %arrayidx0
%7 = load float, float* %arrayidx1
%biop3 = fcmp ogt float %6, %7
br i1 %biop3, label %if.then0, label %if.end0
if.then0:
%8 = load i32, i32* %i
%idxprom2 = sext i32 %8 to i64
%9 = load float*, float** %sorted
%arrayidx2 = getelementptr inbounds float, float* %9, i64 %idxprom2
%10 = load float, float* %arrayidx2
store float %10, float* %temp
%11 = load i32, i32* %i
%biop4 = add nsw i32 %11, 1
%idxprom3 = sext i32 %biop4 to i64
%12 = load float*, float** %sorted
%arrayidx3 = getelementptr inbounds float, float* %12, i64 %idxprom3
%13 = load float, float* %arrayidx3
%14 = load i32, i32* %i
%idxprom4 = sext i32 %14 to i64
%15 = load float*, float** %sorted
%arrayidx4 = getelementptr inbounds float, float* %15, i64 %idxprom4
store float %13, float* %arrayidx4
%16 = load float, float* %temp
%17 = load i32, i32* %i
%biop5 = add nsw i32 %17, 1
%idxprom5 = sext i32 %biop5 to i64
%18 = load float*, float** %sorted
%arrayidx5 = getelementptr inbounds float, float* %18, i64 %idxprom5
store float %16, float* %arrayidx5
br label %if.end0
if.end0:
%19 = load i32, i32* %i
%biop6 = add nsw i32 %19, 1
store i32 %biop6, i32* %i
br label %while.cond0
while.end0:
store i32 0, i32* %i
br label %while.cond1
while.cond1:
%20 = load i32, i32* %i
%21 = load i32, i32* %n
%biop7 = icmp slt i32 %20, %21
br i1 %biop7, label %while.body1, label %while.end1
while.body1:
%22 = load i32, i32* %i
%idxprom6 = sext i32 %22 to i64
%23 = load float*, float** %sorted
%arrayidx6 = getelementptr inbounds float, float* %23, i64 %idxprom6
%24 = load float, float* %arrayidx6
call void @print_float(float noundef %24)
%25 = load i32, i32* %i
%biop8 = add nsw i32 %25, 1
store i32 %biop8, i32* %i
br label %while.cond1
while.end1:
ret void
}