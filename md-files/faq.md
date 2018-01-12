<!-- date -->
09.07.2017
<!-- title -->
How To Use DSSG && Custom Themes
<!-- meta_keywords -->
dsssg, static site generator
<!-- meta_description -->
You will know how to setup your own DSSSG blog
<!-- content -->
## How to create a post?
Go to the *md-file* folder. Then create a .md file of your post with the structure like this. Then open terminal in the base folder of DSSSG ( there should be publish.py ) and type in the terminal `python3 publish.py`
## Are custom themes supported?
Sure. DSSSG uses Jinja2 as a template engine, so just make sure you have two files in your theme: index.html and post.html for the index and post pages accordingly.
Then you should be able to access DSSSG variables `post` and `posts`.
Further reading on the [Jinja2 website](http://jinja.pocoo.org/docs/2.9/templates/ "Jinja2 website").
You can use default theme as an example.
