# Some information about Kattis


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
    "testcases_number": 1  // Number of passed tests.
}
```

Key `status_id` will be one of the following values:

| Status ID | Description    |
|:---------:|----------------|
|     0     | New            |
|     3     | Compiling      |
|     5     | Running        |
|     8     | Accepted       |
|     9     | Run Time Error |
