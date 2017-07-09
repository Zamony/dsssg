#NEXT LINE GOES YOUR POST'S DATE:
10.07.2017
#NEXT LINE GOES YOUR POST'S TITLE: 
On Code Snippets Support
#NEXT LINE GO YOUR META-KEYWORDS
dsssg, static site generator
#NEXT LINE GOES YOUR META-DESCRIPTION
You will know how to setup your own DSSSG blog
#PUT YOUR POST INTRODUCTION BELOW (OPTIONAL, BLANK IF YOU USE DEFAULT THEME). MAKE SURE YOU HAVE ONE EMPTY LINE AFTER IT
Example text goes
here

#PUT YOUR POST'S CONTENT BELOW
DSSSG uses Prism.js code highlighter by default. If you wanna use code snippets in your blog, you are recommended to visit Prism.js website and configure your own prism.js file. Put it in the theme folder.
Just place HTML tags `<pre><code class="language-xxx"></code></pre>` in your .md file, like this:
<pre>
<code class="language-python">
def make_index_and_posts_pages(posts_tuple):
	"""
	The argument is inner representation of all posts
	Creates HTML file of index page. Creates folders for posts and their HTML files.
	Uses Jinja2 as template engine
	"""
	jenv = jinja2.Environment(
	    loader=jinja2.FileSystemLoader( os.path.join( os.path.dirname(__file__), THEME_FOLDER ) )
	)

	index_page = jenv.get_template('index.html')
	index_page_code = index_page.render(posts=posts_tuple)
	with open("index.html", "w") as fh:
	    fh.write(index_page_code)

	for post in posts_tuple:
		post_page = jenv.get_template('post.html')
		post_page_code = post_page.render(post=post)

		post_dir = "." + post["url"] 
		os.mkdir( post_dir )
		with open( os.path.join(post_dir, "index.html"), "w") as fh:
			fh.write(post_page_code)

</code>
</pre>

