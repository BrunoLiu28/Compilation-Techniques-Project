val palindrome : string := "radar";

function string_length(val str : string) : int;

function palindromeString(val str : string) : int {
	var result : int := 1;
	var i : int := 0;
    var j : int := string_length(str);
    while (i < j) && (result = 1){
        if str.get_array()[i] != str.get_array()[j] {
            result := -1;
        }
        i = i + 1;                              #the assigment sign is := and not =
        j := j - 1;
    }
    palindromeString := result;
}


function main(val args:[string]) {
	val result : int := is_palindrome(palindrome);
    if result = -1 {
        print_string("String is not palindrome");
    } else {
        print_string("String is palindrome");
    }
	print_int(result);
}

# c implementation to get the size of the array
int string_length(char str[]) {
    int length = 0;
    while (str[length] != '\0') {
        length++;
    }
    return length;
}

