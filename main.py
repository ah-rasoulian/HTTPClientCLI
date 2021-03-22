import requests
import validators
import json
import os
import sys


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


class HTTPRequestParams:
    def __init__(self):
        # variables containing default information to send an HTTP request
        self.headers = {}
        self.queries = {}
        self.method = "GET"
        self.URL = ""
        self.data = None
        self.timeout = -1

    def set_method(self, entered_method):
        self.method = entered_method

    def set_URL(self, entered_URL):
        self.URL = entered_URL

    def add_header(self, new_header_key, new_header_value):
        global number_of_warnings
        if self.headers.__contains__(new_header_key):
            number_of_warnings += 1
            print(Colors.WARNING + 'warning {}: {} header has changed from {} to {}.'.format(
                number_of_warnings, new_header_key, self.headers[new_header_key], new_header_value) + Colors.END)
        self.headers[new_header_key.lower()] = new_header_value

    def add_query(self, new_query_key, new_query_value):
        global number_of_warnings
        if self.queries.__contains__(new_query_key):
            number_of_warnings += 1
            print(Colors.WARNING + 'warning {}: query value of key {} has changed from {} to {}.'.format(
                number_of_warnings, new_query_key, self.headers[new_query_key], new_query_value) + Colors.END)
        self.queries[new_query_key.lower()] = new_query_value

    def set_data(self, entered_data):
        self.data = entered_data

    def set_timeout(self, timeout_seconds):
        self.timeout = timeout_seconds

    def get_timeout(self):
        if self.timeout == -1:
            return None
        else:
            return self.timeout


def set_HTTP_request_params(instruction_set: [str]):
    global request_params
    final_tag = None

    for index, instruction in enumerate(instruction_set):
        instruction: str
        if index == 0:
            request_params.set_URL(instruction)
        else:
            if index % 2 == 1:
                final_tag = instruction
            else:
                if final_tag == "-M" or final_tag == "--method":
                    request_params.set_method(instruction)
                elif final_tag == "-H" or final_tag == "--headers":
                    for key_value in instruction.split(","):
                        key_value_list = key_value.split(":")
                        request_params.add_header(key_value_list[0], key_value_list[1])
                elif final_tag == "-Q" or final_tag == "--queries":
                    for key_value in instruction.split("&"):
                        key_value_list = key_value.split("=")
                        request_params.add_query(key_value_list[0], key_value_list[1])
                elif final_tag == "-D" or final_tag == "--data":
                    request_params.set_data(instruction)
                elif final_tag == "-J" or final_tag == "--json":
                    request_params.set_data(instruction)
                elif final_tag == "-F" or final_tag == "--file":
                    file = open(instruction)
                    request_params.set_data(file.read())
                    file.close()
                elif final_tag == "-T" or final_tag == "--timeout":
                    request_params.set_timeout(float(instruction))


def send_HTTP_request():
    global number_of_errors, request_params
    try:
        response = requests.request(url=request_params.URL,
                                    method=request_params.method,
                                    params=request_params.queries,
                                    data=request_params.data,
                                    headers=request_params.headers,
                                    timeout=request_params.get_timeout())

        print(response.content)
    except requests.Timeout:
        number_of_errors += 1
        print(Colors.ERROR + 'error {}: request timeout.'.format(number_of_errors) + Colors.END)


# A function that checks whether the value of timeout tag is numeric or not
def check_timeout_format(entered_value: str) -> bool:
    global number_of_errors
    try:
        float(entered_value)
    except ValueError:
        number_of_errors += 1
        print(Colors.ERROR + 'error {}: timeout value can not be converted into a floating point.'.format(
            number_of_errors) + Colors.END)
        return False
    return True


# A function that checks whether any file exists in the entered address or not
# it also returns the absolute path to that file
def check_file_format(entered_address: str) -> (bool, str):
    global number_of_errors, request_params
    request_params.add_header("content-type", "application/octet-stream")

    if os.path.isabs(entered_address):
        file_address = entered_address
    else:
        file_address = os.path.join(os.getcwd(), entered_address)

    if os.path.isfile(file_address):
        return True, file_address
    else:
        number_of_errors += 1
        print(Colors.ERROR + 'error {}: There is no file in the entered address.'.format(number_of_errors) +
              Colors.END)
        return False, ""


# A function that checks whether the value of data tag is within "" or not
# it also prints a warning when data is not in x-www-form-urlencoded format
def check_json_format(entered_data: str) -> bool:
    global number_of_errors, number_of_warnings, request_params
    request_params.add_header("content-type", "application/json")

    try:
        json.loads(entered_data)
    except ValueError:
        number_of_warnings += 1
        print(Colors.WARNING + 'warning {}: json content is not in valid format.'.format(
            number_of_warnings) + Colors.END)
    return True


# A function that checks whether the value of data tag is within "" or not
# it also prints a warning when data is not in x-www-form-urlencoded format
def check_data_format(entered_data: str) -> bool:
    global number_of_errors, number_of_warnings, request_params
    request_params.add_header("content-type", "application/x-www-form-urlencoded")

    for key_value in entered_data.split("&"):
        key_value_list = key_value.split("=")
        if len(key_value_list) != 2:
            number_of_warnings += 1
            print(Colors.WARNING + 'warning {}: Data content is not in x-www-form-urlencoded format.'.format(
                number_of_warnings) + Colors.END)
            return True
        else:
            if key_value_list[0] == "" or key_value_list[1] == "":
                number_of_warnings += 1
                print(Colors.WARNING + 'warning {}: Data content is not in x-www-form-urlencoded format.'.format(
                    number_of_warnings) + Colors.END)
                return True
    return True


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
        return False
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
        return False
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
def check_URL(entered_URL: str) -> bool:
    global number_of_errors
    if validators.url(entered_URL) is True:
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
                    final_status = False

    return final_status


# The main function which takes input, checks its validity, sends the request and prints the response
# This function is ran when no console arguments is passed when calling this program and it takes arguments by
# asking user to enter it
def main_no_console_args():
    global number_of_errors, request_params
    input_instruction = input("Insert a command, type help to see input structures or type exit to stop the "
                              "program.\n")
    while input_instruction != "exit":
        if input_instruction == "help":
            pass
        else:
            instruction_set = input_instruction.split(" ")
            request_params = HTTPRequestParams()
            if check_validity(instruction_set):
                set_HTTP_request_params(instruction_set)
                send_HTTP_request()

        number_of_errors = 0
        input_instruction = input("Insert a new command, type help to see input structures or type exit to stop the "
                                  "program.\n")
    print("Have fun!\nGood Bye.")


# The main function which takes input, checks its validity, sends the request and prints the response
# This function is ran when arguments are passed via console
def main_console_args():
    global request_params
    input_instruction = sys.argv[1:]
    request_params = HTTPRequestParams()
    if check_validity(input_instruction):
        set_HTTP_request_params(input_instruction)
        send_HTTP_request()


tags_functions_check = {
    "--method": check_method,
    "-M": check_method,
    "--headers": check_headers_format,
    "-H": check_headers_format,
    "--queries": check_queries_format,
    "-Q": check_queries_format,
    "--data": check_data_format,
    "-D": check_data_format,
    "--json": check_json_format,
    "-J": check_json_format,
    "--file": check_file_format,
    "-F": check_file_format,
    "--timeout": check_timeout_format,
    "-T": check_timeout_format
}
number_of_errors = 0
number_of_warnings = 0
request_params = HTTPRequestParams()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main_console_args()
    else:
        main_no_console_args()
