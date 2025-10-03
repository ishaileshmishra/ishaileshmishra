#!/usr/bin/env python3
import io, sys, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
README = os.path.join(ROOT, 'README.md')
SRC = os.path.join(ROOT, 'README_ARTICLES.md')

START = '<!-- ARTICLES_START -->'
END = '<!-- ARTICLES_END -->'

def read_file(path):
    with io.open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def inject():
    if not os.path.exists(SRC):
        print(f"Source file not found: {SRC}", file=sys.stderr)
        sys.exit(1)
    src_content = read_file(SRC).strip()

    readme_content = read_file(README)
    pattern = re.compile(
        rf'({re.escape(START)})(.*)({re.escape(END)})',
        flags=re.DOTALL
    )

    if not pattern.search(readme_content):
        print(f"Markers not found in {README}. Please add {START} and {END}", file=sys.stderr)
        sys.exit(1)

    replacement = f"{START}\n\n{src_content}\n\n{END}"
    new_content = pattern.sub(replacement, readme_content)

    if new_content == readme_content:
        print("No changes to README.")
    else:
        write_file(README, new_content)
        print("Injected README_ARTICLES.md into README.md")

if __name__ == "__main__":
    inject()
