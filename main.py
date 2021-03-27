import requests
import validators
import json
import os
import sys
import cgi
from tqdm import tqdm


class Colors:
    CYAN = '\033[96m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'


# A class which its object contains all the parameters needed to send an HTTP request
class HTTPRequestParams:
    def __init__(self):
        # variables containing default information to send an HTTP request
        self.headers = {}
        self.queries = {}
        self.files = {}
        self.method = "GET"
        self.URL = ""
        self.data = None
        self.timeout = -1
        self.file_addresses = []
        self.number_of_files = 0

    # function to set HTTP request method
    def set_method(self, entered_method):
        self.method = entered_method

    # function to set HTTP request URL
    def set_URL(self, entered_URL):
        self.URL = entered_URL

    # function to add a header for HTTP request
    def add_header(self, new_header_key, new_header_value):
        global number_of_warnings
        if self.headers.__contains__(new_header_key):
            number_of_warnings += 1
            print(Colors.WARNING + 'warning {}: {} header has changed from {} to {}.'.format(
                number_of_warnings, new_header_key, self.headers[new_header_key], new_header_value) + Colors.END)
        self.headers[new_header_key.lower()] = new_header_value

    # function to add a query for HTTP request
    def add_query(self, new_query_key, new_query_value):
        global number_of_warnings
        if self.queries.__contains__(new_query_key):
            number_of_warnings += 1
            print(Colors.WARNING + 'warning {}: query value of key {} has changed from {} to {}.'.format(
                number_of_warnings, new_query_key, self.headers[new_query_key], new_query_value) + Colors.END)
        self.queries[new_query_key.lower()] = new_query_value

    # function to set data for HTTP request
    def set_data(self, entered_data):
        self.data = entered_data

    # function to set timeout for HTTP request
    def set_timeout(self, timeout_seconds):
        self.timeout = timeout_seconds

    # function to get timeout for HTTP request, it returns None if no timeout is set that causes timeout to be infinity
    def get_timeout(self):
        if self.timeout == -1:
            return None
        else:
            return self.timeout

    # function to add a new file address to its list
    def add_file_address(self, new_file_address):
        self.file_addresses.append(new_file_address)

    # function to set file to send in HTTP request
    def set_file(self):
        self.number_of_files += 1
        self.files["file" + str(self.number_of_files)] = open(self.file_addresses[self.number_of_files - 1], 'rb')

    # function that returns None if no file is set and returns file dictionary if we have a file to send
    def get_files(self):
        if self.number_of_files == 0:
            return None
        else:
            return self.files


# function that returns file extension of a HTTP file using its content-type header
def get_file_extension(MIME_content_type: str) -> str:
    file_type = MIME_content_type.split(";")[0]
    # some application formats
    if file_type == "application/pdf":
        return ".pdf"

    # some text formats
    elif file_type == "text/html":
        return ".html"

    # some image formats
    elif file_type == "image/png":
        return ".png"
    elif file_type == "image/jpeg":
        return ".jpg"
    elif file_type == "image/gif":
        return "gif"

    # some video formats
    elif file_type == "video/mp4":
        return ".mp4"
    elif file_type == "video/webm":
        return ".webm"
    elif file_type == "video/ogg":
        return ".ogv"
    elif file_type == "video/3gpp":
        return ".3gp"

    # some audio formats
    elif file_type == "audio/mpeg":
        return ".mp3"

    # other formats : not safe
    else:
        return "." + MIME_content_type.split("/")[1]


# A function that again parses input and sets required params to send an HTTP request
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
                    request_params.set_file()
                elif final_tag == "-T" or final_tag == "--timeout":
                    request_params.set_timeout(float(instruction))


# A function that sends HTTP request with predefined params and after receiving response, it prints result
# Also, using a try-catch we define timeout for request
def send_HTTP_request():
    global number_of_errors, request_params
    try:
        response = requests.request(url=request_params.URL,
                                    method=request_params.method,
                                    params=request_params.queries,
                                    data=request_params.data,
                                    files=request_params.get_files(),
                                    headers=request_params.headers,
                                    timeout=request_params.get_timeout(),
                                    stream=True)

        # printing result #############################################
        # print elapsed time
        print(Colors.CYAN + "Response time in sec: " + Colors.END + response.elapsed.total_seconds().__str__())
        # print method, URL, status code and status message
        print(Colors.CYAN + "Method: " + Colors.END + response.request.method, Colors.CYAN + "\nURL: " + Colors.END
              + response.url, Colors.CYAN + "\nStatus: " + Colors.END + response.status_code.__str__() + " " +
              response.reason)
        # print headers and corresponding values
        for header, value in response.headers.items():
            print(Colors.CYAN + header + ": " + Colors.END + value)

        # print or save content
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024

        instruction = input("\nEnter:\t1 to print content-text\n\t2 to print content-bytes\n\t3 to save it to file.\n")
        print()
        if instruction == "1":
            for data in response.iter_lines(block_size):
                print(data)
        elif instruction == "2":
            for data in response.iter_content(block_size):
                print(data)
        elif instruction == "3":
            # if filename and its extension can be read from headers, we use that to save the file,
            # otherwise we try to derive them
            if response.headers.__contains__("content-disposition"):
                value, params = cgi.parse_header(response.headers["Content-Disposition"])
                file_path = os.path.join(os.getcwd(), params["filename"])
            else:
                # if the type of file can be derived from content-type header, we use that, otherwise
                # we save the content in a txt file
                if response.headers.__contains__("content-type"):
                    file_extension = get_file_extension(response.headers["content-type"])
                else:
                    file_extension = ".txt"
                file_name = "downloaded"
                i = 1

                # finding a new filename in the current directory to save the file into it
                file_path = os.path.join(os.getcwd(), (file_name + file_extension))
                while os.path.isfile(file_path) is True:
                    i += 1
                    file_path = os.path.join(os.getcwd(), (file_name + i.__str__() + file_extension))

            # a new filename in the current directory is founded, so we save the file in it
            progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

            with open(file_path, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

            progress_bar.close()
            print("file stored in : ", file_path)
        else:
            print("wrong instruction. By default, context body will be printed as txt:\n")
            print(response.text)
    except requests.Timeout:
        number_of_errors += 1
        print(Colors.ERROR + 'error {}: request timeout.'.format(number_of_errors) + Colors.END)
    except requests.exceptions.RequestException as e:
        number_of_errors += 1
        print(Colors.ERROR + 'error {}: following error occurred while sending request.'.
              format(number_of_errors) + Colors.END)
        print(Colors.ERROR + e.__str__() + Colors.END)


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
def check_file_format(entered_address: str) -> bool:
    global number_of_errors, request_params
    request_params.add_header("content-type", "application/octet-stream")

    if os.path.isabs(entered_address):
        file_address = entered_address
    else:
        file_address = os.path.join(os.getcwd(), entered_address)

    if os.path.isfile(file_address):
        request_params.add_file_address(file_address)
        return True
    else:
        number_of_errors += 1
        print(Colors.ERROR + 'error {}: There is no file in the entered address.'.format(number_of_errors) +
              Colors.END)
        return False


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

    if entered_data.startswith("\"") and entered_data.endswith("\""):
        entered_data = entered_data[1: len(entered_data) - 1]

    for key_value in entered_data.split("&"):
        key_value_list = key_value.split("=")
        if len(key_value_list) != 2:
            number_of_warnings += 1
            print(Colors.WARNING + 'warning {}: Data content is not in x-www-form-urlencoded format.'.format(
                number_of_warnings) + Colors.END)
        else:
            if key_value_list[0] == "" or key_value_list[1] == "":
                number_of_warnings += 1
                print(Colors.WARNING + 'warning {}: Data content is not in x-www-form-urlencoded format.'.format(
                    number_of_warnings) + Colors.END)
    return True


# A function that checks whether the value of header tag is in consistent format or not
# consistent value is like: "tag1=val1,tag2=val2,..."
def check_queries_format(entered_queries: str) -> bool:
    global number_of_errors
    if entered_queries.startswith("\"") and entered_queries.endswith("\""):
        entered_queries = entered_queries[1: len(entered_queries) - 1]

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
    return True


# A function that checks whether the value of header tag is in consistent format or not
# consistent value is like: "tag1=val1,tag2=val2,..."
def check_headers_format(entered_headers: str) -> bool:
    global number_of_errors
    if entered_headers.startswith("\"") and entered_headers.endswith("\""):
        entered_headers = entered_headers[1: len(entered_headers) - 1]

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
