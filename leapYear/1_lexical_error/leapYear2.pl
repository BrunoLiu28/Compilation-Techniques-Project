function isLeapYear(val year:int) : bool {
    if (year % 4 = 0 && year % 100 != 0) || (year % 400 = 0) { 
        isLeapYear := true;
    } else {
        isLeapYear := false;
    }
}

function main(val args:[string]) {
    var year : int := 2023; 
    var leap : bool := isLeapYear(year);
    if leap @ {     # Error: '@' is not a valid operator
        print("Leap year");
    } else {
        print("Not a leap year");
    }
}
