## About
`publish` is one of the simplest static site generators 
## Requerements && Dependencies
Python3, Mistune, Jinja2
## Usage
use this command to build your website's pages:
>./publish.py

if it fails, you need to locate your Python3 binary:
>[PATH_TO_YOUR_PYTHON3_INTERPRETER_BINARY] publish.py
 
use this command to show this message:
>./publish.py --help

NB! Each `*.md` file should have these three contructions defined: 
<!-- date -->
01.01.1970
<!-- title -->
This is the title of my post
<!-- content -->
My post's content

Hint: use Python to view your website's pages in browser (0.0.0.0:8888)
>[PATH_TO_YOUR_PYTHON3_INTERPRETER_BINARY] -m http.server 8888
