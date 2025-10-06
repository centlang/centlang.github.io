import tempfile
import os
import subprocess
import re
import shutil
import markdown
import html

SRC_DIRS = ["docs/"]
BUILD_DIR = "build/"

def nvim_to_html(code: str, lang: str) -> str:
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp_input:
        tmp_input_path = tmp_input.name
        tmp_input.write(code)
        tmp_input.flush()

    with tempfile.NamedTemporaryFile(delete=False) as tmp_output:
        tmp_output_path = tmp_output.name

    subprocess.run(
        [
            "nvim",
            "--headless",
            "-i",
            "NONE",
            f"+e {tmp_input_path}",
            f"+set ft={lang}",
            "+TOhtml",
            f"+w! {tmp_output_path}",
            "+qa",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    html = open(tmp_output_path).read()
    match = re.search(r"<pre.*?</pre>", html, flags=re.DOTALL)

    os.remove(tmp_input_path)
    os.remove(tmp_output_path)

    return match.group(0) if match else f"<pre><code>{code}</code></pre>"

def highlight_html(code: str) -> str:
    def replace(match):
        lang = match.group(1)
        code = html.unescape(match.group(2))

        return nvim_to_html(code, lang)

    return re.sub(
        r'<pre><code(?:\s+class="language-(\w+)")?>(.*?)</code></pre>',
        replace,
        code,
        flags=re.DOTALL,
    )

def render_page(md_code: str) -> str:
    return highlight_html(
        markdown.markdown(md_code, extensions=["fenced_code"])
    )

def main():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

    os.mkdir(BUILD_DIR)

    shutil.copytree("static", os.path.join(BUILD_DIR, "static"))
    shutil.copy("index.html", os.path.join(BUILD_DIR, "index.html"))

    for dir in SRC_DIRS:
        output_dir = BUILD_DIR + dir
        os.mkdir(output_dir)

        for root, _, files in os.walk(dir):
            for file in files:
                if file.endswith(".md"):
                    input = os.path.join(root, file)

                    output = os.path.join(
                        output_dir,
                        os.path.relpath(input, dir).replace(".md", ".html"),
                    )

                    print(f"{input} -> {output}")

                    with open(output, "w") as output_file:
                        output_file.write(render_page(open(input).read()))

if __name__ == "__main__":
    main()
