val unsorted : [double] := [5.5, 3.3, 8.8, 2.2, 1.1, 9.9];

function double_array_length(val arr : [double]) : int;

function bubble_sort(val arr : [double]) : [double] {
    var sorted : [double] := arr; 
    var n : int := double_array_length(sorted);
    var swapped : bool := true;

    while swapped {
        swapped := false;
        var i : int := 0;
        while i < n - 1 {{                          #Syntactic error, an extra {
            if sorted[i] > sorted[i + 1] {
                var temp : double := sorted[i];
                sorted[i] := sorted[i + 1];
                sorted[i + 1] := temp;
                swapped := true;
            }
            i := i + 1;
        }
        n := n - 1;
    }

    bubble_sort = sorted;
}

function main(val args:[string]) {
	val sorted : [double] := bubble_sort(unsorted);
    var i : int := double_array_length(sorted) - 1;
    while i >= 0 {
        print_double(sorted[i]);
        i := i - 1;
    }
}

# c implementation to get the size of the array
int double_array_length(double arr[]) {
    int length = 0;
    while (!isnan(arr[length])) {
        length++;
    }
    return length;
}

