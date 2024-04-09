val num : int := 1_0;

function fibonacci(val n : inti) : int {             #lexical error, type named inti instead of int
    if n <= 1 {
        fibonacci := n;
    } else {
        fibonacci := fibonacci(n - 1) + fibonacci(n - 2);
    }
    fibonacci := fibonacci;
}


function main(val args:[string]) {
	val result : int := fibonacci(num);
	print_int(result);
}



