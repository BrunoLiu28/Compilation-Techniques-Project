function getArrayRandomFloatsSize5() : [float];

function $ (val args:[string]) { # Lexical error: '$' is not a valid token
    var n : int := 5; 
    var sorted : [float] := getArrayRandomFloatsSize5(); 

    var i : int := 0;
    while i < n - 1 {
        if sorted[i] > sorted[i + 1] {
            var temp : float := sorted[i];
            sorted[i] := sorted[i + 1];
            sorted[i + 1] := temp;
        }
        i := i + 1;
    }

    i := 0;
    while i < n  {
        print_float(sorted[i]);
        i := i + 1;
    }
}