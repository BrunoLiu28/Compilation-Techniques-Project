from "test3.pl" import ola; 

function getArrayRandomFloatsSize5() : [float];

function maxRangeSquared(var mi:int, val ma:int) : int {
	var current_max : int := mi ^ 2;
	while mi <= ma {
		var current_candidate : int := mi ^ 2;
		if current_candidate > current_max {
			current_max := current_candidate;
		}
        mi := mi + 1;
	} 
	maxRangeSquared := current_max; 
}

function ola() : int {
    ola := 10;
}

val actual_min : int := -9;
val actual_max : int := 9;

function main(val args: [string]) {
	var a : int := ola();
    print_int(a);

    while x < 10 {
        var a : int := 2;
    }
}