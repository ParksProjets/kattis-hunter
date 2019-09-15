# Some information about Kattis

## Login on Kattis using an email address

Login on Kattis using an email address is quite simple, in two steps.  
First, you need to retreive CSRF token from login page. It is in the hidden
field named `csrf_token`.
> https://kth.kattis.com/login/email

Then you have to make a POST request to the same URL as above with the following
data (using `application/x-www-form-urlencoded` as `Content-Type`).

```json
{
    "csrf_token": "<CRSF token from login page>",
    "user": "<email address>",
    "password": "<password>",
    "submit": "Submit"
}
```

Do not forget to keep the same cookies you used to retrieve CSRF token. If you
get a redirection to `https://kth.kattis.com/users/...` then you are logged,
otherwise you did something wrong.



## Submitting files for a problem

Like the login procedure, there are two steps to do.  
First, you need to retreive CSRF token from submit page. It is in the hidden
field named `csrf_token`. Parameter `{pid}` is the problem ID (like
`kth.ai.duckhunt`).
> https://kth.kattis.com/problems/{pid}/submit

Then you have to make a POST request to the same URL as above with the following
data.

```json
{
    "csrf_token": "<CRSF token from submit page>",
    "type": "files",
    "sub_code": "",
    "problem": "<Problem ID>",
    "language": "C++",  // Or the language you want.
    "submit": "Submit",
    "submit_ctr": 10
}
```

Files are sent in field `sub_file[]`. For them, use content type
`application/octet-stream`. If you get a redirection to
`https://kth.kattis.com/submissions/{sid}` then it's fine.



## Getting information about a submission

You can use the following link for getting information about a submission
(parameter `{sid}` is the submission ID):
> https://kth.kattis.com/submissions/{sid}?only_submission_row

This link will return a JSON object (even if `Content-Type` is `text/html`),
like the one below.

```js
{
    "component": "<tr>...</tr>",  // HTML content of result table.
    "status_id": 3,  // Status of the execution (see below).
    "testcases_number": 1  // Number of executed tests (passed or failed).
}
```

Key `status_id` will be one of the following values:

| Status ID | Description               |
|:---------:|---------------------------|
|     0     | New                       |
|     3     | Compiling                 |
|     5     | Running                   |
|     8     | Accepted or Compile Error |
|     9     | Run Time Error            |
