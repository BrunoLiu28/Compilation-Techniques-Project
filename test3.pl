function isLeapYear(val year:int) : bool {
    if (year % 4 = 0 && year % 100 != 0) || (year % 400 = 0) {
        isLeapYear := true;
    } else {
        isLeapYear := false;
    }
}