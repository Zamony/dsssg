import re
import os
import shutil
import jinja2
import mistune
import datetime

POSTS_FOLDER, MDS_FOLDER, THEME_FOLDER = "posts", "md-files", "theme"

def translit(word):
    rus = "абвгдеёжзийклмнопрстуфхцчшщьъыэюя "
    eng = ("a","b","v","g","d","e","e","zh","z","i","iy","k","l","m","n","o","p",
           "r","s","t","u","f","h","ts","ch","sh","sch","","","y","e","u","ya","-")

    word = word.strip().lower()
    new_word = ""
    for ch in word:
        idx = rus.find(ch)
        if idx >= 0: new_word += eng[idx]
        elif ch.isalnum(): new_word += ch

    while "--" in new_word: new_word = new_word.replace("--", "-")

    return new_word.strip("-")

def parse(lines):
    regex = re.compile(r"(?<=^<!--) *\w+ *(?=-->\n$)")

    body = dict()
    found = None
    tag_name, content = "", ""
    for line in lines:
        found = regex.search(line)
        if found is not None:
            if tag_name != "": body[tag_name] = content
            tag_name = found.group().strip()
            content = ""
        else:
            content += line

    body[tag_name] = content
    return body

def posts_generator():
    md_filenames = os.listdir(MDS_FOLDER)

    for md_filename in md_filenames:
        md_file = os.path.join(MDS_FOLDER, md_filename)
        with open(md_file) as file:
            body = parse( file.readlines() )
            body["url"] = translit( body["title"] )
            body["url"] = os.path.join("/", POSTS_FOLDER, body["url"])
            body["not_listed"] = md_filename.startswith(".")
            body["date"] = body["date"].strip()
            body["date"] = datetime.datetime.strptime(body["date"], "%d.%m.%Y")
        yield body

def publish_post(post):
    post["content"] = mistune.markdown(post["content"], escape=False)

    theme_path = os.path.join(os.path.dirname(__file__), THEME_FOLDER)
    template_loader = jinja2.FileSystemLoader(theme_path)
    engine = jinja2.Environment(loader=template_loader)

    post_template = engine.get_template("post.html")
    page = post_template.render(post=post)

    post_folder = os.path.join("." + post["url"])
    post_file = os.path.join(post_folder, "index.html")
    os.mkdir(post_folder)

    with open(post_file, "w") as f:
        f.write(page)

def publish_index(index_dicts):
    theme_path = os.path.join(os.path.dirname(__file__), THEME_FOLDER)
    template_loader = jinja2.FileSystemLoader(theme_path)
    engine = jinja2.Environment(loader=template_loader)
    index_template = engine.get_template("index.html")

    page = index_template.render(posts=index_dicts)
    with open("index.html", "w") as f:
        f.write(page)

def publish():
    shutil.rmtree(POSTS_FOLDER)
    os.mkdir(POSTS_FOLDER)

    index_dicts = []
    for post in posts_generator():
        publish_post(post)
        if "content" in post.keys(): del post["content"]
        if   not post["not_listed"]: index_dicts.append(post)

    index_dicts.sort(key=lambda post: post["date"], reverse=True )
    publish_index(index_dicts)

if __name__ == "__main__":
    publish()
