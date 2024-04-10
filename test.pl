function maxRangeSquared(var mi:int, val ma:int) : int {
	var current_max : int := mi ^ 2;
	while mi <= ma {
		int current_candidate : int := mi ^ 2;
		if current_candidate > current_max {
			current_max := current_candidate;
		}
	} 
	maxRangeSquared := current_max; # This line returns the current max!
}
