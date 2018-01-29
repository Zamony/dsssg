#!/usr/bin/env python

"""
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
"""

import re
import os
import sys
import shutil
import locale
import jinja2
import mistune
from datetime import datetime

POSTS_FOLDER, MDS_FOLDER, THEME_FOLDER = "posts", "md-files", "theme"
LOCALE, TIME_FORMAT = "ru_RU.UTF-8", "%d.%m.%Y"

locale.setlocale(locale.LC_ALL, LOCALE)

def translit(word):
    rus = "абвгдеёжзийклмнопрстуфхцчшщьъыэюя "
    eng = ("a","b","v","g","d","e","e","zh","z","i","iy",
           "k","l","m","n","o","p","r","s","t","u","f","h",
           "ts","ch","sh","sch","","","y","e","u","ya","-")

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

def get_parse_err(body, md_name):
    for var in ("date", "content", "title"):
        if var not in body:
            return True, "`{}` not in {}, aborting".format(var, md_name)
        elif str(body[var]).strip() == "":
            return True, "`{}` is empty (in {}), aborting".format(var, md_name)
    try:
        datetime.strptime(body["date"].strip(), TIME_FORMAT)
    except ValueError:
        return ( True, 
            "Incorrect `date` format in {}, got: {}" \
            "Should be {}".format(md_name, body["date"].strip(), TIME_FORMAT)
            )
    return False, ""

def posts_generator():
    if MDS_FOLDER not in os.listdir():
        os.mkdir(MDS_FOLDER)
        print("{} folder wasn't found, making one...".format(MDS_FOLDER))
        print("Write some `*.md` files to the folder and try again.")
        sys.exit()
    
    md_filenames = os.listdir(MDS_FOLDER)
    for md_filename in md_filenames:
        md_file = os.path.join(MDS_FOLDER, md_filename)
        with open(md_file) as file:
            body = parse( file.readlines() )
            was_err, err_msg = get_parse_err(body, md_filename)
            if was_err: sys.exit(err_msg)

            if "cut" in body:
                body["cut"], body["content"] = body["content"], body["cut"]
                body["content"] = body["cut"] + body["content"]

            body["url"] = translit( body["title"] )
            body["url"] = os.path.join("/", POSTS_FOLDER, body["url"])
            body["not_listed"] = md_filename.startswith(".")
            body["date"] = body["date"].strip()
            body["date"] = datetime.strptime(body["date"], TIME_FORMAT)
        yield body

def publish_post(post):
    post["content"] = mistune.markdown(post["content"], escape=False)
    if "cut" in post: post["cut"] = mistune.markdown(post["cut"], escape=False)
    
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
    if POSTS_FOLDER in os.listdir(): shutil.rmtree(POSTS_FOLDER)
    os.mkdir(POSTS_FOLDER)

    index_dicts = []
    for post in posts_generator():
        publish_post(post)
        del post["content"]
        if not post["not_listed"]: index_dicts.append(post)

    index_dicts.sort(key=lambda post: post["date"], reverse=True )
    publish_index(index_dicts)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        publish()
        print("Successfully created your website!")
    else:
        print(__doc__)
