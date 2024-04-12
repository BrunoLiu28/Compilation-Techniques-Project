val num : int := 1_0;

function fibonacci(val n : int) : int {
    if n <= 1 {
        fibonacci := n;
    } else {
        fibonacci := fibonacci(n - 1);
    }
    fibonacci := fibonacci;
}
