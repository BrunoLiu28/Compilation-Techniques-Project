val num : int := 1_0;

function fibonacci(val n : int) : int {
    if n <= 1 {
        fibonacci := n;
    } else {
        fibonacci := fibonacci(n - 1) + fibonacci(n - 2);
    }
    fibonacci := fibonacci;
}


function main(val args:[string]) {
	val result :: int := fibonacci(num);    #Syntactic error, an extra :
	print_int(result);
}



