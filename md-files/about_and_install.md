<!-- date -->
08.07.2017
<!-- title -->
About && Installation Guide
<!-- meta_keywords -->
dsssg, static site generator
<!-- meta_description -->
You will know how to setup your own DSSSG blog
<!-- content -->
What is DSSSG? DSSSG is a dead-simple static site generator. You just create a .md file of your blog post, then type
`python3 publish.py`
and you are done.
## Installation
It works only on Python 3.3+ and you must install some dependencies. DSSSG uses mistune to convert Markdown into HTML, it also uses Jinja2 as a template engine.
    pip3 install mistune
    pip3 install jinja2
Then download DSSSG
