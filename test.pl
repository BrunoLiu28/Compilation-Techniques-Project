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

#FIBONACCI
# val num : int := 1_5;

# function fibonacci(val n : int) : int {
#     if n <= 1 {
#         fibonacci := n;
#     } else {
#         fibonacci := fibonacci(n - 1) + fibonacci(n - 2);
#     }
#     fibonacci := fibonacci;
# }

# function main(val args:[string]) {
# 	val result : int := fibonacci(num);
#     print("The fibonacci of the number you entered is:");
# 	print_int(result);
# }

#EXEMPLO IS LEAP YEAR
# from "test2.pl" import *;

# function main(val args:[string]) {
#     var year : int := 2020; 
#     var leap : bool := isLeapYear(year);
#     if leap {
#         print("Leap year");
#     } else {
#         print("Not a leap year");
#     }
# }

# from "test2.pl" import *;

# function isLeapYear(val year:int) : bool {
#     if (year % 4 = 0 && year % 100 != 0) || (year % 400 = 0) {
#         isLeapYear := true;
#     } else {
#         isLeapYear := false;
#     }
# }


val num : int := 1_5;

function fibonacci(val n : int) : int {
    if n <= 1 {
        fibonacci := n;
    } else {
        fibonacci := fibonacci(n - 1) + fibonacci(n - 2);
    }
    fibonacci := fibonacci;
}

function main(val args:[string]) {
	val result : int := fibonacci(num);
    print("The fibonacci of the number you entered is:");
	print_int(result);
}