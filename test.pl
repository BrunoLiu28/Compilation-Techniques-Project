val unsorted : [float] := getArrayRandomFloats();

function float_array_length(val arr : [float]) : int;

function bubble_sort(val arr : [float]) : [float] {
    var sorted : [float] := arr; 
    var n : int := float_array_length(sorted);
    var swapped : bool := true;

    while swapped {
        swapped := false;
        var i : int := 0;
        while i < n - 1 {
            if sorted[i] > sorted[i + 1] {
                var temp : float := sorted[i];
                sorted[i] := sorted[i + 1];
                sorted[i + 1] := temp;
                swapped := true;
            }
            i := i + 1;
        }
        n := n - 1;
    }

    bubble_sort := sorted;
}

function main(val args:[string]) {
	val sorted : [float] := bubble_sort(unsorted);
    var i : int := float_array_length(sorted) - 1;
    while i >= 0 {
        print_float(sorted[i]);
        i := i - 1;
    }
}