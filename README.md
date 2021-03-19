# HTTP_Client_CLI
A Command Line Interface which gets an HTTP client request, interprets it, sends it and finally prints the result.<br>
The request is consists of the following parts:

URL [--tag1 or -T1] [value of tag1] [--tag2 or -T2] [value of tag2] ...

* URL must be in a valid form, otherwise the program returns an error and exits. Also, special characters within " " in the URL address are handled.

Supportings tags are listed below:
1. --method or -M: <br>
corresponding values must be in "GET, POST, PATCH, DELETE, PUT". Other values return an error. Besides, if this tag was missing, default method will be set to GET.

2. --headers or -H: <br>
using this, user can define some http headers for his request. Also, this tag-value can be repeated multiple times and finaly, program will combine them and sets a uniqe header and then sends the request.
corresponding values must be within " " and their structure is like "key1:value1,key2:value2,...". Respectively, ',' can not be used in values.<br>
if user enters a key multiple times, the system will consider the final value and prints a warning telling that this key has been used several times and I send the final value.<br>
all keys are set lowercase before sending.

3. --queries or -Q: <br>
all definitions are same is header except for the format which is like: "key1=value1&key2=value2&..."

4. --data or -D: <br>
used to write body part in requests. This argument sets Content-Type header as application/x-www-form-urlencoded by default and respectively input must be in the format of key1=value1&key2=value2&... ; otherwise although it send the body without making any changes in it, it prints a warning for user telling that the input is not in the format of x-www-form-urlencoded.

5. --json or -J: <br>
to support json format. IT sets Content-Type header as applicatoin/json and will set the value as the body part. Other definitions are same as data tag.

* the headers which are set in --headers tag have more priority compared to --data or --json tags. for instance, the request below is correct: <br>
‫‪foo.com‬‬ ‫‪–H‬‬ ‫”‪“content-type:application/json‬‬ ‫‪--data‬‬ ‫‪“{\”name\”:\”hadi\”,\”last\”:‬‬ ‫”}”\‪\”taba‬‬ ‫‪–M‬‬ ‫‪POST‬‬ <br>
and its functionality is exactly same is: <br>
‫‪foo.com‬‬ ‫‪--json‬‬ ‫‪“{\”name\”:\”hadi\”,\”last\”:‬‬ ‫”}”\‪\”taba‬‬ ‫‪-M‬‬ ‫‪POST‬‬

* in this exaple Content-Type header firstly is set to x-www-form-urlencoded and then using -H argument, it will override into application/json. Only it prints a warning which has been introduced before.
* Similarly, 2 following instructions have same functionality: <br>
‫‪foo.com‬‬ ‫‪--data‬‬ ‫”‪“name=hadi&last=taba‬‬ ‫‪–M‬‬ ‫‪POST‬‬ <br>
‫‪foo.com‬‬ ‫‪-H‬‬ ‫”‪“content-type:application/x-www-form-urlencoded‬‬ ‫‪--json‬‬ ‫”‪“name=hadi&last=taba‬‬ ‫‪-M‬‬ ‫‪POST‬‬

6. --file or -F: <br>
corresponding value must be the address of a file which will be set as the body of the request.<br>
* the address can be relative or absolute.
* content-type header is set to application/octet-stream by default.
* if there was no file in the address, an error will be returned and the program exits.

7. --timeout or -T: <br>
corresponding value is a number representing after how many seconds the program should close the request and prints the relevant message.<br>
By default, it is set to infinity.


Another capabilites of this program are listed below:
* a bar which represent the loading of the request. It starts when request is sent and reaches 100% when the response is received. Timeout value is also supported here.
* after getting a response, its method, status code, status message, all headers , etc. will be shown.
* if headers show that the body is related to a pdf, jpg, png or gif file, it will be stored in desktop. otherwise, the whole buddy will be printed in the consol. (dump)
