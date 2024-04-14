function main(val args:[string]) {
	val sorted : [float] := bubble_sort(unsorted);
    var i : int := float_array_length(sorted) - 1;
    while i >= 0 {
        print_float(sorted[i]);
        i := i - 1;
    }
}