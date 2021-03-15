# HTTP_Client_CLI
A Command Line Interface which gets an HTTP client request, interprets it, sends it and finally prints the result.

The request is consists of the following parts:

URL [--tag1 or -T1] [value of tag1] [--tag2 or -T2] [value of tag2] ...


Supportings tags are listed below:
1. --method or -M: corresponding values must be from "GET, POST, PATCH, DELETE, PUT". Other values return an error. Besides, if this tag was missing, default method will be set to GET.

2. --heades or -H: 

* URL must be in a valid form, otherwise the program returns an error and exits. Also, special characters within "" in the URL address are handled.
