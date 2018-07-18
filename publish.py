#! /usr/bin/env python

import collections
import datetime
import locale
import pathlib
import shutil
from typing import Dict, Iterable, Iterator, List

import jinja2
import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

MetaPost = collections.namedtuple(
    "MetaPost", ["body", "listed", "date", "url"]
)


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            print("no lang")
            return f"\n<pre><code>{mistune.escape(code)}</code></pre>\n"
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        formatter.noclasses = True
        return highlight(code, lexer, formatter)


def translit(title: str) -> str:
    rus = "абвгдеёжзийклмнопрстуфхцчшщьъыэюя "
    eng = ("a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "iy",
           "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h",
           "ts", "ch", "sh", "sch", "", "", "y", "e", "u", "ya", "-")

    title = title.strip().lower()
    new_title = ""
    for ch in title:
        idx = rus.find(ch)
        if idx >= 0:
            new_title += eng[idx]
        elif ch.isalnum():
            new_title += ch

    while "--" in new_title:
        new_title = new_title.replace("--", "-")

    return new_title.strip("-")


def parse(lines: Iterable[str]) -> Dict[str, str]:
    pref, suff = "<!--", "-->"
    post = collections.defaultdict(str)

    for line in lines:
        if line.lstrip().startswith(pref) and line.rstrip().endswith(suff):
            line = line.strip()
            space_idx = line.find(" ")
            identifier = line[len(pref):space_idx]
            if space_idx > 0 and identifier.isidentifier():
                post[identifier] = line[space_idx+1:-len(suff)]
        else:
            post["content"] += line

    return post


def posts_generator(
    md_files: Iterable[pathlib.Path], output_folder: pathlib.Path
) -> Iterator[MetaPost]:
    for md in md_files:
        body = None
        with md.open() as file:
            body = parse(file)

        post_url = translit(body["title"])
        if post_url == "":
            raise ValueError(
                """{}: неправильное или отсутствующее поле title.
                Поле title должно содержать буквы""".format(md.name)
            )

        try:
            date = datetime.datetime.strptime(
                body["date"].strip(), "%d.%m.%Y"
            )
        except ValueError as std_date_exception:
            raise ValueError(
                """{}: неправильное или отсутствующее поле date.
                Дата должна быть в формате дд.мм.ГГГГ""".format(md.name)
            ) from std_date_exception

        yield MetaPost(
            body=body, url=str(post_url),
            listed=not md.name.startswith("_"), date=date
        )


def get_md_files() -> Iterator[pathlib.Path]:
    md_folder = pathlib.Path("md-files")
    md_folder.mkdir(exist_ok=True)
    return md_folder.glob("*.md")


def make_directory_clean(directory: pathlib.Path) -> None:
    shutil.rmtree(f"{directory}")
    directory.mkdir()


def publish_pages(
    output_folder: pathlib.Path, markdown_generator: mistune.Markdown,
    template_engine: jinja2.Environment
) -> List[MetaPost]:
    index = []
    md_files = get_md_files()
    for meta_post in posts_generator(md_files, output_folder):
        meta_post = post2html(meta_post, markdown_generator)
        make_page(meta_post, output_folder, template_engine)
        meta_post.body["content"] = ""
        if meta_post.listed:
            index.append(meta_post)

    return index


def make_page(
    meta_post: MetaPost, output_folder: pathlib.Path,
    template_engine: jinja2.Environment
) -> None:
    try:
        page = template_engine.get_template("page.html")
    except jinja2.TemplateNotFound as template_not_found_err:
        raise jinja2.TemplateNotFound(
            "Не найден шаблон для страницы статьи: theme/page.html"
        ) from template_not_found_err

    html = page.render(post=meta_post)
    output_folder.joinpath(meta_post.url).mkdir(exist_ok=True)
    output_folder.joinpath(meta_post.url, "index.html").write_text(html)


def make_index(
    index: List[MetaPost], pages_folder: pathlib.Path,
    template_engine: jinja2.Environment
) -> None:
    try:
        index_page = template_engine.get_template("index.html")
    except jinja2.TemplateNotFound as template_not_found_err:
        raise jinja2.TemplateNotFound(
            "Не найден шаблон главной страницы: theme/index.html"
        ) from template_not_found_err

    html = index_page.render(posts=index, pages_folder=str(pages_folder))
    pathlib.Path("index.html").write_text(html)


def post2html(meta_post: MetaPost, markdown: mistune.Markdown) -> MetaPost:
    for key in meta_post.body:
        if "\n" in meta_post.body[key]:
            meta_post.body[key] = markdown(meta_post.body[key])
    return meta_post


if __name__ == "__main__":
    renderer = HighlightRenderer()
    markdown_generator = mistune.Markdown(renderer=renderer)
    template_engine = jinja2.Environment(
        loader=jinja2.FileSystemLoader("theme")
    )

    pages_folder = pathlib.Path("pages")
    pages_folder.mkdir(exist_ok=True)
    make_directory_clean(pages_folder)

    index = []
    try:
        index = publish_pages(
            pages_folder, markdown_generator, template_engine
        )
    except (ValueError, jinja2.TemplateNotFound) as err:
        print(err)

    index.sort(key=lambda post: post.date, reverse=True)
    make_index(index, pages_folder, template_engine)
