import requests
import validators


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# A function that checks whether the value of header tag is in consistent format or not
# consistent value is like: "tag1=val1,tag2=val2,..."
def check_queries_format(entered_queries: str) -> bool:
    global number_of_errors
    if entered_queries.startswith("\"") and entered_queries.endswith("\""):
        for key_value in entered_queries.split("&"):
            key_value_list = key_value.split("=")
            if len(key_value_list) != 2:
                number_of_errors += 1
                print(Colors.ERROR + 'error {}: Query content is invalid. Its format must be like "key1=val1&'
                                     'key2=val2&...".'.format(number_of_errors) + Colors.END)
                return False
            else:
                if key_value_list[0] == "" or key_value_list[1] == "":
                    number_of_errors += 1
                    print(Colors.ERROR + 'error {}: Query content is invalid. Its format must be like "key1=val1&'
                                         'key2=val2&...".'.format(number_of_errors) + Colors.END)
                    return False
    else:
        number_of_errors += 1
        print(Colors.ERROR + 'error {}: Header content is invalid. It must be within "".'.format(number_of_errors) +
              Colors.END)
    return True


# A function that checks whether the value of header tag is in consistent format or not
# consistent value is like: "tag1=val1,tag2=val2,..."
def check_headers_format(entered_headers: str) -> bool:
    global number_of_errors
    if entered_headers.startswith("\"") and entered_headers.endswith("\""):
        for key_value in entered_headers.split(","):
            key_value_list = key_value.split(":")
            if len(key_value_list) != 2:
                number_of_errors += 1
                print(Colors.ERROR + 'error {}: Header content is invalid. Its format must be like "key1:val1,'
                                     'key2:val2,...".'.format(number_of_errors) + Colors.END)
                return False
            else:
                if key_value_list[0] == "" or key_value_list[1] == "":
                    number_of_errors += 1
                    print(Colors.ERROR + 'error {}: Header content is invalid. Its format must be like "key1:val1,'
                                         'key2:val2,...".'.format(number_of_errors) + Colors.END)
                    return False
    else:
        number_of_errors += 1
        print(Colors.ERROR + 'error {}: Header content is invalid. It must be within "".'.format(number_of_errors) +
              Colors.END)
    return True


# A function that checks whether an entered method is supported or not
def check_method(entered_method: str) -> bool:
    global number_of_errors
    if entered_method in {"GET", "POST", "PATCH", "DELETE", "PUT"}:
        return True
    else:
        number_of_errors += 1
        print(Colors.ERROR + "error {}: method {} is not supported. Only GET, POST, PATCH, DELETE and PUT methods are "
                             "valid.".format(number_of_errors, entered_method) + Colors.END)
        return False


# A function that using validator package checks whether a str is in a valid URL form or not
def check_URL(URL: str) -> bool:
    global number_of_errors
    if validators.url(URL) is True:
        return True
    else:
        number_of_errors += 1
        print(Colors.ERROR + "error {}: URL is not valid!".format(number_of_errors) + Colors.END)
        return False


# A function that checks whether the input instruction has fulfilled the criteria or not.
# it calls a separate function to check each criterion.
def check_validity(instruction_set: [str]) -> bool:
    global number_of_errors
    final_status = True
    final_tag = None

    for index, instruction in enumerate(instruction_set):
        if index == 0:
            if check_URL(instruction) is False:
                final_status = False
        else:
            if index % 2 == 1:
                final_tag = instruction
            else:
                if tags_functions_check.__contains__(final_tag):
                    if tags_functions_check[final_tag](instruction) is False:
                        final_status = False
                else:
                    number_of_errors += 1
                    print(Colors.ERROR + "error {}: tag {} is not supported. Enter help to see available tags.".format(
                        number_of_errors, final_tag) + Colors.END)

    return final_status


# The main function which takes input, checks its validity, sends the request and prints the response
def main():
    global number_of_errors
    input_instruction = input("Insert a command, type help to see input structures or type exit to stop the "
                              "program.\n")
    while input_instruction != "exit":
        if input_instruction == "help":
            pass
        else:
            instruction_set = input_instruction.split(" ")
            if check_validity(instruction_set):
                pass

        number_of_errors = 0
        input_instruction = input("Insert a new command, type help to see input structures or type exit to stop the "
                                  "program.\n")
    print("Have fun!\nGood Bye.")


tags_functions_check = {
    "--method": check_method,
    "-M": check_method,
    "--headers": check_headers_format,
    "-H": check_headers_format
}
number_of_errors = 0

if __name__ == '__main__':
    main()
