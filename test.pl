# val actual_min : int := -10;
# val actual_max : int := 20;

# function maxRangeSquared(var mi:int, val ma:int) : int {
	# var current_max : int := mi ^ 2;
	# while mi <= ma {
	# 	var current_candidate : int := mi ^ 2;
	# 	if current_candidate > current_max {
	# 		current_max := current_candidate;
	# 	}
    #     mi := mi + 1;
	# } 
	# maxRangeSquared := current_max; # This line returns the current max!
# 	maxRangeSquared := 0;
# }

# function getArrayRandomFloats(val m:[float]) : void;
# function teste() : [float];


function main(val args:[string]) {
	# print_int(getArrayRandomFloats());

	var s : string := "ola";
	print(s);
	# val a : int := 1;
    # var numbers : [float] := teste();
	# getArrayRandomFloats(numbers);
	# # val i : float := 1.0;
	# # print_float(i);
	# numbers[a] := 8.2;
	# # getArrayRandomFloats(numbers);
	# val b : float := numbers[a];
	# print_float(b);
	# getArrayRandomFloats(numbers);
	# val teste : float := 1232.74234;
	# val result2 : int := maxRangeSquared(2, actual_max);
	# print_int(result);
	# print_float(teste);
}

# var global : int := 1;
# function ola() : int {
#     ola := 1;
#     while -5 > ola {
#         ola := ola - 1;
#     }
# }