# Publish
`publish` is one of the simplest static site generators: 
 ```> ./publish.py``` and you are done
## Installation
```
> git clone git@github.com:Zamony/publish.git site && cd site && rm -rf .git
> pipenv install --three
```
## Update
From site folder:
```
> cp -r md-files .. && cd ../
> rm -rf site && git clone git@github.com:Zamony/publish.git site && cd site && rm -rf .git 
> rm -rf md-files && mv ../md-files .
> pipenv install --three
```
## Usage
use this command to build your website's pages:
>./publish.py

if it fails, you need to locate your Python3 binary:
>[PATH_TO_YOUR_PYTHON3_INTERPRETER_BINARY] publish.py
 
use this command to show the help message:
>./publish.py --help

Hint: use Python to view your website's pages in browser (0.0.0.0:8888)
>[PATH_TO_YOUR_PYTHON3_INTERPRETER_BINARY] -m http.server 8888
