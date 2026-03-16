# Python Static Site Generator

A static site generator built from scratch in Python. Converts Markdown files into a full HTML site using a template. Built as part of a [Boot.dev](https://boot.dev) course.

## How it works

1. Markdown files in `content/` are parsed into an HTML node tree
2. The tree is rendered into HTML and injected into `template.html`
3. Output files are written to `docs/`
4. Static assets from `static/` are copied to `docs/`

## Usage

**Run locally:**
```bash
bash main.sh
```
Generates the site and serves it at `http://localhost:8888`.

**Build for GitHub Pages:**
```bash
bash build.sh
```
Generates the site with the correct base path for deployment.

**Run tests:**
```bash
bash test.sh
# or
python -m pytest
```

## Project structure

```
content/       # Markdown source files
static/        # Static assets (CSS, images)
docs/          # Generated output (served by GitHub Pages)
template.html  # HTML template
src/           # Source code
  tests/       # Test suite
```

## Supported Markdown

- Headings (`#` through `######`)
- Bold (`**text**`), italic (`_text_`), inline code (`` `text` ``)
- Fenced code blocks
- Unordered and ordered lists
- Blockquotes
- Links and images
