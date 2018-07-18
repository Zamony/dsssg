import datetime
import pathlib
import unittest
from unittest.mock import ANY, Mock, call, create_autospec, patch

import jinja2

import publish


class TestPublish(unittest.TestCase):

    def test_translit_uppercase_lowered(self):
        title = "TITLE"
        #
        result = publish.translit(title)
        #
        self.assertEqual(result, "title")

    def test_translit_rus_to_eng(self):
        title = "строка"
        #
        result = publish.translit(title)
        #
        self.assertEqual(result, "stroka")

    def test_tranlit_space_to_dash(self):
        title = "title title title"
        #
        result = publish.translit(title)
        #
        self.assertEqual(result, "title-title-title")

    def test_translit_removes_non_alnum(self):
        title = "hey! is it title?"
        #
        result = publish.translit(title)
        #
        self.assertEqual(result, "hey-is-it-title")

    def test_translit_preserves_numbers(self):
        title = "title 1"
        #
        result = publish.translit(title)
        #
        self.assertEqual(result, "title-1")

    def test_translit_no_double_dash(self):
        title = "double  space  here"
        #
        result = publish.translit(title)
        #
        self.assertEqual(result, "double-space-here")

    def test_translit_not_starts_with_dash(self):
        title = "      many spaces"
        #
        result = publish.translit(title)
        #
        self.assertEqual(result, "many-spaces")

    def test_translit_not_ends_with_dash(self):
        title = "many spaces      "
        #
        result = publish.translit(title)
        #
        self.assertEqual(result, "many-spaces")

    def test_parse_ordinary_inline(self):
        lines = [
            "<!--title Default title-->\n",
        ]

        #
        post = publish.parse(lines)
        #
        self.assertIn("title", post)
        self.assertEqual(post["title"], "Default title")

    def test_parse_no_identifiers(self):
        lines = [
            "no\n",
            "identifiers\n"
        ]

        #
        post = publish.parse(lines)
        #
        self.assertIn("content", post)
        self.assertEqual(post["content"], "no\nidentifiers\n")

    def test_parse_inline_identifier_no_value(self):
        lines = [
            "<!--title-->\n",
        ]
        #
        post = publish.parse(lines)
        #
        self.assertEqual(len(post.keys()), 0)

    def test_parse_comment_ignored(self):
        lines = [
            "<!-- comment comment -->"
        ]
        #
        post = publish.parse(lines)
        #
        self.assertEqual(len(post.keys()), 0)

    @patch("publish.translit")
    @patch("publish.parse")
    def test_posts_generator_not_hidden_post(
        self, mock_parse, mock_translit
    ):
        mock_parse.return_value = dict(title="title 1", date="01.01.2018")
        mock_translit.return_value = "title-1"
        md = create_autospec(pathlib.Path)
        md.name = "file.md"
        output_folder = pathlib.Path("posts")

        #
        post = next(publish.posts_generator([md], output_folder))

        #
        self.assertEqual(post.url, "title-1")
        self.assertEqual(post.date, datetime.datetime(2018, 1, 1))
        self.assertTrue(post.listed)

    @patch("publish.translit")
    @patch("publish.parse")
    def test_posts_generator_hidden_post(
        self, mock_parse, mock_translit
    ):
        mock_parse.return_value = dict(title="title 1", date="01.01.2018")
        mock_translit.return_value = "title-1"
        md = create_autospec(pathlib.Path)
        md.name = "_file.md"
        output_folder = pathlib.Path("posts")

        #
        post = next(publish.posts_generator([md], output_folder))

        #
        self.assertFalse(post.listed)

    @patch("publish.translit")
    @patch("publish.parse")
    def test_posts_generator_invalid_date(
        self, mock_parse, mock_translit
    ):
        mock_parse.return_value = dict(title="title 1", date="date")
        mock_translit.return_value = "title-1"
        md = create_autospec(pathlib.Path)
        md.name = "file.md"
        output_folder = pathlib.Path("posts")

        #
        #
        with self.assertRaises(ValueError) as context:
            next(publish.posts_generator([md], output_folder))

        self.assertIn("date", str(context.exception))

    @patch("publish.translit")
    @patch("publish.parse")
    def test_posts_generator_invalid_title(
        self, mock_parse, mock_translit
    ):
        mock_parse.return_value = dict(title="", date="01.05.2018")
        mock_translit.return_value = ""
        md = create_autospec(pathlib.Path)
        md.name = "file.md"
        output_folder = pathlib.Path("posts")

        #
        #
        with self.assertRaises(ValueError) as context:
            next(publish.posts_generator([md], output_folder))

        self.assertIn("title", str(context.exception))

    @patch("pathlib.Path.joinpath")
    def test_make_page_template_not_found(self, mock_join):
        template_engine = Mock()
        template_engine.get_template.side_effect = jinja2.TemplateNotFound(
            "post.html"
        )

        output_folder = pathlib.Path("posts")

        meta_post = Mock(spec=publish.MetaPost)
        meta_post.url = "test"

        #
        #
        with self.assertRaises(jinja2.TemplateNotFound) as context:
            publish.make_page(meta_post, output_folder, template_engine)

        self.assertIn("page", str(context.exception))

    @patch("pathlib.Path.joinpath")
    def test_make_page_template_found(self, mock_join):
        template_engine = Mock()
        template_engine.get_template().render.return_value = "Text"

        output_folder = pathlib.Path("posts")

        meta_post = Mock(spec=publish.MetaPost)
        meta_post.url = "test"

        #
        publish.make_page(meta_post, output_folder, template_engine)

        #
        mock_join.assert_has_calls([
            call("test"), call().mkdir(exist_ok=True),
            call("test", "index.html"), call().write_text("Text")
        ])

    @patch("pathlib.Path")
    def test_make_index_template_not_found(self, mock_path):
        template_engine = Mock()
        template_engine.get_template.side_effect = jinja2.TemplateNotFound(
            "index.html"
        )

        output_folder = pathlib.Path("pages")

        index = [Mock(spec=publish.MetaPost)]
        index[0].url = "test"

        #
        #
        with self.assertRaises(jinja2.TemplateNotFound) as context:
            publish.make_index(index, output_folder, template_engine)
        self.assertIn("index", str(context.exception))

    @patch("pathlib.Path")
    def test_make_index_template_found(self, mock_path):
        template_engine = Mock()
        template_engine.get_template().render.return_value = "Text"

        output_folder = pathlib.Path("pages")

        index = [Mock(spec=publish.MetaPost)]
        index[0].url = "test"
        #
        publish.make_index(index, output_folder, template_engine)
        #
        mock_path.assert_has_calls([
            call("index.html"), call().write_text("Text")
        ])

    def test_post2html(self):
        mock_markdown = Mock()
        mock_markdown.return_value = "<p>text<p>"

        meta_post = publish.MetaPost(
            body={"content": "text\n"},
            url="test",
            listed=True,
            date=None,
        )

        #
        new_meta_post = publish.post2html(meta_post, mock_markdown)
        #
        mock_markdown.assert_called_once_with("text\n")
        self.assertEqual(new_meta_post.body["content"], "<p>text<p>")

    @patch("publish.make_page")
    @patch("publish.post2html")
    @patch("publish.get_md_files")
    @patch("publish.posts_generator")
    def test_publish_pages(
        self, mock_gen, mock_get_md, mock_post2html, mock_make_page
    ):
        meta_post = publish.MetaPost(
            body={"content": "text"},
            listed=True, date=None, url=None
        )
        meta_html_post = publish.MetaPost(
            body={"content": "<p>text</p>\n"}, listed=True, date=None, url=None
        )
        meta_post_empty_content = publish.MetaPost(
            body={"content": ""}, listed=True, date=None, url=None
        )

        mock_get_md.return_value = [pathlib.Path("file.md")]
        mock_gen.return_value = iter([meta_post])
        mock_post2html.return_value = meta_html_post

        mock_path = Mock()
        mock_md = Mock()
        mock_template_engine = Mock()

        #
        index = publish.publish_pages(mock_path, mock_md, mock_template_engine)
        #
        mock_get_md.assert_called_once()
        mock_gen.assert_called_once_with([pathlib.Path("file.md")], ANY)
        mock_post2html.assert_called_once_with(meta_post, ANY)
        mock_make_page.assert_called_once_with(meta_html_post, ANY, ANY)
        self.assertEqual([meta_post_empty_content], index)

    @patch("pathlib.Path")
    def test_get_md_files(self, mock_path):
        #
        publish.get_md_files()
        #
        mock_path.assert_has_calls([
            call("md-files"), call().mkdir(exist_ok=True),
            call().glob("*.md")
        ])

    @patch("shutil.rmtree")
    def test_make_directory_clean(self, mock_rmtree):
        directory = Mock()
        directory.__str__ = Mock(return_value="dir")
        #
        publish.make_directory_clean(directory)
        #
        mock_rmtree.assert_called_once_with("dir")
        directory.__str__.assert_called_once()
        directory.assert_has_calls([call.mkdir()])
