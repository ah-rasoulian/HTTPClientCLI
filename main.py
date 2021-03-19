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


# A function that checks whether an entered method is supported or not
def check_method(entered_method):
    global number_of_errors
    if entered_method in {"GET", "POST", "PATCH", "DELETE", "PUT"}:
        return True
    else:
        print(Colors.ERROR + "error {}: method {} is not supported. Only GET, POST, PATCH, DELETE and PUT methods are "
                             "valid.".format(number_of_errors, entered_method) + Colors.END)
        number_of_errors += 1
        return False


# A function that using validator package checks whether a str is in a valid URL form or not
def check_URL(URL: str) -> bool:
    global number_of_errors
    if validators.url(URL) is True:
        return True
    else:
        print(Colors.ERROR + "error {}: URL is not valid!".format(number_of_errors + 1) + Colors.END)
        number_of_errors += 1
        return False


# A function that checks whether the input instruction has fulfilled the criteria or not.
# it calls a separate function to check each criterion.
def check_validity(instruction_set: [str]) -> bool:
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
                if tags_functions_check[final_tag](instruction) is False:
                    final_status = False

    return final_status


# The main function which takes input, checks its validity, sends the request and prints the response
def main():
    input_instruction = input("Insert a command, type help to see input structures or type exit to stop the "
                              "program.\n")
    while input_instruction != "exit":
        if input_instruction == "help":
            pass
        else:
            instruction_set = input_instruction.split(" ")
            if check_validity(instruction_set):
                pass

        input_instruction = input("Insert a new command, type help to see input structures or type exit to stop the "
                                  "program.")
    print("Have fun!\nGood Bye.")


tags_functions_check = {
    "--method": check_method,
    "-M": check_method,
}
number_of_errors = 0

if __name__ == '__main__':
    main()
