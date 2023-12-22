#!C:/Program Files/nodejs/node.exe 

const method = process.env['REQUEST_METHOD']

process.stdout.write("Content-Type: text/html\r\n");
process.stdout.write("\r\n");
process.stdout.write(`<!doctype html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Py-201</title>
</head>

<body>
    <h1>CGI працює з JSS</h1>
    <b>Method: ${method}<b>
</body>

</html>
`);