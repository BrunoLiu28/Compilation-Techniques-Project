function getArrayRandomFloatsSize5() : [float];

functio main(val args:[string]) { # Syntactic error: 'functio' should be 'function'
    var n : int := 5; 
    var sorted : [float] := getArrayRandomFloatsSize5(); 

    var i : int := 0;
    print("Unsorted array:");
    while i < n  {
        print_float(sorted[i]);
        i := i + 1;
    }

    i := 0;
    while i < n - 1 {
        if sorted[i] > sorted[i + 1] {
            var temp : float := sorted[i];
            sorted[i] := sorted[i + 1];
            sorted[i + 1] := temp;
        }
        i := i + 1;
    }

    i := 0;
    print("Sorted array:");
    while i < n  {
        print_float(sorted[i]);
        i := i + 1;
    }
}