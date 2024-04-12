val unsorted : [float] := [5.5, 3.3, 8.8, 2.2, 1.1, 9.9];

function double_array_length(val arr : [float]) : int;

function bubble_sort(val arr : [float]) : [float] {
    var sorted : [float] := arr; 
    var n : int := float_array_length(sorted);

    bubble_sort := sorted;
}