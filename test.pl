# val actual_min : int := -10;
# val actual_max : int := 20;

# function maxRangeSquared(var mi:int, val ma:int) : int {
# 	var current_max : int := mi * mi;
# 	while mi <= ma {
# 		var current_candidate : int := mi * mi;
# 		if current_candidate > current_max {
# 			current_max := current_candidate;
# 		}
#         mi := mi + 1;
# 	} 
# 	maxRangeSquared := current_max; # This line returns the current max!
# 	maxRangeSquared := 0;
# }

# # function getArrayRandomFloats(val m:[float]) : void;
# function teste() : [float];
# function createMatrix() : [[float]];
# function createMatrix2() : [[int]];
# function ola(): int {
#     ola := 2*9;
# }

# function main(val args: [string]) {
# 	var a : int := ola();
#     print_int(a);

#     while x < 10 {
#         var a : int := 2;
#     }
# }
# var actual_max : int := 20;


# function ola(): float {
#     ola := 2.11;
# }

# function main(val args:[string]) {
# 	# print_int(getArrayRandomFloats());
# 	# var s : string := "ola";
# 	# print(s);
# 	# val a : int := 1;
    # var numbers : [[int]] := createMatrix2();
    # var numbers2 : int := numbers[2][3];
    # print_int(numbers2);

    # val i : float := 3.4;
    # val i2 : float := 2.7;
    # val i3 : float := i / i2;
    # print_float(i3);
    # # val i4 : bool := i <= i2;
    # # print_bool(i4);

    # val f : int := 3;
    # val f2 : int := 2;
    # val f3 : int := f * f2;
    # print_int(f3);
    # val f4 : bool := f >= f2;
    # if i4 && f4 {
    #     print_int(100000);
    # } else {
    #     print_int(999999);
    # }
    # print_float(numbers[2]);
# 	# getArrayRandomFloats(numbers);
# 	# # val i : float := 1.0;
# 	# # print_float(i);
# 	# numbers[a] := 8.2;
# 	# # getArrayRandomFloats(numbers);
# 	# val b : float := numbers[a];
# 	# print_float(b);
# 	# getArrayRandomFloats(numbers);
	# val teste : float := 2.2;
# 	val result2 : int := maxRangeSquared(2, actual_max);
# 	print_int(result2);
# 	# print_float(teste);
    # if actual_max > 5 {
        # var z : float := 2.11^10;
        # while actual_max > 5 {
        # var z : bool := teste+1.2 > teste;
        # print_bool(z);
        # }
    # }
    
    # print_float(z);
# }

# # var global : int := 1;
# # function ola() : int {
# #     ola := 1;
# #     while -5 > ola {
# #         ola := ola - 1;
# #     }
# # }


# val actual_min : int := -9;
# val actual_max : int := 9;

# function maxRangeSquared(var mi:int, val ma:int) : int {
# 	var current_max : int := mi + 2;
# 	while mi <= ma {
# 		var current_candidate : int := mi + 2;
# 		if current_candidate > current_max {
# 			current_max := current_candidate;
# 		}
# 	} 
# 	maxRangeSquared := current_max; # This line returns the current max!
# }


# function main(val args:[string]) {
# 	val result : int := maxRangeSquared(actual_min, actual_max);
# 	print_int(result);
# }

# function isPrime(val num:int) : bool {
#     isPrime := true;
#     if num <= 1 {
#         isPrime := false;
#     }
#     var i : int := 2;
#     while i * i <= num {
#         var f : int := 2;
#         if num % i = 0 {
#             isPrime := false; 
#         }
#         i := i + 1;
#     }

# }
# function main(val args:[string]) {
#     val _ult : bool := isPrime(10+7);
#     print_bool(_ult);
# }

# function float_array_length(val arr : [float]) : int;

# function bubble_sort(val arr : [float]) : [float] {
#     var sorted : [float] := arr; 
#     var n : int := float_array_length(sorted);
#     var swapped : bool := true;

#     while swapped {
#         swapped := false;
#         # var i : int := 0;
#         # while i < n - 1 {
#         #     if sorted[i] > sorted[i + 1] {
#         #         var temp : float := sorted[i];
#         #         sorted[i] := sorted[i + 1];
#         #         sorted[i + 1] := temp;
#         #         swapped := true;
#         #     }
#         #     i := i + 1;
#         # }
#         n := n - 1;
#     }

#     bubble_sort := sorted;
# }

# var mmm : string := "teste";
# var teste : string := "testdsadasdse";

# function main(val args:[string]) {
    # val unsorted : [float] := getArrayRandomFloats();
	# val sorted : [float] := bubble_sort(unsorted);

    # var sorted : [float] := teste();
    # var n : int := 5;
    # print_int(n);
    # var swapped : bool := true;
    # var temp : float := sorted[0];
    # while swapped {
    #     swapped := false;
        # var i : int := 0;
        # while i < n - 1 {
        #     if sorted[i+1] > sorted[i] {
        #         temp := sorted[i+1];
        #         # sorted[i] := sorted[i + 1];
        #         # sorted[i + 1] := temp;
        #         # swapped := true;
        #     }
        #     print_float(temp);
        #     i := i + 1;
        # }
        
        # teste := "teste";
        # print(teste);
        # # print(swapped);
        # print_float(temp);
    #     n := n - 1;
    # }

    # var final : [float] := sorted;
    # var f : int := float_array_length(final) - 1;
    # while i >= 0 {
    #     print_float(sorted[i]);
    #     i := i - 1;
    # }
# }
#####################################################################################################################
#EXEMPLO DO BUBBLE SORT

# function getArrayRandomFloatsSize5() : [float];

# function main(val args:[string]) {
#     var n : int := 5; 
#     var sorted : [float] := getArrayRandomFloatsSize5(); 

#     var i : int := 0;
#     while i < n - 1 {
#         if sorted[i] > sorted[i + 1] {
#             var temp : float := sorted[i];
#             sorted[i] := sorted[i + 1];
#             sorted[i + 1] := temp;
#         }
#         i := i + 1;
#     }

#     i := 0;
#     while i < n  {
#         print_float(sorted[i]);
#         i := i + 1;
#     }
# }

#EXEMPLO DO PROFESSOR

# val actual_min : int := -9;
# val actual_max : int := 9;

# function maxRangeSquared(var mi:int, val ma:int) : int {
# 	var current_max : int := mi ^ 2;
# 	while mi <= ma {
# 		var current_candidate : int := mi ^ 2;
# 		if current_candidate > current_max {
# 			current_max := current_candidate;
# 		}
#         mi := mi + 1;
# 	} 
# 	maxRangeSquared := current_max; 
# }


# function main(val args:[string]) {
# 	val result : int := maxRangeSquared(actual_min, actual_max);
# 	print_int(result);
# }


#EXEMPLO IS LEAP YEAR
# function isLeapYear(val year:int) : bool {
#     if (year % 4 = 0 && year % 100 != 0) || (year % 400 = 0) {
#         isLeapYear := true;
#     } else {
#         isLeapYear := false;
#     }
# }

from "test2.pl" import *;

function main(val args:[string]) {
    var year : int := 2023; 
    var leap : bool := isLeapYear(year);
    if leap {
        print("Leap year");
    } else {
        print("Not a leap year");
    }
}

