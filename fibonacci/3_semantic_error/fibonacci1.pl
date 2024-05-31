val num : int := 15.3; # Semantic error: expected type int, got float

function fibonacci(val n : int) : int {
    if n <= 1 {
        fibonacci := n;
    } else {
        fibonacci := fibonacci(n - 1) + fibonacci(n - 2);
    }
    fibonacci := fibonacci;
}

function main(val args:[string]) {
	val result : int := fibonacci(num);
    print("The fibonacci of the number you entered is:");
	print_int(result);
}