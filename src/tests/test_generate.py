import os
import pytest
from html_functions import generate_page, generate_pages_recursively


TEMPLATE = """\
<!doctype html>
<html>
  <head>
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <article>{{ Content }}</article>
  </body>
</html>"""


@pytest.fixture
def template_file(tmp_path):
    t = tmp_path / "template.html"
    t.write_text(TEMPLATE)
    return str(t)


class TestGeneratePage:
    def test_creates_output_file(self, tmp_path, template_file):
        src = tmp_path / "index.md"
        src.write_text("# Hello\n\nSome content.")
        dest = tmp_path / "out" / "index.html"

        generate_page(str(src), template_file, str(dest), "/")

        assert dest.exists()

    def test_title_injected(self, tmp_path, template_file):
        src = tmp_path / "index.md"
        src.write_text("# My Title\n\nParagraph.")
        dest = tmp_path / "index.html"

        generate_page(str(src), template_file, str(dest), "/")

        html = dest.read_text()
        assert "<title>My Title</title>" in html

    def test_content_injected(self, tmp_path, template_file):
        src = tmp_path / "index.md"
        src.write_text("# Title\n\nHello world.")
        dest = tmp_path / "index.html"

        generate_page(str(src), template_file, str(dest), "/")

        html = dest.read_text()
        assert "Hello world" in html

    def test_placeholders_replaced(self, tmp_path, template_file):
        src = tmp_path / "index.md"
        src.write_text("# Title\n\nContent.")
        dest = tmp_path / "index.html"

        generate_page(str(src), template_file, str(dest), "/")

        html = dest.read_text()
        assert "{{ Title }}" not in html
        assert "{{ Content }}" not in html

    def test_basepath_applied_to_href(self, tmp_path, template_file):
        src = tmp_path / "index.md"
        src.write_text("# Title\n\nContent.")
        dest = tmp_path / "index.html"

        generate_page(str(src), template_file, str(dest), "/mysite/")

        html = dest.read_text()
        assert 'href="/index.css"' not in html
        assert 'href="/mysite/index.css"' in html

    def test_creates_parent_directories(self, tmp_path, template_file):
        src = tmp_path / "index.md"
        src.write_text("# Title\n\nContent.")
        dest = tmp_path / "a" / "b" / "c" / "index.html"

        generate_page(str(src), template_file, str(dest), "/")

        assert dest.exists()

    def test_markdown_rendered_to_html(self, tmp_path, template_file):
        src = tmp_path / "index.md"
        src.write_text("# Title\n\n**bold** and _italic_")
        dest = tmp_path / "index.html"

        generate_page(str(src), template_file, str(dest), "/")

        html = dest.read_text()
        assert "<b>bold</b>" in html
        assert "<i>italic</i>" in html


class TestGeneratePagesRecursively:
    def test_generates_single_md_file(self, tmp_path, template_file):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "index.md").write_text("# Home\n\nWelcome.")
        dest = tmp_path / "dest"
        dest.mkdir()

        generate_pages_recursively(str(tmp_path / "src"), template_file, str(dest), "/")

        assert (dest / "index.html").exists()

    def test_md_extension_replaced_with_html(self, tmp_path, template_file):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "page.md").write_text("# Page\n\nContent.")
        dest = tmp_path / "dest"
        dest.mkdir()

        generate_pages_recursively(str(tmp_path / "src"), template_file, str(dest), "/")

        assert (dest / "page.html").exists()
        assert not (dest / "page.md").exists()

    def test_recurses_into_subdirectories(self, tmp_path, template_file):
        src = tmp_path / "src"
        (src / "blog").mkdir(parents=True)
        (src / "blog" / "post.md").write_text("# Post\n\nBody.")
        dest = tmp_path / "dest"
        dest.mkdir()

        generate_pages_recursively(str(src), template_file, str(dest), "/")

        assert (dest / "blog" / "post.html").exists()

    def test_multiple_files_generated(self, tmp_path, template_file):
        src = tmp_path / "src"
        src.mkdir()
        (src / "a.md").write_text("# A\n\nContent A.")
        (src / "b.md").write_text("# B\n\nContent B.")
        dest = tmp_path / "dest"
        dest.mkdir()

        generate_pages_recursively(str(src), template_file, str(dest), "/")

        assert (dest / "a.html").exists()
        assert (dest / "b.html").exists()

    def test_non_md_files_ignored(self, tmp_path, template_file):
        src = tmp_path / "src"
        src.mkdir()
        (src / "index.md").write_text("# Title\n\nContent.")
        (src / "notes.txt").write_text("just a text file")
        dest = tmp_path / "dest"
        dest.mkdir()

        generate_pages_recursively(str(src), template_file, str(dest), "/")

        assert not (dest / "notes.txt").exists()
        assert not (dest / "notes.html").exists()
