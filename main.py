import requests
import validators


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    Error = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# A function that using validator package checks whether a str is in a valid URL form or not
def check_URL(URL: str) -> bool:
    if validators.url(URL) is True:
        return True
    else:
        return False


# A function that checks whether the input instruction has fulfilled the criteria or not.
# it calls a separate function to check each criterion.
def check_validity(instruction_set: [str]) -> bool:
    final_status = True
    error_number = 1
    for index, instruction in enumerate(instruction_set):
        if index == 0:
            if check_URL(instruction) is False:
                final_status = False
                print(Colors.UNDERLINE + "error {}: URL is not valid!".format(error_number) + Colors.END)
                error_number += 1
        else:
            pass
    return final_status


# The main function which takes input, checks its validity, sends the request and prints the response
def main():
    input_instruction = input()
    while input_instruction != "exit":
        instruction_set = input_instruction.split(" ")
        if check_validity(instruction_set):
            pass

        input_instruction = input()
    print("exited from CLI")


if __name__ == '__main__':
    main()
