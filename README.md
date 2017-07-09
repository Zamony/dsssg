## About
DSSSG is a dead-simple static site generator. You just create a .md file of your blog post, then type
`python3 publish.py`
and you are done.
It's fully GithubPages-compatible: https://zamony.github.io/
## Installation
It works only on Python 3.3+ and you must install some dependencies. DSSSG uses mistune to convert Markdown into HTML, it also uses Jinja2 as a template engine.
    `pip3 install mistune`
    `pip3 install jinja2`
Then download DSSSG
## How to create a post?
Go to the *md-file* folder. Then create a .md file of your post with the structure like this. Then open terminal in the base folder of DSSSG ( there should be publish.py ) and type in the terminal `python3 publish.py`
## Are custom themes supported?
Sure. DSSSG uses Jinja2 as a template engine, so just make sure you have two files in your theme: index.html and post.html for the index and post pages accordingly.
Then you should be able to access DSSSG variables `post` and `posts`.
Further reading on the [Jinja2 website](http://jinja.pocoo.org/docs/2.9/templates/ "Jinja2 website").
You can use default theme as an example.
## Code Snippets
DSSSG uses Prism.js code highlighter by default. If you wanna use code snippets in your blog, you are recommended to visit Prism.js website and configure your own prism.js file. Put it in the theme folder.
Just place HTML tags `<pre><code class="language-xxx"></code></pre>` in your .md file, like this:
