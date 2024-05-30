from "second.pl" import *;

val num : int := 1_5;
function main(val args:[string]) {
	val result : int := fibonacci(num);
    print("The fibonacci of the number you entered is:");
	print_int(result);
}