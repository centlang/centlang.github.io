import tempfile
import os
import subprocess
import re
import shutil
import markdown
import html

SRC_DIRS = ["docs/"]
TEMPLATES_DIR = "templates/"
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
    return re.sub(
        r'<pre><code(?:\s+class="language-(\w+)")?>(.*?)</code></pre>',
        lambda m: nvim_to_html(html.unescape(m.group(2)), m.group(1)),
        code,
        flags=re.DOTALL,
    )

def render_template(code: str, context: dict) -> str:
    code = re.sub(
        r"{{\s*(\w+)\s*}}", lambda m: context.get(m.group(1), ""), code
    )

    match = re.match(r"{%\s*extends (\w+)\s*%}", code)

    if match:
        path = os.path.join(TEMPLATES_DIR, f"{match.group(1)}.html")
        context = context | {"content": re.sub(r"{%.*?%}", "", code)}

        return render_template(open(path).read(), context)

    return code

def render_page(code: str, md: bool = False) -> str:
    if md:
        match = re.match(r"{%\s*extends (\w+)\s*%}", code)

        if match:
            path = os.path.join(TEMPLATES_DIR, f"{match.group(1)}.html")
            content = highlight_html(
                markdown.markdown(
                    re.sub(r"{%.*?%}", "", code), extensions=["fenced_code"]
                )
            )

            return render_template(open(path).read(), {"content": content})

    return render_template(code, {})

def main():
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    os.mkdir(BUILD_DIR)

    shutil.copytree("static", os.path.join(BUILD_DIR, "static"))

    with open(os.path.join(BUILD_DIR, "index.html"), "w") as file:
        file.write(render_page(open("index.html").read()))

    for dir in SRC_DIRS:
        output_dir = BUILD_DIR + dir
        os.mkdir(output_dir)

        for root, _, files in os.walk(dir):
            for file in files:
                if not file.endswith((".md", ".html")):
                    continue

                input = os.path.join(root, file)

                output = os.path.join(
                    output_dir,
                    os.path.relpath(input, dir).replace(".md", ".html"),
                )

                print(f"{input} -> {output}")

                with open(output, "w") as output_file:
                    output_file.write(
                        render_page(open(input).read(), file.endswith(".md"))
                    )

if __name__ == "__main__":
    main()
